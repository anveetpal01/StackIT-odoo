from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas, auth, utils

router = APIRouter(prefix="/answers", tags=["answers"])

@router.post("/", response_model=schemas.Answer)
def create_answer(answer: schemas.AnswerCreate, question_id: int, db: Session = Depends(utils.get_db), current_user: models.User = Depends(auth.get_current_user)):
    db_answer = models.Answer(
        content=answer.content,
        question_id=question_id,
        owner_id=current_user.id
    )
    db.add(db_answer)
    db.commit()
    utils.notify_mentions(db, answer.content, current_user.id)
    question = db.query(models.Question).filter(models.Question.id == db_answer.question_id).first()
    if question and question.owner_id != current_user.id:
        utils.create_notification(db, question.owner_id, f"Your question received a new answer.")

    db.refresh(db_answer)
    return db_answer


@router.post("/{answer_id}/accept", response_model=schemas.Answer)
def accept_answer(answer_id: int, db: Session = Depends(utils.get_db), current_user: models.User = Depends(auth.active_user_required)):
    answer = db.query(models.Answer).filter(models.Answer.id == answer_id).first()
    if not answer:
        raise HTTPException(status_code=404, detail="Answer not found")
    question = db.query(models.Question).filter(models.Question.id == answer.question_id).first()
    if question.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Only the question owner can accept an answer")
    # Unaccept all answers for this question
    db.query(models.Answer).filter(models.Answer.question_id == question.id).update({"is_accepted": False})
    answer.is_accepted = True
    db.commit()
    db.refresh(answer)
    return answer
