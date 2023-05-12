from pydantic import BaseModel, Field
from typing import Any, List, Dict, Union, Optional


class ErrorResponseModel(BaseModel):
    status_code: int
    detail: str
