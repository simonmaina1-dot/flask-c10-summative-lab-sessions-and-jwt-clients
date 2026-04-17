import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from api.extensions import db, bcrypt
from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship

# User model for authentication
class User(db.Model):
    __tablename__ = 'user'  # Note: lowercase for FK reference
    
    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    hashed_password = Column(String(120), nullable=False)
    
    # Relationship to notes
    notes = relationship('Note', backref='user', lazy=True)

    def __init__(self, username, password):
        self.username = username
        self.hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.hashed_password, password)

# Note model
class Note(db.Model):
    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    content = Column(Text, nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)

    def __init__(self, title, content, user_id):
        self.title = title
        self.content = content
        self.user_id = user_id

    def __repr__(self):
        return f'<Note {self.title}: {self.content[:20]}...>'
