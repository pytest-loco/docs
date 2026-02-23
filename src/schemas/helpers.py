"""Module for dynamic Pydantic model reconstruction and schema modification."""

from dataclasses import dataclass, field
from inspect import isclass
from gettext import gettext as _
from sys import modules
from typing import Annotated, Any, Literal, Union, get_args, get_origin
from types import ModuleType, NoneType, UnionType

from pydantic import AliasChoices, AliasPath, BaseModel, ConfigDict, Field, RootModel, create_model
from pydantic.fields import FieldInfo


@dataclass(slots=True)
class ModelParams:
    """Configuration parameters for the model reconstruction process.

    Attributes:
        mode: Field processing mode.
            Value `input` uses validation aliases, `output` uses serialization aliases.
        short: If `True`, truncates the model's docstring to the first line.
        module: The target module where new models will be registered.
        renames: A mapping of qualified model names to their new desired names.
        replaces: A mapping of types to be replaced with alternative types.
    """

    mode: Literal['input', 'output'] = 'input'
    short: bool = True

    module: ModuleType = field(default_factory=lambda: modules[__name__])

    renames: dict[str, str] = field(default_factory=dict)
    replaces: dict[Any, Any] = field(default_factory=dict)


def get_model_qualname(model: type[BaseModel]) -> str:
    """Constructs the fully qualified name of a Pydantic model.

    Args:
        model: The Pydantic model class.

    Returns:
        A string representing 'module.classname'.
    """
    return f'{model.__module__}.{model.__name__}'


def rebuild_model(model: type[BaseModel], params: ModelParams) -> type[BaseModel]:
    """Recursively reconstructs a Pydantic model based on provided parameters.

    Args:
        model: The source Pydantic model to rebuild.
        params: Reconstruction configuration.

    Returns:
        A new Pydantic model class or the model name string if a recursion limit is hit.
    """
    if issubclass(model, RootModel):
        root_info = model.model_fields['root']
        return rebuild_type(root_info.annotation, params)

    try:
        return register_model(model, params)
    except RecursionError:
        return model.__name__


def rebuild_type(field_type: Any, params: ModelParams) -> Any:
    """Recursively simplify field types.

    Args:
        field_type: The original type of the field.
        params: Reconstruction configuration.

    Returns:
        The transformed type.
    """
    origin = get_origin(field_type)

    if origin is Annotated:
        base, *_ = get_args(field_type)
        return rebuild_type(base, params)

    if origin is not None:
        if origin is Union or origin is UnionType:
            origin = Union
        args = tuple(rebuild_type(item, params) for item in get_args(field_type))
        return origin[args]

    if replace := params.replaces.get(field_type):
        return replace

    if isclass(field_type) and issubclass(field_type, BaseModel):
        return rebuild_model(field_type, params)

    return field_type


def exclude_none_type(field_type: Any) -> Any:
    """Removes `NoneType` from a `Union` type definition.

    Args:
        field_type: The type to process.

    Returns:
        A `Union` type without `NoneType`, or the original type if it's not a `Union`.
    """
    origin = get_origin(field_type)
    if origin is not Union:
        return field_type

    bases = tuple(
        item
        for item in get_args(field_type)
        if item is not NoneType
    )

    return Union[bases]


def get_field_name(field_alias: str | AliasPath | AliasChoices | None,
                   fallback: str) -> tuple[str, tuple[str, ...]]:
    """Extracts the primary field name and additional aliases from Pydantic alias objects.

    Args:
        field_alias: Pydantic alias configuration (string, `Path`, or `AliasChoices`).
        fallback: The default field name to use if no alias is found.

    Returns:
        A tuple containing (primary_name, tuple_of_additional_aliases).
    """
    if isinstance(field_alias, str):
        return field_alias, ()

    if isinstance(field_alias, AliasChoices):
        field_name, *aliases = (
            alias for alias in field_alias.choices
            if isinstance(alias, str)
        )
        return field_name, aliases

    return fallback, ()


