from typing import List, Union
from fastapi import FastAPI, HTTPException, Query, Path as PathParam, Depends, status, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, Field, EmailStr
from datetime import datetime, timedelta
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path as FilePath

app = FastAPI(title="Enhanced FastAPI Demo",
             description="A demo showing common FastAPI features",
             version="1.0.0")

templates = Jinja2Templates(directory="templates")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Token settings
ACCESS_TOKEN_EXPIRE_MINUTES = 1440  # 24 hours
active_tokens = {}  # Store active tokens with their expiration time

# Models
class UserBase(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)

class UserCreate(UserBase):
    password: str = Field(..., min_length=6)

class User(UserBase):
    id: int
    created_at: datetime
    is_active: bool = True

    class Config:
        from_attributes = True

class Item(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    description: Union[str, None] = Field(None, max_length=1000)
    price: float = Field(..., gt=0)
    tags: List[str] = []
    is_offer: bool = False

class ItemResponse(Item):
    id: int

# Mock databases
public_items_db = {
    1: {
        "id": 1,
        "name": "Public Demo Item",
        "description": "This item is publicly viewable",
        "price": 19.99,
        "tags": ["public", "demo"],
        "is_offer": True
    },
    2: {
        "id": 2,
        "name": "Free Sample",
        "description": "Another publicly available item",
        "price": 0.00,
        "tags": ["public", "free"],
        "is_offer": False
    }
}

items_db = {
    1: {
        "id": 1,
        "name": "Laptop",
        "description": "High-performance laptop with 16GB RAM",
        "price": 999.99,
        "tags": ["electronics", "computers"],
        "is_offer": False
    },
    2: {
        "id": 2,
        "name": "Smartphone",
        "description": "Latest model with 5G support",
        "price": 699.99,
        "tags": ["electronics", "mobile"],
        "is_offer": True
    },
    3: {
        "id": 3,
        "name": "Coffee Maker",
        "description": "Automatic coffee maker with timer",
        "price": 79.99,
        "tags": ["appliances", "kitchen"],
        "is_offer": False
    }
}

users_db = {
    1: {
        "id": 1,
        "email": "testuser@example.com",
        "username": "testuser",
        "password": "testpass",  # In real apps, this should be hashed
        "created_at": datetime.now(),
        "is_active": True
    }
}

# Authentication functions
def create_access_token(data: dict):
    expires = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    token = f"user_{data['username']}_{datetime.utcnow().timestamp()}"  # Simple token generation
    active_tokens[token] = expires
    return {"access_token": token, "expires_at": expires}

async def get_current_user(token: str = Depends(oauth2_scheme)):
    if token not in active_tokens:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )
    
    if datetime.utcnow() > active_tokens[token]:
        del active_tokens[token]
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired"
        )
    
    # Extract username from token
    username = token.split('_')[1]
    user = next((u for u in users_db.values() if u["username"] == username), None)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Routes
@app.get("/api")
async def read_api_status():
    return {"message": "Welcome to Enhanced FastAPI Demo"}

@app.get("/", response_class=HTMLResponse)
async def get_tutorial(request: Request):
    return templates.TemplateResponse("fastapi_tutorial.html", {"request": request})

@app.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = next((u for u in users_db.values() if u["username"] == form_data.username), None)
    if not user or form_data.password != user["password"]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    return create_access_token({"username": user["username"]})

@app.post("/token/revoke")
async def revoke_token(token: str = Depends(oauth2_scheme)):
    if token in active_tokens:
        del active_tokens[token]
        return {"message": "Token revoked successfully"}
    raise HTTPException(status_code=404, detail="Token not found")

@app.get("/items", response_model=List[ItemResponse])
async def list_items(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    current_user: dict = Depends(get_current_user)
):
    return list(items_db.values())[skip : skip + limit]

@app.get("/items/{item_id}")
async def read_item(item_id: int, current_user: dict = Depends(get_current_user)):
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return items_db[item_id]

@app.post("/items", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
async def create_item(
    item: Item,
    current_user: dict = Depends(get_current_user)
):
    item_id = len(items_db) + 1
    item_dict = item.model_dump()
    item_dict["id"] = item_id
    items_db[item_id] = item_dict
    return item_dict

@app.put("/items/{item_id}", response_model=ItemResponse)
async def update_item(
    item_id: int,
    item: Item,
    current_user: dict = Depends(get_current_user)
):
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    item_dict = item.model_dump()
    item_dict["id"] = item_id
    items_db[item_id] = item_dict
    return item_dict

@app.patch("/items/{item_id}", response_model=ItemResponse)
async def patch_item(
    item_id: int,
    item: Item,
    current_user: dict = Depends(get_current_user)
):
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    stored_item = dict(items_db[item_id])
    stored_item.update(item.model_dump(exclude_unset=True))
    items_db[item_id] = stored_item
    return stored_item

@app.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(
    item_id: int,
    current_user: dict = Depends(get_current_user)
):
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    del items_db[item_id]
    return None

@app.get("/public/items")
async def list_public_items(skip: int = 0, limit: int = 10):
    items = list(public_items_db.values())[skip : skip + limit]
    return items

@app.get("/public/items/{item_id}")
async def read_public_item(item_id: int):
    if item_id not in public_items_db:
        raise HTTPException(status_code=404, detail="Public item not found")
    return public_items_db[item_id]