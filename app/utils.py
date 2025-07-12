from sqlalchemy.orm import Session

def get_db():
    from .database import SessionLocal
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_notification(db: Session, user_id: int, message: str):
    from .models import Notification
    notification = Notification(user_id=user_id, message=message)
    db.add(notification)
    db.commit()
    db.refresh(notification)
    return notification
import re
def notify_mentions(db: Session, text: str, sender_id: int):
    from .models import User
    usernames = set(re.findall(r'@(\w+)', text))
    for username in usernames:
        user = db.query(User).filter(User.username == username).first()
        if user and user.id != sender_id:
            create_notification(db, user.id, f"You were mentioned in a post.")
