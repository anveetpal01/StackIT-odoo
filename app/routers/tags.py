from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas, utils

router = APIRouter(prefix="/tags", tags=["tags"])

@router.post("/", response_model=schemas.Tag)
def create_tag(tag: schemas.Tag, db: Session = Depends(utils.get_db)):
    db_tag = models.Tag(name=tag.name)
    db.add(db_tag)
    db.commit()
    db.refresh(db_tag)
    return db_tag

@router.get("/", response_model=List[schemas.Tag])
def get_tags(db: Session = Depends(utils.get_db)):
    return db.query(models.Tag).all()
