#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

"""
Register new Pipes
"""
from meerschaum.utils.misc import attempt_import
pydantic = attempt_import('pydantic')

class MetaPipe(pydantic.BaseModel):
    connector_keys : str ### e.g. sql:main
    metric_key : str
    location_key : str = None

