import sqlalchemy
from sqlalchemy import DateTime

from main.constants import *
from main.database_set import metadata

users = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("username", sqlalchemy.String, nullable=True),
    sqlalchemy.Column("full_name", sqlalchemy.String),
    sqlalchemy.Column("weight", sqlalchemy.Float),
    sqlalchemy.Column("chat_id", sqlalchemy.BigInteger),
    sqlalchemy.Column("phone_number", sqlalchemy.String),
    sqlalchemy.Column("status", sqlalchemy.Enum(UserStatus), default=UserStatus.active),
    sqlalchemy.Column('created_at', DateTime(timezone=True), nullable=True),
    sqlalchemy.Column('updated_at', DateTime(timezone=True), nullable=True)
)


referrals = sqlalchemy.Table(
    "referrals",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("referral_from", sqlalchemy.BigInteger),
    sqlalchemy.Column("referral_to", sqlalchemy.BigInteger),
)
