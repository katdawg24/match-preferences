from sqlalchemy import Column, Date, DateTime, ForeignKey, Integer, String, Boolean, Enum as SQLAlchemyEnum, func
from sqlalchemy.orm import relationship
from .database import Base
from enum import Enum
from sqlalchemy import Float
from sqlalchemy.sql import expression

class UserAccount(Base):
    __tablename__ = "user_accounts"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    hashed_password = Column(String)
    name = Column(String)
    is_admin = Column(Boolean, server_default=expression.false())
    is_deleted = Column(Boolean, server_default=expression.false())

    # Relationships
    group_members = relationship("GroupMember", back_populates="account")

class Group(Base):
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    description = Column(String)
    password = Column(String)
    num_preferences = Column(Integer)
    direct_matches = Column(Boolean, server_default=expression.false())
    additional_prefs_allowed = Column(Boolean, server_default=expression.false())
    match_complete = Column(Boolean, server_default=expression.false())
    match_date = Column(DateTime, server_default=func.now())
    is_deleted = Column(Boolean, server_default=expression.false())

    # Relationships
    members = relationship("GroupMember", back_populates="group")
    tasks = relationship("Task", back_populates="group")

class GroupMember(Base):
    __tablename__ = "group_members"

    id = Column(Integer, primary_key=True, index=True)
    group_id = Column(Integer, ForeignKey("groups.id"))
    group_member_id = Column(Integer, nullable=True)
    account_id = Column(Integer, ForeignKey("user_accounts.id"))
    is_deleted = Column(Boolean, server_default=expression.false())

    group = relationship("Group", back_populates="members")
    preferences = relationship("TaskPreference", back_populates="group_member")
    matches = relationship("Match", back_populates="group_member")
    account = relationship("UserAccount", back_populates="group_members")

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    group_id = Column(Integer, ForeignKey("groups.id"))
    name = Column(String)
    description = Column(String)
    group_task_id = Column(Integer)
    min_assignment_count = Column(Integer)
    max_assignment_count = Column(Integer)
    is_deleted = Column(Boolean, server_default=expression.false())

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
    member_id = Column(Integer, ForeignKey("group_members.id"))
    match_date = Column(DateTime, server_default=func.now())
    is_deleted = Column(Boolean, server_default=expression.false())

    task = relationship("Task", back_populates="matches")
    group_member = relationship("GroupMember", back_populates="matches")