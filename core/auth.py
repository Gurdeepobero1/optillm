from core.db import SessionLocal, User

def get_user(api_key: str):
    db = SessionLocal()
    user = db.query(User).filter(User.api_key == api_key).first()
    db.close()
    return user