from fastapi import FastAPI
from routers.user import router as auth_router
from routers.job import router as job_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(job_router)


