from pydantic import BaseModel

class botDto(BaseModel):
    chatId:str
    otp:str