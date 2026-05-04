from pydantic import BaseModel
from typing import List , Optional

class Developer(BaseModel):
    name: str
    experience: Optional[int] = None

class Project(BaseModel):
    title: str
    description: Optional[List[str]] = None
    languages:Optional[List[str]] = []
    lead_developers: Developer

