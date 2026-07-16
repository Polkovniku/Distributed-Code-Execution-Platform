from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.job import JobCreate, JobCreateResponse, JobResponse
from service.job import JobService
from core.dependencies import get_current_user, get_db
from models.user import User

router = APIRouter(prefix="/jobs", tags=["jobs"])

def get_job_service(db: Annotated[AsyncSession, Depends(get_db)]):
    return JobService(db)


@router.get("/", response_model=list[JobResponse])
async def get_jobs(user: Annotated[User, Depends(get_current_user)], service: Annotated[JobService, Depends(get_job_service)]):
    return await service.get_jobs_by_user(user.id)

@router.get("/{job_id}", response_model=JobResponse)
async def get_job(
    job_id: UUID,
    user: Annotated[User, Depends(get_current_user)],
    service: Annotated[JobService, Depends(get_job_service)]
):
    job = await service.get_job_by_id(job_id, user.id)
    if job is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job is not found")
    return job

@router.post("/", response_model=JobCreateResponse)
async def create_job(
    user: Annotated[User, Depends(get_current_user)], 
    data: JobCreate,
    service: Annotated[JobService, Depends(get_job_service)]
):
    job = await service.create_job(user.id, data)
    return JobCreateResponse(job_id=job.id)
    
