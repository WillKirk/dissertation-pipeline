import os

# S1 - OBVIOUS: Hardcoded Flask secret key
SECRET_KEY = "hardcoded-secret-key-123"

class Config:
    SECRET_KEY = SECRET_KEY
    SQLALCHEMY_DATABASE_URI = "sqlite:///dissertation.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class ProductionConfig(Config):
    DEBUG = False

class DevelopmentConfig(Config):
    DEBUG = True