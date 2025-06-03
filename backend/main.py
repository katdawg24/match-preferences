
# Create database tables on application startup.
from contextlib import asynccontextmanager
from datetime import datetime, timedelta, timezone
import logging
import os
from typing import Annotated, Optional
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Depends, FastAPI, HTTPException, status
from jose import JWTError
import jwt
from jwt import InvalidTokenError
from sqlalchemy import delete, null, select, text
from schemas import GroupMemberToReturn, Token, TokenData, UserToReturn
from db.database import Base, SessionLocal, engine, get_db
from db.models import Group, GroupMember, Task, TaskPreference, Match, UserAccount
from ManyToOneSetup import solve_assignment_with_ranges, solve_exact_assignment, solve_one_to_one
from pydantic import BaseModel
from sqlalchemy.orm import joinedload, Session
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

load_dotenv()

#Start up and shut down tasks for the FastAPI application using lifespan
@asynccontextmanager
async def lifespan(app: FastAPI):

    # Create database tables on application startup.
    Base.metadata.create_all(bind=engine)

    with SessionLocal() as session:
        has_data = session.query(Group).count() > 0 or session.query(Task).count() > 0

    if not has_data and os.getenv('SQLALCHEMY_DATABASE_URL'):
        logging.info("No data found, loading canned data...")
        dir_path = os.path.dirname(__file__)
        sql_path = os.path.join(dir_path, "db\\data.sql")
                
        with engine.begin() as conn:
            logging.info("Executing data.sql...")
            query = text(open(sql_path, "r").read())
            conn.execute(query)

    else:
        logging.info("Data already present, skipping canned-data.sql")

        

    yield
    # On application shutdown, you can add cleanup tasks if needed.


app = FastAPI(lifespan=lifespan)

origins = ["http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#region ----------------------User Auth-----------------------------
#for password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

#-----authentication values-------
SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = 30
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: Annotated[str, Depends(oauth2_scheme)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=403, detail="Token is invalid or expired")
        print(payload)
        return payload
        
    except JWTError:
        raise HTTPException(status_code=403, detail="Token is invalid or expired")


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)],
                            db: Session = Depends(get_db)):
    env = os.getenv("ENV", "production")
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    # print(f"Received token: {token}")  # Print the token
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        print("Invalid token", token)
        raise HTTPException(status_code=400, detail="token is invalid")
    

    user = db.query(UserAccount).filter(UserAccount.email == token_data.username).first()

    if user is None:
        raise HTTPException(status_code=404, detail="User user not found")
    elif user.is_deleted:
        raise HTTPException(status_code=403, detail="This account has been deleted")
    
    return user

# validate user type
def validate_admin(current_user: UserAccount):
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"General members are not authorized to perform this action",
        )
    
@app.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db)
) -> Token:
    
    #Check users
    user = db.query(UserAccount).filter(UserAccount.email == form_data.username).first()
        
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    elif not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    elif user.is_deleted:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This account has been deleted and cannot be used to log in",
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": form_data.username}, expires_delta=access_token_expires
    )

    return Token(access_token=access_token, token_type="bearer")


@app.get("/verify-token/{token}")
async def verify_user_token(token: str):
    verify_token(token=token)
    return {'message': 'Token is valid.'}

@app.get("/me", response_model=UserToReturn)
async def read_users_me(
    current_user:  Annotated[UserToReturn, Depends(get_current_user)],
):
    
    return current_user


def generate_matches(group_id: int):
    db = next(get_db())

    group = db.query(Group).filter(Group.id == group_id).first()

    num_preferences = group.__getattribute__("num_preferences")
    direct_matches = group.__getattribute__("direct_matches")

    # Fetch group members and tasks
    group_members = db.query(GroupMember).filter(GroupMember.group_id == group_id, GroupMember.is_deleted == False, GroupMember.group_member_id != null()).all()
    tasks = db.query(Task).filter(Task.group_id == group_id, Task.is_deleted == False).all()
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
    group_members = db.query(GroupMember).filter(GroupMember.group_id == group_id, GroupMember.is_deleted == False, GroupMember.group_member_id != null()).all()
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

generate_matches(1)  # Generate matches for group with ID 1 if it exists
generate_matches(2)  # Generate matches for group with ID 2 if it exists