"""Serialize output provenance using package-relative paths, without local usernames."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parent.parent

def clean(value):
    if isinstance(value,str):return value.replace(str(ROOT),'evidence/analysis/figures')
    if isinstance(value,list):return [clean(x) for x in value]
    if isinstance(value,tuple):return [clean(x) for x in value]
    if isinstance(value,dict):return {k:clean(v) for k,v in value.items()}
    return value

def dumps(value,*args,**kwargs):return json.dumps(clean(value),*args,**kwargs)
