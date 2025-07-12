from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import Dict
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas, auth, utils


router = APIRouter(prefix="/notifications", tags=["notifications"])
active_connections: Dict[int, WebSocket] = {}

@router.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: int):
    await websocket.accept()
    active_connections[user_id] = websocket
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        active_connections.pop(user_id, None)


@router.get("/", response_model=List[schemas.Notification])
def get_notifications(db: Session = Depends(utils.get_db), current_user: models.User = Depends(auth.active_user_required)):
    return db.query(models.Notification).filter(models.Notification.user_id == current_user.id).order_by(models.Notification.created_at.desc()).all()

@router.post("/mark_read/{notification_id}")
def mark_notification_read(notification_id: int, db: Session = Depends(utils.get_db), current_user: models.User = Depends(auth.active_user_required)):
    notif = db.query(models.Notification).filter(models.Notification.id == notification_id, models.Notification.user_id == current_user.id).first()
    if notif:
        notif.is_read = True
        db.commit()
    return {"detail": "Notification marked as read"}

@router.get("/unread_count")
def unread_count(db: Session = Depends(utils.get_db), current_user: models.User = Depends(auth.active_user_required)):
    count = db.query(models.Notification).filter(models.Notification.user_id == current_user.id, models.Notification.is_read == False).count()
    return {"unread": count}
