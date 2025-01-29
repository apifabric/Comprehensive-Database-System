# coding: utf-8
from sqlalchemy import DECIMAL, DateTime  # API Logic Server GenAI assist
from sqlalchemy import Column, Date, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

########################################################################################################################
# Classes describing database for SqlAlchemy ORM, initially created by schema introspection.
#
# Alter this file per your database maintenance policy
#    See https://apilogicserver.github.io/Docs/Project-Rebuild/#rebuilding
#
# Created:  January 29, 2025 07:37:00
# Database: sqlite:////tmp/tmp.JSvgcVEWc7-01JJRFV5B3KJ3TE869JBHE2PMR/Comprehensive_Database_System/database/db.sqlite
# Dialect:  sqlite
#
# mypy: ignore-errors
########################################################################################################################
 
from database.system.SAFRSBaseX import SAFRSBaseX, TestBase
from flask_login import UserMixin
import safrs, flask_sqlalchemy, os
from safrs import jsonapi_attr
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.sql.sqltypes import NullType
from typing import List

db = SQLAlchemy() 
Base = declarative_base()  # type: flask_sqlalchemy.model.DefaultMeta
metadata = Base.metadata

#NullType = db.String  # datatype fixup
#TIMESTAMP= db.TIMESTAMP

from sqlalchemy.dialects.sqlite import *

if os.getenv('APILOGICPROJECT_NO_FLASK') is None or os.getenv('APILOGICPROJECT_NO_FLASK') == 'None':
    Base = SAFRSBaseX   # enables rules to be used outside of Flask, e.g., test data loading
else:
    Base = TestBase     # ensure proper types, so rules work for data loading
    print('*** Models.py Using TestBase ***')



class Configuration(Base):  # type: ignore
    """
    description: Stores various system configuration settings.
    """
    __tablename__ = 'configuration'
    _s_collection_name = 'Configuration'  # type: ignore

    id = Column(Integer, primary_key=True)
    key = Column(String)
    value = Column(String)

    # parent relationships (access parent)

    # child relationships (access children)



class Profile(Base):  # type: ignore
    """
    description: Stores additional info about the user.
    """
    __tablename__ = 'profile'
    _s_collection_name = 'Profile'  # type: ignore

    id = Column(Integer, primary_key=True)
    bio = Column(String)
    date_of_birth = Column(Date)
    user_id = Column(ForeignKey('user.id'))

    # parent relationships (access parent)
    user : Mapped["User"] = relationship(foreign_keys='[Profile.user_id]', back_populates=("ProfileList"))

    # child relationships (access children)
    UserList : Mapped[List["User"]] = relationship(foreign_keys='[User.profile_id]', back_populates="profile")



class Role(Base):  # type: ignore
    """
    description: Defines different roles within the system.
    """
    __tablename__ = 'role'
    _s_collection_name = 'Role'  # type: ignore

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)

    # parent relationships (access parent)

    # child relationships (access children)
    UserRoleList : Mapped[List["UserRole"]] = relationship(back_populates="role")



class Team(Base):  # type: ignore
    """
    description: Represents a team within the system.
    """
    __tablename__ = 'team'
    _s_collection_name = 'Team'  # type: ignore

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)

    # parent relationships (access parent)

    # child relationships (access children)
    UserTeamList : Mapped[List["UserTeam"]] = relationship(back_populates="team")



class User(Base):  # type: ignore
    """
    description: Represents a system user.
    """
    __tablename__ = 'user'
    _s_collection_name = 'User'  # type: ignore

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    created_at = Column(DateTime)
    profile_id = Column(ForeignKey('profile.id'))

    # parent relationships (access parent)
    profile : Mapped["Profile"] = relationship(foreign_keys='[User.profile_id]', back_populates=("UserList"))

    # child relationships (access children)
    ProfileList : Mapped[List["Profile"]] = relationship(foreign_keys='[Profile.user_id]', back_populates="user")
    AssetList : Mapped[List["Asset"]] = relationship(back_populates="owner")
    AuditLogList : Mapped[List["AuditLog"]] = relationship(back_populates="user")
    DepartmentList : Mapped[List["Department"]] = relationship(back_populates="head")
    ProjectList : Mapped[List["Project"]] = relationship(back_populates="lead")
    TaskList : Mapped[List["Task"]] = relationship(back_populates="assigned_to")
    UserRoleList : Mapped[List["UserRole"]] = relationship(back_populates="user")
    UserTeamList : Mapped[List["UserTeam"]] = relationship(back_populates="user")



class Asset(Base):  # type: ignore
    """
    description: Represents assets owned by users.
    """
    __tablename__ = 'asset'
    _s_collection_name = 'Asset'  # type: ignore

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    owner_id = Column(ForeignKey('user.id'))

    # parent relationships (access parent)
    owner : Mapped["User"] = relationship(back_populates=("AssetList"))

    # child relationships (access children)



class AuditLog(Base):  # type: ignore
    """
    description: Keeps track of user activities.
    """
    __tablename__ = 'audit_log'
    _s_collection_name = 'AuditLog'  # type: ignore

    id = Column(Integer, primary_key=True)
    action = Column(String)
    user_id = Column(ForeignKey('user.id'))
    timestamp = Column(DateTime)

    # parent relationships (access parent)
    user : Mapped["User"] = relationship(back_populates=("AuditLogList"))

    # child relationships (access children)



class Department(Base):  # type: ignore
    """
    description: Defines departments within the company.
    """
    __tablename__ = 'department'
    _s_collection_name = 'Department'  # type: ignore

    id = Column(Integer, primary_key=True)
    name = Column(String)
    head_id = Column(ForeignKey('user.id'))

    # parent relationships (access parent)
    head : Mapped["User"] = relationship(back_populates=("DepartmentList"))

    # child relationships (access children)



class Project(Base):  # type: ignore
    """
    description: Represents projects within the organization.
    """
    __tablename__ = 'project'
    _s_collection_name = 'Project'  # type: ignore

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    lead_id = Column(ForeignKey('user.id'))

    # parent relationships (access parent)
    lead : Mapped["User"] = relationship(back_populates=("ProjectList"))

    # child relationships (access children)



class Task(Base):  # type: ignore
    """
    description: Represents tasks assigned to users.
    """
    __tablename__ = 'task'
    _s_collection_name = 'Task'  # type: ignore

    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
    assigned_to_id = Column(ForeignKey('user.id'))
    status = Column(String)

    # parent relationships (access parent)
    assigned_to : Mapped["User"] = relationship(back_populates=("TaskList"))

    # child relationships (access children)



class UserRole(Base):  # type: ignore
    """
    description: Associative table connecting users with roles.
    """
    __tablename__ = 'user_role'
    _s_collection_name = 'UserRole'  # type: ignore

    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey('user.id'))
    role_id = Column(ForeignKey('role.id'))

    # parent relationships (access parent)
    role : Mapped["Role"] = relationship(back_populates=("UserRoleList"))
    user : Mapped["User"] = relationship(back_populates=("UserRoleList"))

    # child relationships (access children)



class UserTeam(Base):  # type: ignore
    """
    description: Associative table connecting users with teams.
    """
    __tablename__ = 'user_team'
    _s_collection_name = 'UserTeam'  # type: ignore

    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey('user.id'))
    team_id = Column(ForeignKey('team.id'))

    # parent relationships (access parent)
    team : Mapped["Team"] = relationship(back_populates=("UserTeamList"))
    user : Mapped["User"] = relationship(back_populates=("UserTeamList"))

    # child relationships (access children)
