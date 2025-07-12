from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Boolean, Table, UniqueConstraint
from sqlalchemy.orm import relationship
from .database import Base
import datetime

# Association Table for Many-to-Many (Questions <-> Tags)
question_tags = Table(
    'question_tags', Base.metadata,
    Column('question_id', Integer, ForeignKey('questions.id')),
    Column('tag_id', Integer, ForeignKey('tags.id'))
)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    email = Column(String(100), unique=True, index=True)
    hashed_password = Column(String(255))
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    questions = relationship("Question", back_populates="owner")
    answers = relationship("Answer", back_populates="owner")

class Question(Base):
    __tablename__ = "questions"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255))
    description = Column(Text)
    owner_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    tags = relationship("Tag", secondary=question_tags, back_populates="questions")
    owner = relationship("User", back_populates="questions")
    answers = relationship("Answer", back_populates="question")

class Answer(Base):
    __tablename__ = "answers"
    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text)
    question_id = Column(Integer, ForeignKey("questions.id"))
    owner_id = Column(Integer, ForeignKey("users.id"))
    is_accepted = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    question = relationship("Question", back_populates="answers")
    owner = relationship("User", back_populates="answers")

class Tag(Base):
    __tablename__ = "tags"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, index=True)
    questions = relationship("Question", secondary=question_tags, back_populates="tags")

class Notification(Base):
    __tablename__ = "notifications"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    message = Column(String(255))
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


class Vote(Base):
    __tablename__ = "votes"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    answer_id = Column(Integer, ForeignKey("answers.id"))
    value = Column(Integer)  # 1 for upvote, -1 for downvote
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    __table_args__ = ( 
        # Prevent multiple votes by the same user on the same answer
        UniqueConstraint('user_id', 'answer_id', name='unique_user_answer_vote'),
    )

class Comment(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text)
    answer_id = Column(Integer, ForeignKey("answers.id"))
    owner_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


class PlatformMessage(Base):
    __tablename__ = "platform_messages"
    id = Column(Integer, primary_key=True, index=True)
    message = Column(String(255))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
