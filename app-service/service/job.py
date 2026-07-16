from uuid import UUID
from fastapi import HTTPException, status
from models.job import Job
from schemas.job import JobCreate
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from core.celery_app import celery_app
import asyncio

class JobService:
    def __init__(self, db: AsyncSession):
        self.db = db
        
    async def create_job(self, user_id: UUID, data: JobCreate) -> Job:
        job = Job(user_id=user_id, language=data.language, code=data.code)

        try:
            self.db.add(job)
            await self.db.commit()
            await self.db.refresh(job)
        except SQLAlchemyError:
            await self.db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Invalid create job")

        try:
            await asyncio.to_thread(celery_app.send_task, "execute_code_task", args=[str(job.id)])
        except Exception:
            raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail="Failed to queue job")

        return job
        
    async def get_job_by_id(self, job_id: UUID, user_id: UUID) -> Job | None:
        return await self.db.scalar(select(Job).where(Job.id == job_id, Job.user_id == user_id))
    
    async def get_jobs_by_user(self, user_id: UUID) -> list[Job]:
        return (await self.db.scalars(select(Job).where(Job.user_id == user_id).order_by(Job.created_at.desc()))).all()