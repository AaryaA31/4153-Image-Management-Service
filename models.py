from config import db
from sqlalchemy import Column, Integer, String, Text, ForeignKey, TIMESTAMP
from datetime import datetime

class Review(db.Model):
    __tablename__ = 'reviews'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    # dish_id = Column(Integer, ForeignKey('dish_db.dishes.id'), nullable=False)
    dish_id = Column(Integer, nullable=False)
    rating = Column(Integer, nullable=False)
    review = Column(Text)
    created_at = Column(TIMESTAMP, default=str(datetime.now()))
    updated_at = Column(TIMESTAMP, default=str(datetime.now()))
    
    # relationships
    dish = db.relationship('Dish', primaryjoin='Review.dish_id == Dish.id', backref='reviews', foreign_keys=[dish_id])

    def __repr__(self):
        return f"<Review(id={self.id}, dish_id='{self.dish_id}', rating='{self.rating}', review='{self.review}', created_at='{self.created_at}', updated_at='{self.updated_at}')>"
    

class Dish(db.Model):
    __bind_key__ = 'dish_db'
    __tablename__ = 'dishes'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    dining_hall_id = Column(Integer, nullable=False)
    station_id = Column(Integer, nullable=False)
    created_at = Column(TIMESTAMP, default=str(datetime.now()))
    updated_at = Column(TIMESTAMP, default=str(datetime.now()))

    def __repr__(self):
        return f"<Dish(id={self.id}, name='{self.name}')>"