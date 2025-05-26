# This module defines the SQLAlchemy ORM model for the 'tasks' table.
# The Task class maps to the 'tasks' table with fields for id, title,
# completion status, creation time, and completion time.
# It uses SQLAlchemy types and constraints to define the schema.

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP

from .database import Base

class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    completed = Column(Boolean, server_default='False', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    completed_at = Column(TIMESTAMP(timezone=True), nullable=True)