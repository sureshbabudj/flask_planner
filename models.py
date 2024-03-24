from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Table, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timezone

Base = declarative_base()

# Association table for the many-to-many relationship between users and plans
user_plan_association = Table('user_plan_association', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('plan_id', Integer, ForeignKey('plans.id'))
)

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    _password_hash = Column(String(128))  # Store the hash of the password

    # Property to set password hash
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    # Method to set password hash
    @password.setter
    def password(self, password):
        self._password_hash = generate_password_hash(password)

    # Method to check password hash
    def verify_password(self, password):
        return check_password_hash(self._password_hash, password)

    created_plans = relationship('Plan', back_populates='creator')
    participated_plans = relationship('Plan', secondary=user_plan_association, back_populates='participants')

class Plan(Base):
    __tablename__ = 'plans'
    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    summary = Column(String(250))
    link = Column(String(250))
    duration = Column(Integer)  # Duration in minutes
    start_time = Column(DateTime, nullable=False, default=datetime.now(timezone.utc))
    end_time = Column(DateTime, nullable=False, default=datetime.now(timezone.utc))
    creator_id = Column(Integer, ForeignKey('users.id'))
    creator = relationship('User', back_populates='created_plans')
    participants = relationship('User', secondary=user_plan_association, back_populates='participated_plans')

    # Ensure that the end_time is after the start_time
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        assert self.end_time > self.start_time, "end_time must be after start_time"