def format_list(*items: tuple, literals: bool = False,
                sep: str = ',', last: str = _('and')) -> str:
    """Formats a sequence of items into a human-readable localized string.

    Args:
        *items: Items to be formatted.
        literals: If `True`, wraps items in double backticks (markdown/rst code style).
        sep: The separator used between items.
        last: The conjunction used before the last item (e.g., `"and"`).

    Returns:
        A formatted string like `"A, B and C"`.
    """
    strings = [
        f'{item}' if not literals else f'``{item}``'
        for item in map(_, map(str, items))
    ]
    if not strings:
        return ''

    if len(strings) == 1:
        return strings[0]

    separated_items = f'{sep} '.join(strings[:-1])
    last_item = strings[-1]

    return f'{separated_items} {last} {last_item}'


def get_field_strings(field_name: str, field_info: FieldInfo,
                      params: ModelParams) -> tuple[str, str | None]:
    """Determines the effective field name and generated description based on aliases.

    Args:
        field_name: The internal attribute name.
        field_info: Pydantic field metadata.
        params: Reconstruction configuration.

    Returns:
        A tuple of (effective_name, combined_description).
    """
    field_aliases = ()
    if params.mode == 'input' and field_info.validation_alias:
        field_name, field_aliases = get_field_name(field_info.validation_alias, field_name)
    if params.mode == 'output' and field_info.serialization_alias:
        field_name, field_aliases = get_field_name(field_info.serialization_alias, field_name)

    description = field_info.description
    if field_aliases:
        if not description:
            description = ''
        else:
            description += '\n\n'
        description += '**{}**: {}'.format(
            _('Aliases'),
            format_list(field_name, *field_aliases, literals=True),
        )

    return field_name, description


def format_description(text: str | None) -> str | None:
    """Formats the description, replacing newlines with double newlines.

    Args:
        text: The original description text.

    Returns:
        The formatted description text.
    """
    if not text:
        return None

    return text.replace('\n', '\n\n')


def rebuild_fields(model: type[BaseModel],
                   params: ModelParams) -> dict[str, tuple[Any, FieldInfo]]:
    """Maps original model fields to new field definitions for the reconstructed model.

    Args:
        model: The source model class.
        params: Reconstruction configuration.

    Returns:
        A dictionary mapping field names to (type, FieldInfo) tuples.
    """
    fields = {}
    for field_name, field_info in model.model_fields.items():
        field_name, description = get_field_strings(field_name, field_info, params)
        field_type = rebuild_type(field_info.annotation, params)

        field_default = field_info.default
        if field_info.default_factory:
            factory = field_info.default_factory
            field_default = factory()
            if isclass(factory) and issubclass(factory, RootModel):
                field_default = field_default.root
        if field_default is not None:
            field_type = exclude_none_type(field_type)

        fields[field_name] = (
            field_type, Field(
                default=field_default,
                title=field_info.title,
                description=format_description(description),
            )
        )

    return fields


def register_model(model: type[BaseModel],
                   params: ModelParams) -> type[BaseModel]:
    """Creates and registers a new Pydantic model in the target module.

    Args:
        model: The source Pydantic model.
        params: Reconstruction configuration.

    Returns:
        The newly created Pydantic model class.
    """
    model_name = model.__name__
    if rename := params.renames.get(get_model_qualname(model)):
        model_name = rename

    if model_ := getattr(params.module, model_name, None):
        return model_

    description = ''
    if model.__doc__:
        description = model.__doc__
        if params.short and (lines := description.splitlines()):
            description = lines[0]

    model_ = create_model(
        model_name,
        __doc__=format_description(description),
        __base__=model,
        __config__=ConfigDict(
            title=model.model_config.get('title'),
        ),
        **rebuild_fields(model, params),
    )

    setattr(params.module, model_name, model_)

    return model_


def extract_from_root(model: type,
                      only_models: bool = True) -> list[type]:
    """Recursively extracts all Pydantic models from a `RootModel` annotation.

    Args:
        model: The `RootModel` class to extract from.
        only_models: If `True`, extract only Pydantic models.

    Returns:
        A list of classes found within the RootModel annotation.
    """
    if isclass(model):
        if issubclass(model, RootModel):
            root_info = model.model_fields['root']
            return extract_from_root(root_info.annotation)
        if issubclass(model, BaseModel):
            return [model]

    origin = get_origin(model)
    if origin is Union or origin is UnionType:
        values = []
        for item in get_args(model):
            values.extend(extract_from_root(item))
        return values

    if not only_models:
        return [model]

    return []
