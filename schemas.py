from flask_marshmallow import Marshmallow
from marshmallow import fields
from models import Review
from marshmallow_sqlalchemy import SQLAlchemySchema

ma = Marshmallow()

class ReviewSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Review

    id = ma.auto_field()
    dish_id = ma.auto_field()
    rating = ma.auto_field()
    review = ma.auto_field()
    created_at = ma.auto_field()
    updated_at = ma.auto_field()

    message = fields.String(allow_none=True)

    # HATEOAS links
    _links = ma.Hyperlinks({
        "self": {
            "href": ma.URLFor("reviews.get_review", values=dict(id="<id>")),
            "method": "GET"
        },
        "update": {
            "href": ma.URLFor("reviews.update_review", values=dict(id="<id>")),
            "method": "PUT"
        },
        "delete": {
            "href": ma.URLFor("reviews.delete_review", values=dict(id="<id>")),
            "method": "DELETE"
        },
        "collection": {
            "href": ma.URLFor("reviews.get_reviews"),
            "method": "GET"
        },
        "submit": {
            "href": ma.URLFor("reviews.submit_review", values=dict(dish_id="<dish_id>")),
            "method": "POST"
        }
    })