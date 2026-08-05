import os

# S1 - OBVIOUS: Hardcoded Flask secret key
SECRET_KEY = "hardcoded-secret-key-123"

# S2 - MODERATE: Hardcoded third-party API key
SENDGRID_API_KEY = "SG.hardcoded-api-key-example-1234567890"

class Config:
    SECRET_KEY = SECRET_KEY
    SQLALCHEMY_DATABASE_URI = "sqlite:///dissertation.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SENDGRID_API_KEY = SENDGRID_API_KEY

class ProductionConfig(Config):
    DEBUG = False

class DevelopmentConfig(Config):
    DEBUG = True