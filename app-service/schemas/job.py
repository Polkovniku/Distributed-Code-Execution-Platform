from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field, ConfigDict
from models.job import JobStatusEnum

class JobResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    user_id: UUID
    language: str
    status: JobStatusEnum
    stdout: str | None
    stderr: str | None
    exit_code: int | None
    created_at: datetime
    started_at: datetime | None
    finished_at: datetime | None
    
class JobCreate(BaseModel):
    language: str
    code: str = Field(min_length=1)
    
class JobCreateResponse(BaseModel):
    job_id: UUID