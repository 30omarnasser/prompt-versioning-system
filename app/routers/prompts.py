from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.models import Prompt, PromptVersion, Execution, Evaluation
from app.schemas.schemas import (
    PromptCreate, PromptResponse,
    PromptVersionCreate, PromptVersionResponse,
    ExecutionCreate, ExecutionResponse,
    EvaluationCreate, EvaluationResponse,
    CompareRequest
)
from app.services.execution_service import run_prompt

router = APIRouter(prefix="/api", tags=["prompts"])

@router.post("/prompts", response_model=PromptResponse)
def create_prompt(prompt: PromptCreate, db: Session = Depends(get_db)):
    db_prompt = Prompt(name=prompt.name, description=prompt.description)
    db.add(db_prompt)
    db.commit()
    db.refresh(db_prompt)
    return db_prompt

@router.post("/prompts/{prompt_id}/versions", response_model=PromptVersionResponse)
def create_version(prompt_id: int, version: PromptVersionCreate, db: Session = Depends(get_db)):
    # Auto-increment version number
    max_version = db.query(PromptVersion).filter(PromptVersion.prompt_id == prompt_id)\
        .order_by(PromptVersion.version_number.desc()).first()
    new_version_num = (max_version.version_number + 1) if max_version else 1

    db_version = PromptVersion(
        prompt_id=prompt_id,
        version_number=new_version_num,
        template=version.template,
        variables=version.variables,
        model=version.model,
        temperature=version.temperature
    )
    db.add(db_version)
    db.commit()
    db.refresh(db_version)
    return db_version

@router.post("/execute", response_model=ExecutionResponse)
def execute(execution: ExecutionCreate, db: Session = Depends(get_db)):
    version = db.query(PromptVersion).filter(PromptVersion.id == execution.version_id).first()
    if not version:
        raise HTTPException(status_code=404, detail="Version not found")

    output, latency = run_prompt(
        version.template,
        execution.input_data,
        version.model,
        version.temperature
    )

    db_exec = Execution(
        version_id=version.id,
        input_data=execution.input_data,
        output=output,
        latency=latency
    )
    db.add(db_exec)
    db.commit()
    db.refresh(db_exec)
    return db_exec

@router.get("/executions")
def get_executions(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    executions = db.query(Execution).offset(skip).limit(limit).all()
    return executions

@router.post("/executions/{execution_id}/evaluations", response_model=EvaluationResponse)
def add_evaluation(execution_id: int, eval_data: EvaluationCreate, db: Session = Depends(get_db)):
    exec_obj = db.query(Execution).filter(Execution.id == execution_id).first()
    if not exec_obj:
        raise HTTPException(status_code=404, detail="Execution not found")

    eval_obj = Evaluation(
        execution_id=execution_id,
        score=eval_data.score,
        method=eval_data.method,
        feedback=eval_data.feedback
    )
    db.add(eval_obj)
    db.commit()
    db.refresh(eval_obj)
    return eval_obj

@router.post("/compare")
def compare_versions(compare: CompareRequest, db: Session = Depends(get_db)):
    """A/B test — same input on two versions"""
    v1 = db.query(PromptVersion).filter(PromptVersion.id == compare.version_id1).first()
    v2 = db.query(PromptVersion).filter(PromptVersion.id == compare.version_id2).first()

    if not v1 or not v2:
        raise HTTPException(status_code=404, detail="One or both versions not found")

    output1, latency1 = run_prompt(v1.template, compare.input_data, v1.model, v1.temperature)
    output2, latency2 = run_prompt(v2.template, compare.input_data, v2.model, v2.temperature)

    return {
        "version1": {"id": v1.id, "version_number": v1.version_number, "output": output1, "latency": latency1},
        "version2": {"id": v2.id, "version_number": v2.version_number, "output": output2, "latency": latency2}
    }