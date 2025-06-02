
# Create database tables on application startup.
from datetime import datetime

from sqlalchemy import delete, select
from db.database import Base, engine, get_db
from db.models import Group, GroupMember, Task, TaskPreference, Match
from ManyToOneSetup import solve_assignment_with_ranges, solve_exact_assignment, solve_one_to_one
from pydantic import BaseModel
from sqlalchemy.orm import joinedload

Base.metadata.create_all(bind=engine)

def generate_matches(group_id: int):
    db = next(get_db())

    group = db.query(Group).filter(Group.id == group_id).first()

    num_preferences = group.__getattribute__("num_preferences")
    direct_matches = group.__getattribute__("direct_matches")

    # Fetch group members and tasks
    group_members = db.query(GroupMember).filter(GroupMember.group_id == group_id).all()
    tasks = db.query(Task).filter(Task.group_id == group_id).all()
    num_tasks = len(tasks)

    # Create a dictionary to store task preferences for each group member
    task_preferences = {}
    for member in group_members:
        member_rankings = db.query(TaskPreference).options(joinedload(TaskPreference.task)).filter(TaskPreference.member_id == member.id).all()
        sorted_rankings = sorted(member_rankings, key=lambda x: x.rank)
        task_preferences[member.group_member_id] = [task.task.group_task_id for task in sorted_rankings]

    if not direct_matches:
        # Create a dictionary to store the number of task assignments allowed for each task
        assignment_ranges = False
        for task in tasks:
            if task.min_assignment_count != task.max_assignment_count:
                assignment_ranges = True
                break

        if assignment_ranges:
            task_assignment_ranges = {}
            for task in tasks:
                task_assignment_ranges[task.group_task_id] = (task.min_assignment_count, task.max_assignment_count)

            results, maxsum = solve_assignment_with_ranges(num_tasks, num_preferences, task_assignment_ranges, task_preferences)
        else:
            task_assignment_nums = {}
            for task in tasks:
                task_assignment_nums[task.group_task_id] = task.min_assignment_count

            results, maxsum = solve_exact_assignment(num_tasks, num_preferences, task_assignment_nums, task_preferences)
    else:
        results, maxsum = solve_one_to_one(num_tasks, num_preferences, task_preferences)

    # Store the matches in the database
    store_matches(group_id, results)

def store_matches(group_id: int, results: dict):
    db = next(get_db())

    group = db.query(Group).filter(Group.id == group_id).first()

    # Clear existing matches
    stmt = delete(Match).where(Match.task_id.in_(
        select(Task.id).filter(Task.group_id == group_id)
    ))
    db.execute(stmt)
    db.commit()

    # Get IDs of group members and tasks
    group_members = db.query(GroupMember).filter(GroupMember.group_id == group_id).all()
    member_id_map = {member.group_member_id: member.id for member in group_members}

    tasks = db.query(Task).filter(Task.group_id == group_id).all()
    task_id_map = {task.group_task_id: task.id for task in tasks}

    for group_member_id, group_task_id in results.items():
        # Map group member and task IDs to database IDs
        member_id = member_id_map[group_member_id]
        task_id = task_id_map[group_task_id]

        # Create a new match entry
        match = Match(member_id=member_id, task_id=task_id)
        db.add(match)

    group.match_complete = True
    group.match_date = datetime.now().date()
    db.commit()

generate_matches(2)
