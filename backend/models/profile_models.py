from pydantic import BaseModel
from typing import List, Dict

class UserProfile(BaseModel):
    name: str
    email: str
    skills: List[str]
    education: str