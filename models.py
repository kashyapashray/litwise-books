from sqlalchemy import Column, Integer, String, Text, Date, Float, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()

class Book(Base):
    __tablename__ = 'books'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    # Basic book information
    title = Column(String(500), nullable=False)
    author = Column(String(300), nullable=True)
    isbn = Column(String(20), nullable=True)
    isbn13 = Column(String(20), nullable=True)
    
    # Publication details
    first_publish_year = Column(Integer, nullable=True)
    publisher = Column(String(300), nullable=True)
    number_of_pages = Column(Integer, nullable=True)
    
    # Open Library specific fields
    openlibrary_key = Column(String(100), nullable=True, unique=True)
    work_key = Column(String(100), nullable=True)
    edition_key = Column(String(100), nullable=True)
    
    # Content and descriptions
    description = Column(Text, nullable=True)
    subjects = Column(Text, nullable=True)  # Comma-separated subjects
    
    # Ratings and popularity
    average_rating = Column(Float, nullable=True)
    rating_count = Column(Integer, nullable=True)
    
    # Additional metadata
    language = Column(String(10), nullable=True, default='en')
    cover_image_url = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(String(50), default=str(datetime.now()))
    updated_at = Column(String(50), default=str(datetime.now()))
    
    def __repr__(self):
        return f"<Book(id={self.id}, title='{self.title}', author='{self.author}')>"
    
    def to_dict(self):
        """Convert book object to dictionary for easy serialization"""
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'isbn': self.isbn,
            'isbn13': self.isbn13,
            'first_publish_year': self.first_publish_year,
            'publisher': self.publisher,
            'number_of_pages': self.number_of_pages,
            'openlibrary_key': self.openlibrary_key,
            'work_key': self.work_key,
            'edition_key': self.edition_key,
            'description': self.description,
            'subjects': self.subjects,
            'average_rating': self.average_rating,
            'rating_count': self.rating_count,
            'language': self.language,
            'cover_image_url': self.cover_image_url,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        } 