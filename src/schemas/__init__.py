"""Core Model Registry Module."""

from sys import modules

from pytest_loco import schema
from pytest_loco.builtins import checkers
from pytest_loco.schema import inputs, cases

from .helpers import ModelParams, get_model_qualname, rebuild_type, register_model


CHEKERS = {
    checker.name: checker.build()
    for checker in (
        checkers.eq,
        checkers.neq,
        checkers.gt,
        checkers.gte,
        checkers.lt,
        checkers.lte,
        checkers.regex,
    )
}

CHEKS_RENAMES = {
    get_model_qualname(check): '{}Check'.format(''.join(
        item.capitalize()
        for item in name.split('_')
    ))
    for name, check in CHEKERS.items()
}

MODELS = [
    inputs.InputDefinition,
    cases.Parameter,
    schema.BaseAction,
    schema.BaseCheck,
    schema.BaseContent,
    schema.Case,
    schema.IncludeAction,
    schema.Template,
    *CHEKERS.values(),
]

RENAMES = {
    get_model_qualname(schema.BaseAction): 'Action',
    get_model_qualname(schema.BaseCheck): 'Check',
    get_model_qualname(schema.BaseContent): 'Content',
    **CHEKS_RENAMES,
}

PARAMS = ModelParams(
    module=modules[__name__],
    mode='input',
    renames=RENAMES,
)


TypeName = rebuild_type(inputs.TypeName, PARAMS)

for model in MODELS:
    register_model(
        model,  # type: ignore[arg-type]
        PARAMS,
    )
