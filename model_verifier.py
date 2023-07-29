import json
from typing import Union, List

from approvaltests import verify as verify
from pydantic import BaseModel
from pydantic_core import to_jsonable_python


def verify_model(model: Union[List[BaseModel],BaseModel]):
    verify(json.dumps(model, default=to_jsonable_python, indent=4))
