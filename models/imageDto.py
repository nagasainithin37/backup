from pydantic import BaseModel

class imageDto(BaseModel):
    image:str
    accountno:str