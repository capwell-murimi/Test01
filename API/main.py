from fastapi import FastAPI, Depends, HTTPException, status

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from schemas import UserCreate, UserResponse, UserBase
from crud import create_user, authenticate_user, get_users, update_users, delete_users, create_table, get_user_by_email
from auth import create_access_data, verify_access_token


app = FastAPI()

create_table()

oath2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(token: str = Depends(oath2_scheme)):
    email = verify_access_token(token)

    if email is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    user = get_user_by_email(email)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_UNAUTHORIZED, detail="user not found")
    return user

@app.post("/register", response_model=UserResponse)
def register(user: UserCreate):
    return create_user(user)


@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    access_token = create_access_data(data={"sub": user["email"]})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users", response_model = list[UserResponse])
def list_users(current_user: dict = Depends(get_current_user)):
    return get_users()

@app.put("/users/{id}")
def update_user_data(id: int, user: UserBase, current_user: dict = Depends(get_current_user)):
    updated = update_users(id,user.name,user.email,user.age)

    if not updated:
        raise HTTPException(status_code=404, detail="User not found")
    return updated

@app.delete("/users/{id}")
def delete_user_data(id: int, current_user: dict = Depends(get_current_user)):
    deleted = delete_users(id)

    if not deleted:
        raise HTTPException(status_code=404, detail="User not found mamen!")
    
    return {"detail": "User deleted successfully"}

