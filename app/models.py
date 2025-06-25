from sqlalchemy import Column, Integer, String, Text, JSON
from pgvector.sqlalchemy import Vector
from app.db import Base

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), unique=True, nullable=False)
    description = Column(Text, nullable=False)
    tools = Column(JSON, nullable=False)
    team_members = Column(JSON, nullable=False)
    supervisor = Column(String(100), nullable=False)
    year = Column(Integer, nullable=False)
    embedding = Column(Vector(768), nullable=False)

    