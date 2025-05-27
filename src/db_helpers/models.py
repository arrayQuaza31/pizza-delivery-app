from enum import Enum
from db_helpers.database import Base
from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy_utils import ChoiceType


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
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
    id = Column(Integer, primary_key=True)
    quantity = Column(Integer, nullable=False)
    order_status = Column(ChoiceType(choices=OrderStatuses, impl=String()), default=OrderStatuses.PENDING)
    pizza_size = Column(ChoiceType(choices=PizzaSizes, impl=String()), default=PizzaSizes.SMALL)
    user_id = Column(Integer, ForeignKey(column='users.id'))
    user = relationship('User', back_populates='orders')  # orders relation under User class (many to one)

    def __repr__(self):
        return f"<Order {self.id}>"