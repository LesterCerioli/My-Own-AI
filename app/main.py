# main.py
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import uuid

import models
import schemas
import crud
import services
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/projects/", response_model=schemas.Project)
def create_project(project: schemas.ProjectCreate, db: Session = Depends(get_db)):
    
    db_project = crud.create_project(db, project)
    
    try:
        deepseek_response = services.call_deepseek_api(project.requirements)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao chamar DeepSeek: {str(e)}")

    
    db_project = crud.update_project_deepseek_response(db, db_project.id, deepseek_response)

    
    learning_data = schemas.LearningDataCreate(
        project_id=db_project.id,
        input_data={"requirements": project.requirements},
        output_data=deepseek_response
    )
    crud.create_learning_data(db, learning_data)

    return db_project

@app.post("/projects/{project_id}/publish/")
def publish_project(project_id: uuid.UUID, github_credentials: schemas.GitHubCredentials, db: Session = Depends(get_db)):
    
    db_project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if not db_project:
        raise HTTPException(status_code=404, detail="Projeto não encontrado")

    if not db_project.deepseek_response:
        raise HTTPException(status_code=400, detail="Projeto não possui código gerado")

    
    try:
        repo_url = services.create_github_repo(
            github_credentials.username,
            github_credentials.password,
            github_credentials.repo_name
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao criar repositório no GitHub: {str(e)}")

    
    try:
        services.push_code_to_github(
            github_credentials.username,
            github_credentials.password,
            github_credentials.repo_name,
            db_project.deepseek_response,
            branch="smartai"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao publicar código no GitHub: {str(e)}")

    
    db_project = crud.update_project_github_repo_url(db, project_id, repo_url)

    return {"message": "Projeto publicado com sucesso", "repo_url": repo_url}