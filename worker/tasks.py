from core.celery_app import celery_app
from service.executer import CodeExecuter
from service.job_repository import JobRepository
import asyncio
from core.database import AsyncSessionLocal
from models.job import JobStatusEnum
from datetime import datetime, timedelta, timezone
from models.job import Job
from sqlalchemy import delete

@celery_app.task(name="execute_code_task")
def execute_code_task(job_id: str):
    asyncio.run(_execute_code_task(job_id))


async def _execute_code_task(job_id: str):
    async with AsyncSessionLocal() as db:
        repo = JobRepository(db)
        executor = CodeExecuter()
        
        job = await repo.get_job_by_id(job_id)
        if job is None:
            return
        
        await repo.mark_runnig(job)
        
        result = await asyncio.to_thread(executor.run, job.language, job.code)
        
        await repo.save_result(
            job,
            stdout=result["stdout"],
            stderr=result["stderr"],
            exit_code=result["exit_code"],
            status=JobStatusEnum(result["status"])
        )
        
        
@celery_app.task(name="cleanup_old_jobs")
def cleanup_old_jobs():
    asyncio.run(_cleanup_old_jobs())
    
async def _cleanup_old_jobs():
    async with AsyncSessionLocal() as db:
        cutoff = datetime.now(timezone.utc) - timedelta(days=1)
        await db.execute(delete(Job).where(Job.created_at < cutoff))
        await db.commit()