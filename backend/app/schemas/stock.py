from pydantic import BaseModel

# 這是給前端看的資料格式 (DTO)
class StockResponse(BaseModel):
    code: str
    name: str

    class Config:
        from_attributes = True