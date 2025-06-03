from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.dialects.postgresql import UUID, TIMESTAMP
from sqlalchemy_utils import ChoiceType
from enum import Enum
import uuid
from datetime import datetime, timezone

Base = declarative_base()

# ----------------------------
# ----- Serializer Class -----


class CustomSerializerMixin:
    def to_dict(self, include: set[str] = set(), exclude: set[str] = set()):
        result = {}
        for column in self.__table__.columns:
            if (include and column.name not in include) or (column.name in exclude):
                continue
            column_name = column.name
            column_value = getattr(self, column_name)
            if isinstance(column_value, uuid.UUID):
                result[column_name] = str(column_value)
            elif isinstance(column_value, datetime):
                result[column_name] = column_value.isoformat()
            elif isinstance(column_value, Enum):
                result[column_name] = column_value.value
            else:
                result[column_name] = column_value
        return result


# ------------------------
# ----- User Schemas -----


class User(Base, CustomSerializerMixin):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String(20), unique=True, nullable=False)
    email = Column(String(254), unique=True)
    password = Column(String(100), nullable=False)
    is_staff = Column(Boolean, default=False)
    is_verified = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP(timezone=True), default=lambda: datetime.now(timezone.utc))
    orders = relationship(
        "Order",
        back_populates="user",
        cascade="all, delete-orphan",
    )  # user relation under Order class (one to many)

    def __repr__(self):
        return f"<User {self.username}>"


# -------------------------
# ----- Order Schemas -----


class OrderStatuses(Enum):
    RECEIVED = "received"
    PREPARED = "prepared"
    IN_TRANSIT = "in-transit"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


class PizzaSizes(Enum):
    SMALL = "small"
    MEDIUM = "medium"
    LARGE = "large"
    EXTRA_LARGE = "extra-large"


class Order(Base, CustomSerializerMixin):
    __tablename__ = "orders"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    quantity = Column(Integer, nullable=False)
    order_status = Column(ChoiceType(choices=OrderStatuses, impl=String()), default=OrderStatuses.RECEIVED)
    pizza_size = Column(ChoiceType(choices=PizzaSizes, impl=String()), default=PizzaSizes.SMALL)
    user_id = Column(UUID(as_uuid=True), ForeignKey(column="users.id", ondelete="CASCADE"))
    time_of_order = Column(TIMESTAMP(timezone=True), default=lambda: datetime.now(timezone.utc))
    user = relationship(
        "User",
        back_populates="orders",
    )  # orders relation under User class (many to one)

    def __repr__(self):
        return f"<Order {self.id}>"
