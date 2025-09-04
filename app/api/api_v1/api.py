from fastapi import APIRouter

# Import routers from endpoints
from app.api.api_v1.endpoints import auth, users, tickets, tasks, comments, projects

api_router = APIRouter()

# Include routers for different endpoints
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(tickets.router, prefix="/tickets", tags=["tickets"])

api_router.include_router(tasks.router, prefix="/tasks", tags=["tasks"])
api_router.include_router(comments.router, prefix="/comments", tags=["comments"])
api_router.include_router(projects.router, prefix="/projects", tags=["projects"])