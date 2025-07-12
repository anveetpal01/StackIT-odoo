from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas, auth, utils

router = APIRouter(prefix="/admin", tags=["admin"])

@router.post("/ban_user/{user_id}")
def ban_user(user_id: int, db: Session = Depends(utils.get_db), current_admin: models.User = Depends(auth.admin_required)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.is_active = False
    db.commit()
    return {"detail": "User banned"}

@router.delete("/reject_question/{question_id}")
def reject_question(question_id: int, db: Session = Depends(utils.get_db), current_admin: models.User = Depends(auth.admin_required)):
    question = db.query(models.Question).filter(models.Question.id == question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    db.delete(question)
    db.commit()
    return {"detail": "Question rejected"}

@router.delete("/reject_answer/{answer_id}")
def reject_answer(answer_id: int, db: Session = Depends(utils.get_db), current_admin: models.User = Depends(auth.admin_required)):
    answer = db.query(models.Answer).filter(models.Answer.id == answer_id).first()
    if not answer:
        raise HTTPException(status_code=404, detail="Answer not found")
    db.delete(answer)
    db.commit()
    return {"detail": "Answer rejected"}

@router.post("/send_message", response_model=schemas.PlatformMessage)
def send_platform_message(msg: schemas.PlatformMessageCreate, db: Session = Depends(utils.get_db), current_admin: models.User = Depends(auth.admin_required)):
    db_msg = models.PlatformMessage(message=msg.message)
    db.add(db_msg)
    db.commit()
    db.refresh(db_msg)
    return db_msg

@router.get("/user_activity")
def user_activity(db: Session = Depends(utils.get_db), current_admin: models.User = Depends(auth.admin_required)):
    users = db.query(models.User).all()
    questions = db.query(models.Question).all()
    answers = db.query(models.Answer).all()
    return {
        "total_users": len(users),
        "total_questions": len(questions),
        "total_answers": len(answers),
    }
