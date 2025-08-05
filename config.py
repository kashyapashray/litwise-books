import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Database configuration
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = int(os.getenv('DB_PORT', 3306))
    DB_NAME = os.getenv('DB_NAME', 'litwise_books')
    DB_USER = os.getenv('DB_USER', 'root')
    DB_PASSWORD = os.getenv('DB_PASSWORD', '')
    
    # Open Library API
    OPENLIBRARY_BASE_URL = "https://openlibrary.org"
    OPENLIBRARY_SEARCH_URL = f"{OPENLIBRARY_BASE_URL}/search.json"
    OPENLIBRARY_WORKS_URL = f"{OPENLIBRARY_BASE_URL}/works"
    
    # Request settings
    REQUEST_TIMEOUT = 30
    REQUEST_DELAY = 0.5  # Delay between API calls to be respectful
    
    @property
    def DATABASE_URL(self):
        return f"mysql+pymysql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}" 