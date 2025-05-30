from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.dialects.postgresql import UUID, TIMESTAMP
from sqlalchemy_utils import ChoiceType
from enum import Enum
import uuid
from datetime import datetime

Base = declarative_base()

# ----------

class User(Base):
    __tablename__ = 'users'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String(20), unique=True, nullable=False)
    email = Column(String(100), unique=True)
    password = Column(Text, nullable=False)
    is_staff = Column(Boolean, default=False)
    is_active = Column(Boolean, default=False)
    orders = relationship('Order', back_populates='user')  # user relation under Order class (one to many)

    def __repr__(self):
        return f"<User {self.username}>"

# ----------

class OrderStatuses(Enum):
    PENDING = 'pending'
    IN_TRANSIT = 'in-transit'
    DELIVERED = 'delivered'

class PizzaSizes(Enum):
    SMALL = 'small'
    MEDIUM = 'medium'
    LARGE = 'large'
    EXTRA_LARGE = 'extra-large'

class Order(Base):
    __tablename__ = 'orders'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4())
    quantity = Column(Integer, nullable=False)
    order_status = Column(ChoiceType(choices=OrderStatuses, impl=String()), default=OrderStatuses.PENDING)
    pizza_size = Column(ChoiceType(choices=PizzaSizes, impl=String()), default=PizzaSizes.SMALL)
    user_id = Column(UUID(as_uuid=True), ForeignKey(column='users.id'))
    time_of_order = Column(TIMESTAMP(timezone=True), default=datetime.now)
    user = relationship('User', back_populates='orders')  # orders relation under User class (many to one)

    def __repr__(self):
        return f"<Order {self.id}>"