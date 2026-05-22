from pydantic import BaseModel , HttpUrl

from datetime import datetime
from typing import Optional, List


class WebhookCreate(BaseModel):
    url:HttpUrl
    events:List[str]
    secret:str


class WebhookResponse(BaseModel):
    id:int
    url:str
    events:str
    is_active:bool
    created_at: datetime

    class Config:
        from_attributes=True



class WebhookUpdate(BaseModel):

   url: Optional[HttpUrl]=None
   events: Optional[List[str]]=None
   is_active:Optional[bool]=None


class WebhookDeliveryResponse(BaseModel):
    id:int
    webhook_id:int
    delivery_id:str
    event_type:str
    success:bool
    status_code:Optional[int]=None
    delivered_at: datetime

    class Config:
        from_attributes=True

class WebhookEventPayload(BaseModel):
    event :str
    timestamp:datetime
    data:dict