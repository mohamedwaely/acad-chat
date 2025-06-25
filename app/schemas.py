from pydantic import BaseModel, field_validator
from typing import List
import datetime

class ChatResponse(BaseModel):
    response: str

class ChatRequest(BaseModel):
    query: str

class ProjectBase(BaseModel):
    title: str
    supervisor: str
    description: str
    tools: List[str]
    team_members: List[str]
    year: int

    @field_validator('year')
    def year_valid(cls, v):
        current_year = datetime.datetime.now().year
        if v < 2023 or v > current_year:
            raise ValueError(f'Year must be between 2023 and {current_year}')
        return v

class ProjectResponse(BaseModel):
    id: int
    title: str
    supervisor: str
    description: str
    tools: List[str]
    team_members: List[str]
    year: int

    class Config:
        from_attributes = True
