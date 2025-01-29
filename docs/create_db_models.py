# using resolved_model self.resolved_model FIXME
# created from response, to create create_db_models.sqlite, with test data
#    that is used to create project
# should run without error in manager 
#    if not, check for decimal, indent, or import issues

import decimal
import logging
import sqlalchemy
from sqlalchemy.sql import func 
from decimal import Decimal
from logic_bank.logic_bank import Rule
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, Date, DateTime, Numeric, Boolean, Text, DECIMAL
from sqlalchemy.types import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from datetime import date   
from datetime import datetime
from typing import List


logging.getLogger('sqlalchemy.engine.Engine').disabled = True  # remove for additional logging

Base = declarative_base()  # from system/genai/create_db_models_inserts/create_db_models_prefix.py


from sqlalchemy.dialects.sqlite import *

class User(Base):
    """description: Represents a system user."""
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    email = Column(String)
    created_at = Column(DateTime, default=datetime.now())
    profile_id = Column(Integer, ForeignKey('profile.id'))

class Profile(Base):
    """description: Stores additional info about the user."""
    __tablename__ = 'profile'
    id = Column(Integer, primary_key=True, autoincrement=True)
    bio = Column(String)
    date_of_birth = Column(Date)
    user_id = Column(Integer, ForeignKey('user.id'))

class Role(Base):
    """description: Defines different roles within the system."""
    __tablename__ = 'role'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    description = Column(String)

class UserRole(Base):
    """description: Associative table connecting users with roles."""
    __tablename__ = 'user_role'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    role_id = Column(Integer, ForeignKey('role.id'))

class Asset(Base):
    """description: Represents assets owned by users."""
    __tablename__ = 'asset'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    description = Column(String)
    owner_id = Column(Integer, ForeignKey('user.id'))

class AuditLog(Base):
    """description: Keeps track of user activities."""
    __tablename__ = 'audit_log'
    id = Column(Integer, primary_key=True, autoincrement=True)
    action = Column(String)
    user_id = Column(Integer, ForeignKey('user.id'))
    timestamp = Column(DateTime, default=datetime.now())

class Configuration(Base):
    """description: Stores various system configuration settings."""
    __tablename__ = 'configuration'
    id = Column(Integer, primary_key=True, autoincrement=True)
    key = Column(String)
    value = Column(String)

class Task(Base):
    """description: Represents tasks assigned to users."""
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    description = Column(String)
    assigned_to_id = Column(Integer, ForeignKey('user.id'))
    status = Column(String)

class Team(Base):
    """description: Represents a team within the system."""
    __tablename__ = 'team'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    description = Column(String)

class UserTeam(Base):
    """description: Associative table connecting users with teams."""
    __tablename__ = 'user_team'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    team_id = Column(Integer, ForeignKey('team.id'))

class Department(Base):
    """description: Defines departments within the company."""
    __tablename__ = 'department'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    head_id = Column(Integer, ForeignKey('user.id'))

class Project(Base):
    """description: Represents projects within the organization."""
    __tablename__ = 'project'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    description = Column(String)
    lead_id = Column(Integer, ForeignKey('user.id'))


# end of model classes


try:
    
    
    # ALS/GenAI: Create an SQLite database
    import os
    mgr_db_loc = True
    if mgr_db_loc:
        print(f'creating in manager: sqlite:///system/genai/temp/create_db_models.sqlite')
        engine = create_engine('sqlite:///system/genai/temp/create_db_models.sqlite')
    else:
        current_file_path = os.path.dirname(__file__)
        print(f'creating at current_file_path: {current_file_path}')
        engine = create_engine(f'sqlite:///{current_file_path}/create_db_models.sqlite')
    Base.metadata.create_all(engine)
    
    
    Session = sessionmaker(bind=engine)
    session = Session()
    
    # ALS/GenAI: Prepare for sample data
    
    
    session.commit()
    user1 = User(name="John Doe", email="john.doe@example.com", created_at=datetime(2021, 1, 1), profile_id=1)
    user2 = User(name="Jane Smith", email="jane.smith@example.com", created_at=datetime(2021, 2, 15), profile_id=2)
    user3 = User(name="Alice Jones", email="alice.jones@example.com", created_at=datetime(2021, 3, 30), profile_id=3)
    user4 = User(name="Bob Brown", email="bob.brown@example.com", created_at=datetime(2021, 4, 20), profile_id=4)
    
    
    
    session.add_all([user1, user2, user3, user4])
    session.commit()
    # end of test data
    
    
except Exception as exc:
    print(f'Test Data Error: {exc}')
