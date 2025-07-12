from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas, auth, utils

router = APIRouter(prefix="/comments", tags=["comments"])

@router.post("/", response_model=schemas.Comment)
def create_comment(comment: schemas.CommentCreate, db: Session = Depends(utils.get_db), current_user: models.User = Depends(auth.active_user_required)):
    db_comment = models.Comment(
        answer_id=comment.answer_id,
        content=comment.content,
        owner_id=current_user.id
    )
    db.add(db_comment)
    db.commit()
    utils.notify_mentions(db, comment.content, current_user.id)
    db.refresh(db_comment)
    return db_comment

@router.get("/answer/{answer_id}", response_model=List[schemas.Comment])
def get_comments(answer_id: int, db: Session = Depends(utils.get_db)):
    return db.query(models.Comment).filter(models.Comment.answer_id == answer_id).all()
