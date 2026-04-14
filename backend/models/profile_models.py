from typing import Dict, List

from pydantic import BaseModel, Field


class ResumeItem(BaseModel):
    title: str
    subtitle: str = ""
    duration: str = ""
    description: str = ""
    technologies: List[str] = Field(default_factory=list)
    highlights: List[str] = Field(default_factory=list)
    link: str = ""


class UserProfile(BaseModel):
    name: str
    email: str
    skills: List[str] = Field(default_factory=list)
    education: str = ""
    phone: str = ""
    location: str = ""
    headline: str = ""
    core_competencies: List[str] = Field(default_factory=list)
    experience: List[ResumeItem] = Field(default_factory=list)
    projects: List[ResumeItem] = Field(default_factory=list)
    certifications: List[str] = Field(default_factory=list)
    links: Dict[str, str] = Field(default_factory=dict)
