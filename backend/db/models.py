from sqlalchemy import Column, Date, ForeignKey, Integer, String, Boolean, Enum as SQLAlchemyEnum
from sqlalchemy.orm import relationship
from .database import Base
from enum import Enum
from sqlalchemy import Float

class Group(Base):
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String)
    password = Column(String)
    num_preferences = Column(Integer)
    direct_matches = Column(Boolean, default=False)
    additional_prefs_allowed = Column(Boolean, default=False)
    match_complete = Column(Boolean, default=False)
    match_date = Column(Date)

    # Relationships
    members = relationship("GroupMember", back_populates="group")
    tasks = relationship("Task", back_populates="group")

class GroupMember(Base):
    __tablename__ = "group_members"

    id = Column(Integer, primary_key=True, index=True)
    group_id = Column(Integer, ForeignKey("groups.id"))
    group_member_id = Column(Integer)
    is_admin = Column(Boolean, default=False)
    name = Column(String)

    group = relationship("Group", back_populates="members")
    preferences = relationship("TaskPreference", back_populates="group_member")
    matches = relationship("Match", back_populates="group_member")

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    group_id = Column(Integer, ForeignKey("groups.id"))
    name = Column(String)
    description = Column(String)
    group_task_id = Column(Integer)
    min_assignment_count = Column(Integer)
    max_assignment_count = Column(Integer)

    group = relationship("Group", back_populates="tasks")
    preferences = relationship("TaskPreference", back_populates="task")
    matches = relationship("Match", back_populates="task")

class TaskPreference(Base):
    __tablename__ = "task_preferences"

    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey("tasks.id"))
    member_id = Column(Integer, ForeignKey("group_members.id"))
    rank = Column(Float)

    task = relationship("Task", back_populates="preferences")
    group_member = relationship("GroupMember", back_populates="preferences")

class Match(Base):
    __tablename__ = "matches"

    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey("tasks.id"))
    group_member_id = Column(Integer, ForeignKey("group_members.id"))

    task = relationship("Task", back_populates="matches")
    group_member = relationship("GroupMember", back_populates="matches")