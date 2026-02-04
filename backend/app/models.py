# app/models.py
from sqlalchemy import Column, String, Date, Text, Numeric
from sqlalchemy.dialects.postgresql import UUID, JSONB
import uuid
from app.database import Base

class WorkLog(Base):
    __tablename__ = "work_log"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_name = Column(String(50))
    work_date = Column(Date)
    work_hours = Column(Numeric(5, 2))
    content = Column(Text)
    extra_data = Column(JSONB)