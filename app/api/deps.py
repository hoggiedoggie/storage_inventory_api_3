from uuid import UUID
from fastapi import Request, HTTPException, Depends, status
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.user import User
from app.core.security import SECRET_KEY, ALGORITHM

def get_current_user(
    request: Request, 
    db: Session = Depends(get_db)
) -> User:
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Not authenticated"
        )

    try:
        token_data = token.split(" ")[1] if " " in token else token
        
        payload = jwt.decode(token_data, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
            
        current_user_uuid = UUID(user_id)
        
    except (JWTError, IndexError, ValueError):
        
        raise HTTPException(status_code=401, detail="Could not validate credentials")

    user = db.query(User).filter(User.id == current_user_uuid).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user