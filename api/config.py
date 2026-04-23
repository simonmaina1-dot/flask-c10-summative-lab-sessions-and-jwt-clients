import os


class Config:
    SECRET_KEY = (
        os.environ.get("SECRET_KEY")
        or "dev-super-secret-jwt-key-that-is-long-enough-for-hs256-min32bytes-like-this-12345678"
    )
    JWT_SECRET_KEY = (
        os.environ.get("JWT_SECRET_KEY")
        or "dev-jwt-super-secret-key-that-is-long-enough-for-hs256-min32bytes-like-this-too-987654"
    )
    JWT_TOKEN_LOCATION = ['headers', 'cookies']
    JWT_ACCESS_COOKIE_PATH = '/api'
    JWT_COOKIE_SECURE = False
    JWT_COOKIE_CSRF_PROTECT = False
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or "sqlite:///notes.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
