"""
JSON Model Registry Module.

This module extracts Pydantic models from the JSON format plugin, 
replaces their technical internal names with descriptive public names, 
and registers them for use within the pytest-loco-json ecosystem.
"""

from sys import modules

from pytest_loco_json.format import json_format

from .helpers import ModelParams, get_model_qualname, extract_from_root, register_model


DECODER, DECODER_WITH_QUERY, *_ = extract_from_root(json_format.build_decoder())
ENCODER, *_ = extract_from_root(json_format.build_encoder())

RENAMES = {
    get_model_qualname(DECODER): 'Decoder',
    get_model_qualname(DECODER_WITH_QUERY): 'SelectiveDecoder',
    get_model_qualname(ENCODER): 'Encoder',
}

MODELS = {
    DECODER: 'input',
    DECODER_WITH_QUERY: 'input',
    ENCODER: 'input',
}

for model, mode in MODELS.items():
    register_model(
        model,
        ModelParams(
            module=modules[__name__],
            mode=mode,
            renames=RENAMES,
        ),
    )
