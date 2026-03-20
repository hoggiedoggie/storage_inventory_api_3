from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.user import UserCreate, UserRead
from app.services.auth import auth_service
from app.core.security import security_helper

router = APIRouter()

@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """Creates a new account in the database."""
    return auth_service.register_new_user(db, user_data)

@router.post("/login")
def login(
    response: Response, 
    user_data: UserCreate, 
    db: Session = Depends(get_db)
):
    """Logs the user in and sets an HttpOnly cookie with JWT."""
    user = auth_service.authenticate_user(db, user_data.email, user_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Invalid email or password"
        )
    
    # Generate the token
    token = security_helper.create_access_token(data={"sub": str(user.id)})
    
    # Set the cookie according to security requirements
    response.set_cookie(
        key="access_token", 
        value=f"Bearer {token}", 
        httponly=True,  # Protects against XSS
        max_age=3600,   # 1 hour
        samesite="lax", # Protects against CSRF
        secure=False    # Set to True if using HTTPS
    )
    
    return {"status": "success", "message": "User logged in"}

@router.post("/logout")
def logout(response: Response):
    """Logs the user out by deleting the session cookie."""
    response.delete_cookie("access_token")
    return {"message": "Logged out successfully"}