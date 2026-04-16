import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-super-secret-jwt-key-that-is-long-enough-for-hs256-min32bytes-like-this-12345678'
    JWT_SECRET_KEY = SECRET_KEY
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///notes.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
