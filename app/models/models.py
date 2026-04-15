from sqlalchemy import Column, Integer, String, Float, Text, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.database import Base

class Prompt(Base):
    __tablename__ = "prompts"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    versions = relationship("PromptVersion", back_populates="prompt", cascade="all, delete-orphan")

class PromptVersion(Base):
    __tablename__ = "prompt_versions"
    id = Column(Integer, primary_key=True, index=True)
    prompt_id = Column(Integer, ForeignKey("prompts.id"))
    version_number = Column(Integer, nullable=False)
    template = Column(Text, nullable=False)
    variables = Column(JSON, nullable=False)          # e.g. ["text"]
    model = Column(String, default="llama3.1:8b")
    temperature = Column(Float, default=0.7)
    created_at = Column(DateTime, default=datetime.utcnow)

    prompt = relationship("Prompt", back_populates="versions")
    executions = relationship("Execution", back_populates="version", cascade="all, delete-orphan")

class Execution(Base):
    __tablename__ = "executions"
    id = Column(Integer, primary_key=True, index=True)
    version_id = Column(Integer, ForeignKey("prompt_versions.id"))
    input_data = Column(JSON, nullable=False)
    output = Column(Text, nullable=False)
    latency = Column(Float, nullable=False)   # seconds
    created_at = Column(DateTime, default=datetime.utcnow)

    version = relationship("PromptVersion", back_populates="executions")
    evaluations = relationship("Evaluation", back_populates="execution", cascade="all, delete-orphan")

class Evaluation(Base):
    __tablename__ = "evaluations"
    id = Column(Integer, primary_key=True, index=True)
    execution_id = Column(Integer, ForeignKey("executions.id"))
    score = Column(Float, nullable=False)     # 1-10
    method = Column(String, default="manual") # manual | llm_as_judge
    feedback = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    execution = relationship("Execution", back_populates="evaluations")