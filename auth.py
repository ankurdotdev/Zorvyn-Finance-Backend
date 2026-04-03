from fastapi import Header, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
import models

def get_current_user(x_user_id: int = Header(...), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == x_user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized: User not found")
    if user.status == models.UserStatus.INACTIVE:
        raise HTTPException(status_code=403, detail="Forbidden: User is inactive")
    return user

def check_role(roles: list):
    def role_checker(user: models.User = Depends(get_current_user)):
        if user.role not in roles:
            raise HTTPException(
                status_code=403, 
                detail=f"Forbidden: {user.role} does not have required permissions"
            )
        return user
    return role_checker

# Pre-defined dependencies for common role checks
require_admin = check_role([models.UserRole.ADMIN])
require_analyst_or_admin = check_role([models.UserRole.ADMIN, models.UserRole.ANALYST])
require_any_role = check_role([models.UserRole.ADMIN, models.UserRole.ANALYST, models.UserRole.VIEWER])
