
# Create database tables on application startup.
from db.database import Base, engine, get_db
from db.models import Group, GroupMember, Task, TaskPreference, Match
from ManyToOneSetup import solve_assignment_with_ranges, solve_exact_assignment, solve_one_to_one


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
        member_rankings = db.query(TaskPreference).filter(TaskPreference.group_member_id == member.group_member_id).all()
        sorted_rankings = sorted(member_rankings, key=lambda x: x.rank)
        task_preferences[member.group_member_id] = [task.group_task_id for task in sorted_rankings]

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

