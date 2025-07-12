from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas, auth, utils

router = APIRouter(prefix="/votes", tags=["votes"])

@router.post("/", response_model=schemas.VoteOut)
def vote(vote: schemas.VoteCreate, db: Session = Depends(utils.get_db), current_user: models.User = Depends(auth.get_current_user)):
    # Prevent duplicate votes
    db_vote = db.query(models.Vote).filter(
        models.Vote.user_id == current_user.id,
        models.Vote.answer_id == vote.answer_id
    ).first()
    if db_vote:
        if db_vote.value == vote.value:
            raise HTTPException(status_code=400, detail="Already voted")
        db_vote.value = vote.value  # Change vote
    else:
        db_vote = models.Vote(user_id=current_user.id, answer_id=vote.answer_id, value=vote.value)
        db.add(db_vote)
    db.commit()
    # Return total votes for the answer
    total = db.query(models.Vote).filter(models.Vote.answer_id == vote.answer_id).with_entities(models.Vote.value).all()
    votes = sum([v[0] for v in total])
    return schemas.VoteOut(answer_id=vote.answer_id, votes=votes)
