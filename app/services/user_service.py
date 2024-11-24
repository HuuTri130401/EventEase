from fastapi import Depends, HTTPException, logger
from app.repositories.user_repository import UserRepository, get_user_repository
from app.schemas.sche_user import UserRegisterRequest

class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def get_user_by_username(self, username: str):
        user = self.user_repository.get_user_by_username(username)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        if user.is_deleted == True or user.status == "inactive":
            raise HTTPException(status_code=404, detail="User is deleted or inactive")
        return user
    
    def get_user_by_id(self, id: int):
        user = self.user_repository.get_user_by_id(id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        if user.is_deleted == True or user.status == "inactive":
            raise HTTPException(status_code=404, detail="User is deleted or inactive")
        return user
    
    def get_all_user(self):
        users = self.user_repository.get_all_user()
        if not users:
            return {"message": "List user is empty"}
        return users
    
    def create_user(self, data: UserRegisterRequest):
        exist_user = self.user_repository.get_user_by_email(data.email)
        if not exist_user:
            new_user = self.user_repository.create_user(data)
            return new_user
        raise HTTPException(status_code=400, detail='Email already exist!')

def get_user_service(user_repository: UserRepository = Depends(get_user_repository)):
    return UserService(user_repository)