from pydantic import BaseModel, EmailStr
from typing import Optional, Dict, Any, List
from uuid import UUID
from datetime import datetime

class ProjectBase(BaseModel):
    name: str
    language: str
    requirements: str

class ProjectCreate(ProjectBase):
    pass

class Project(ProjectBase):
    id: UUID
    status: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class DeepSeekRequest(BaseModel):
    prompt: str
    max_tokens: Optional[int] = 4000

class DeepSeekResponse(BaseModel):
    id: UUID
    project_id: UUID
    response: Dict[str, Any]
    tokens_used: Optional[int]
    created_at: datetime
    
    class Config:
        from_attributes = True

class GitHubCredentials(BaseModel):
    username: str
    password: str  # ou token
    repo_name: str

class FileStructure(BaseModel):
    path: str
    content: str
    language: str

class ProjectGenerationRequest(BaseModel):
    project: ProjectCreate
    github_credentials: GitHubCredentials

class LearningDataBase(BaseModel):
    input_pattern: str
    output_pattern: str
    language: str

class LearningData(LearningDataBase):
    id: UUID
    success_rate: int
    usage_count: int
    created_at: datetime
    
    class Config:
        from_attributes = True