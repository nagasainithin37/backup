from pydantic import BaseModel

class Transaction(BaseModel):
    accountno:str
    timestamp:int