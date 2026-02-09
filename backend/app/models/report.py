from sqlalchemy import Column, Integer, String, DateTime, Text, SmallInteger
from sqlalchemy.dialects.postgresql import JSONB
from app.models.base import Base
from datetime import datetime


class ReportTemplate(Base):
    __tablename__ = "report_template"

    id = Column(Integer, primary_key=True, comment="模板ID")
    template_name = Column(String(100), nullable=False, comment="模板名称")
    dept = Column(String(50), comment="适用部门")
    role = Column(String(50), comment="适用角色")
    template_type = Column(String(20), nullable=False, comment="模板类型")
    content = Column(JSONB, nullable=False, comment="模板内容配置")
    file_path = Column(Text, comment="模板文件路径")
    preview_image = Column(Text, comment="预览图片路径")
    is_default = Column(SmallInteger, default=0, comment="是否默认模板：0-否，1-是")
    status = Column(SmallInteger, default=1, comment="模板状态：1-启用，0-禁用")
    create_time = Column(DateTime, default=datetime.utcnow, comment="创建时间")
    update_time = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment="更新时间")
