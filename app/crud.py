from sqlalchemy.orm import Session
from app import models, schemas
import uuid

def create_project(db: Session, project: schemas.ProjectCreate):
    db_project = models.Project(
        id=uuid.uuid4(),
        name=project.name,
        language=project.language,
        requirements=project.requirements
    )
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project

def get_project(db: Session, project_id: uuid.UUID):
    return db.query(models.Project).filter(models.Project.id == project_id).first()

def save_deepseek_response(db: Session, project_id: uuid.UUID, prompt: str, response: dict):
    db_response = models.DeepSeekResponse(
        id=uuid.uuid4(),
        project_id=project_id,
        prompt=prompt,
        response=response
    )
    db.add(db_response)
    db.commit()
    db.refresh(db_response)
    return db_response

def create_github_repo_record(db: Session, project_id: uuid.UUID, repo_name: str, repo_url: str):
    db_repo = models.GitHubRepository(
        id=uuid.uuid4(),
        project_id=project_id,
        repo_name=repo_name,
        repo_url=repo_url
    )
    db.add(db_repo)
    db.commit()
    db.refresh(db_repo)
    return db_repo