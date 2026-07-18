from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from models.job import Job, JobStatusEnum
from datetime import datetime, timezone

class JobRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_job_by_id(self, job_id: str) -> Job | None:
        return await self.db.get(Job, UUID(job_id))
    
    async def mark_runnig(self, job: Job) -> None:
        job.status = JobStatusEnum.RUNNING
        job.started_at = datetime.now(timezone.utc)
        await self.db.commit()
        
    async def save_result(
        self,
        job: Job,
        stdout: str,
        stderr: str,
        exit_code: int,
        status: JobStatusEnum
    ):
        job.stdout = stdout
        job.stderr = stderr
        job.exit_code = exit_code
        job.status = status
        job.finished_at = datetime.now(timezone.utc)
        await self.db.commit()