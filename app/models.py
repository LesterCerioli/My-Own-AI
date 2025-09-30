from sqlalchemy import Column, String, Text, DateTime, JSON, Boolean, ForeignKey, Integer  # Added Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
from app.database import Base

class Project(Base):
    __tablename__ = "projects"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    name = Column(String(255), nullable=False)
    language = Column(String(100), nullable=False)
    requirements = Column(Text, nullable=False)
    status = Column(String(50), default="pending")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class DeepSeekResponse(Base):
    __tablename__ = "deepseek_responses"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id"), nullable=False)
    prompt = Column(Text, nullable=False)
    response = Column(JSON, nullable=False)
    tokens_used = Column(Integer)  # This was causing the error
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class GitHubRepository(Base):
    __tablename__ = "github_repositories"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id"), nullable=False)
    repo_name = Column(String(255), nullable=False)
    repo_url = Column(String(500), nullable=False)
    branch_name = Column(String(255), default="smartai")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class LearningData(Base):
    __tablename__ = "learning_data"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    input_pattern = Column(Text, nullable=False)
    output_pattern = Column(Text, nullable=False)
    language = Column(String(100))
    success_rate = Column(Integer, default=0)  # This was causing the error
    usage_count = Column(Integer, default=0)   # This was causing the error
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())