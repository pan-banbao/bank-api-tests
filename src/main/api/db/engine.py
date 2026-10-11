from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.main.api.configs.config import Config
from src.main.api.db import models

engine = create_engine(Config.fetch('dataBaseUrl'), echo=False)
SessionLocal = sessionmaker(bind=engine)