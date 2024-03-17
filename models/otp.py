from pydantic import BaseModel

class Otp(BaseModel):
    service:str
    identifier:str
    otp:str
    timestamp:int