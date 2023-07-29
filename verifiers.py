import json
from typing import Union, List

from approvaltests import verify as verify, verify
from pydantic import BaseModel
from pydantic_core import to_jsonable_python


def verify_model(model: Union[List[BaseModel],BaseModel]):
    verify(json.dumps(model, default=to_jsonable_python, indent=4))


def verify_json(output):
    json_encoded_output = json.dumps(output, indent=4)
    verify(json_encoded_output)


def verify_report(lines: List[str]):
    verify("\n".join(lines))
