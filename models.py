# models.py
from sqlalchemy import Column, String, Integer, Text, Enum, TIMESTAMP, ForeignKey, JSON
from sqlalchemy.sql import func
from database import Base
import json as json_lib

class User(Base):
    __tablename__ = 'users'
    
    id = Column(String(50), primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    university = Column(String(100), nullable=False)
    major = Column(String(100), nullable=False)
    year = Column(String(50), nullable=False)
    learning_style = Column(Text)
    study_environments = Column(JSON)
    study_methods = Column(JSON)
    subjects = Column(JSON)
    schedule = Column(JSON)
    performance_level = Column(Integer, default=3)
    group_preferences = Column(JSON)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'university': self.university,
            'major': self.major,
            'year': self.year,
            'learningStyle': self.learning_style,
            'studyEnvironments': self.study_environments or [],
            'studyMethods': self.study_methods or [],
            'subjects': self.subjects or [],
            'schedule': self.schedule or {},
            'performanceLevel': self.performance_level,
            'groupPreferences': self.group_preferences or {}
        }

class StudyGroup(Base):
    __tablename__ = 'study_groups'
    
    id = Column(String(50), primary_key=True)
    title = Column(String(200), nullable=False)
    subject = Column(String(100), nullable=False)
    description = Column(Text)
    schedule = Column(String(200))
    location = Column(String(200))
    max_members = Column(Integer, default=6)
    current_members = Column(Integer, default=1)
    leader_id = Column(String(50), ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    leader_name = Column(String(100), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'subject': self.subject,
            'description': self.description,
            'schedule': self.schedule,
            'location': self.location,
            'maxMembers': self.max_members,
            'currentMembers': self.current_members,
            'leader': self.leader_name,
            'createdAt': self.created_at.isoformat() if self.created_at else None
        }

class GroupMember(Base):
    __tablename__ = 'group_members'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    group_id = Column(String(50), ForeignKey('study_groups.id', ondelete='CASCADE'), nullable=False)
    user_id = Column(String(50), ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    user_name = Column(String(100), nullable=False)
    user_major = Column(String(100))
    role = Column(Enum('leader', 'member'), default='member')
    status = Column(Enum('active', 'pending', 'archived'), default='pending')
    joined_at = Column(TIMESTAMP, server_default=func.now())
    
    def to_dict(self):
        return {
            'id': self.user_id,
            'name': self.user_name,
            'major': self.user_major,
            'role': self.role,
            'status': self.status,
            'joinedAt': self.joined_at.isoformat() if self.joined_at else None
        }

class Message(Base):
    __tablename__ = 'messages'
    
    id = Column(String(50), primary_key=True)
    group_id = Column(String(50), ForeignKey('study_groups.id', ondelete='CASCADE'), nullable=False)
    sender_id = Column(String(50), ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    sender_name = Column(String(100), nullable=False)
    message = Column(Text)
    type = Column(Enum('text', 'image', 'file', 'announcement'), default='text')
    image_uri = Column(Text)
    file_name = Column(String(255))
    timestamp = Column(TIMESTAMP, server_default=func.now())
    
    def to_dict(self):
        return {
            'id': self.id,
            'groupId': self.group_id,
            'senderId': self.sender_id,
            'senderName': self.sender_name,
            'message': self.message,
            'type': self.type,
            'imageUri': self.image_uri,
            'fileName': self.file_name,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None
        }

class MessageReaction(Base):
    __tablename__ = 'message_reactions'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    message_id = Column(String(50), ForeignKey('messages.id', ondelete='CASCADE'), nullable=False)
    user_id = Column(String(50), ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    user_name = Column(String(100), nullable=False)
    emoji = Column(String(10), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    
    def to_dict(self):
        return {
            'userId': self.user_id,
            'userName': self.user_name,
            'emoji': self.emoji
        }

class StudySession(Base):
    __tablename__ = 'study_sessions'
    
    id = Column(String(50), primary_key=True)
    group_id = Column(String(50), ForeignKey('study_groups.id', ondelete='CASCADE'), nullable=False)
    title = Column(String(200), nullable=False)
    scheduled_time = Column(String(200), nullable=False)
    location = Column(String(200), nullable=False)
    created_by = Column(String(50), ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    
    def to_dict(self):
        return {
            'id': self.id,
            'groupId': self.group_id,
            'title': self.title,
            'scheduledTime': self.scheduled_time,
            'location': self.location,
            'createdBy': self.created_by
        }

class SessionAttendee(Base):
    __tablename__ = 'session_attendees'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(String(50), ForeignKey('study_sessions.id', ondelete='CASCADE'), nullable=False)
    user_id = Column(String(50), ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    user_name = Column(String(100), nullable=False)
    joined_at = Column(TIMESTAMP, server_default=func.now())