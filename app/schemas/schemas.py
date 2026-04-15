from pydantic import BaseModel, ConfigDict
from typing import List, Dict, Any, Optional
from datetime import datetime

class PromptCreate(BaseModel):
    name: str
    description: Optional[str] = None

class PromptResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class PromptVersionCreate(BaseModel):
    prompt_id: int
    template: str
    variables: List[str]
    model: str = "llama3.1:8b"
    temperature: float = 0.7

class PromptVersionResponse(BaseModel):
    id: int
    prompt_id: int
    version_number: int
    template: str
    variables: List[str]
    model: str
    temperature: float
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class ExecutionCreate(BaseModel):
    version_id: int
    input_data: Dict[str, Any]

class ExecutionResponse(BaseModel):
    id: int
    version_id: int
    input_data: Dict[str, Any]
    output: str
    latency: float
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class EvaluationCreate(BaseModel):
    score: float
    method: str = "manual"
    feedback: Optional[str] = None

class EvaluationResponse(BaseModel):
    id: int
    execution_id: int
    score: float
    method: str
    feedback: Optional[str]
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class CompareRequest(BaseModel):
    version_id1: int
    version_id2: int
    input_data: Dict[str, Any]