from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class Webhook(Base):
    __tablename__="webhooks"
    id=Column(Integer,primary_key=True,index=True)
    user_id=Column(Integer,ForeignKey("users.id"),nullable=False)
    url=Column(String(500),nullable=False)
    secret=Column(String(100),nullable=False)
    is_active=Column(Boolean, default=True)
    events=Column(String(200),nullable=False)
    created_at=Column(DateTime,default=datetime.utcnow)


    user=relationship("User",back_populates="webhooks")

    deliveries=relationship("WebhookDelivery",back_populates="webhook")

    def __repr__(self):
        return f"<Webhook {self.url}>"
    

class WebhookDelivery(Base):
    __tablename__="webhook_deliveries"

    id=Column(Integer,primary_key=True,index=True)
    webhook_id=Column(Integer,ForeignKey("webhooks.id"),nullable=False)
    delivery_id=Column(String(100),unique=True,nullable=False)
    event_type=Column(String(50),nullable=False)
    payload=Column(Text,nullable=False)
    status_code=Column(Integer)
    success=Column(Boolean,default=False)
    delivered_at= Column(DateTime,default=datetime.utcnow)

    webhook=relationship("Webhook",back_populates="deliveries")

    def __repr__(self):
        return f"<WebhookDelivery {self.event_type} {self.success}>"