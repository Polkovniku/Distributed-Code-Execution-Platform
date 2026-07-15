from sqlalchemy.orm import Mapped, mapped_column
import uuid
from sqlalchemy import UUID, DateTime, String, func, ForeignKey, Enum
from datetime import datetime
from core.database import Base
import enum

class JobStatusEnum(str, enum.Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    FINISHED = "FINISHED"
    FAILED = "FAILED"
    TIMEOUT = "TIMEOUT"

class Job(Base):
    __tablename__="jobs"
    
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    language: Mapped[str] = mapped_column(String(20), nullable=False)
    code: Mapped[str]
    status: Mapped[JobStatusEnum] = mapped_column(Enum(JobStatusEnum, name="jobstatusenum"), default=JobStatusEnum.PENDING) 
    stdout: Mapped[str | None] = mapped_column(nullable=True) #результат работы кода
    stderr: Mapped[str | None] = mapped_column(nullable=True) #ошибки
    exit_code: Mapped[int | None] = mapped_column(nullable=True) #код завершения программы
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    started_at: Mapped[datetime | None] = mapped_column(nullable=True)
    finished_at: Mapped[datetime | None] = mapped_column(nullable=True)