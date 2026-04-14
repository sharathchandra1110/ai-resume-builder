from pydantic import BaseModel


class JobDescription(BaseModel):
    jd_text: str
    target_title: str = ""
    company_name: str = ""
