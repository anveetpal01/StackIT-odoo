from fastapi import FastAPI
from .routers import users, questions, answers, tags, notifications
from .database import Base, engine
from .routers import votes
 

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(users.router)
app.include_router(questions.router)
app.include_router(answers.router)
app.include_router(tags.router)
app.include_router(notifications.router)
app.include_router(votes.router)

from .routers import comments
app.include_router(comments.router)
from .routers import admin
app.include_router(admin.router)
from fastapi.staticfiles import StaticFiles
from .routers import uploads

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
app.include_router(uploads.router)
from .database import Base, engine
Base.metadata.create_all(bind=engine)


from .routers import auth as auth_router
app.include_router(auth_router.router)
