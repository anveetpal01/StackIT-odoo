from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas, auth, utils

router = APIRouter(prefix="/questions", tags=["questions"])

@router.post("/", response_model=schemas.Question)
def create_question(question: schemas.QuestionCreate, db: Session = Depends(utils.get_db), current_user: models.User = Depends(auth.active_user_required)):
    if not question.tag_ids or len(question.tag_ids) == 0:
        raise HTTPException(status_code=400, detail="At least one tag is required")
    tags = db.query(models.Tag).filter(models.Tag.id.in_(question.tag_ids)).all()
    db_question = models.Question(
        title=question.title,
        description=question.description,
        owner_id=current_user.id,
        tags=tags
    )
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    return db_question
