
from typing import List
from pydantic import BaseModel

class CacheRequest(BaseModel):
    accession_numbers: List[str]
