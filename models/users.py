from pydantic import BaseModel

class User(BaseModel):
    name:str
    email:str
    accountno:str
    phoneNum:str
    isEmailVerified:bool
    isPhoneNumVerified:bool
    isTelegramVerified:bool
    telegramChatId:int