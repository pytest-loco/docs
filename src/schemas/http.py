"""HTTP Model Registry Module.

This module initializes and registers the HTTP-related Pydantic models 
for the pytest-loco-http extension.

It transforms internal models (like `CookieModel`, `RequestModel`) into 
public-facing versions (`Cookie`, `Request`) with specific input/output 
configurations and sanitized names.
"""

from sys import modules

from pytest_loco.schema import BaseCheck

from pytest_loco_http.plugin import http
from pytest_loco_http.schema import (
    CookieModel,
    FileModel,
    FilesModel,
    RequestModel,
    ResponseModel,
    UrlModel,
)

from .helpers import ModelParams, get_model_qualname, register_model


ACTIONS = {
    actor.name: actor.build(namespace=http.name)
    for actor in http.actors
}

ACTION_RENAMES = {
    get_model_qualname(action): 'Http{}'.format(actor_name.capitalize())
    for actor_name, action in ACTIONS.items()
}

RENAMES = {
    get_model_qualname(CookieModel): 'Cookie',
    get_model_qualname(FileModel): 'File',
    get_model_qualname(FilesModel): 'Files',
    get_model_qualname(RequestModel): 'Request',
    get_model_qualname(ResponseModel): 'Response',
    get_model_qualname(UrlModel): 'Url',
    **ACTION_RENAMES,
}

REPLACES = {
    BaseCheck: 'Check',
}

ACTION_MODELS = dict.fromkeys(ACTIONS.values(), 'input')

MODELS = {
    CookieModel: 'output',
    RequestModel: 'output',
    ResponseModel: 'output',
    UrlModel: 'output',
    FilesModel: 'input',
    FileModel: 'input',
    **ACTION_MODELS,
}


for model, mode in MODELS.items():
    register_model(
        model,
        ModelParams(
            module=modules[__name__],
            mode=mode,
            renames=RENAMES,
            replaces=REPLACES,
        ),
    )
