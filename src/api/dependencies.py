# src/api/dependencies.py

from fastapi import Request, HTTPException, status
from typing import Optional

def get_current_user_id(request: Request) -> int:
   
    user_id: Optional[int] = getattr(request.state, "user_id", None)
    
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="User ID not found in request state. Authentication check failed."
        )
        
    return user_id