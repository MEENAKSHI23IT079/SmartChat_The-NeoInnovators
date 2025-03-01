from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from pydantic import BaseModel
from bson import ObjectId

app = FastAPI()

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client.chat_db  # Database
collection = db.chats  # Collection

# Define a request model
class ChatMessage(BaseModel):
    user_id: str
    message: str

@app.post("/store_chat/")
async def store_chat(chat: ChatMessage):
    """Store chat messages in MongoDB"""
    try:
        # Insert data into MongoDB
        result = collection.insert_one(chat.dict())

        return {"status": "Saved", "chat_id": str(result.inserted_id)}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error storing chat: {str(e)}")

@app.get("/get_chat/")
async def get_chat(user_id: str):
    """Retrieve previous chat messages for a specific user"""
    try:
        # Find messages for the given user_id
        chats = collection.find({"user_id": user_id})

        messages = [{"id": str(chat["_id"]), "message": chat["message"]} for chat in chats]

        if not messages:
            return {"history": "No messages found for this user."}

        return {"history": messages}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving chats: {str(e)}")
