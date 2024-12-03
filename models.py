from config import db
from sqlalchemy import Column, Integer, BLOB
from datetime import datetime

class Image(db.Model):
    __tablename__ = 'images'

    id = Column(Integer, primary_key=True)  # Use review_id as the primary key
    image_data = Column(BLOB, nullable=False)  # Store binary image data

    def __repr__(self):
        return f"<Image(review_id={self.id})>"
