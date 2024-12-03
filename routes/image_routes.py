from flask import Blueprint, jsonify, request
from models import Review, Dish, db
from schemas import ReviewSchema
from datetime import datetime

# register blueprint and create schemas
reviews_bp = Blueprint('reviews', __name__)
review_schema = ReviewSchema()
reviews_schema = ReviewSchema(many=True)

# POST /api/v1/reviews: Submit a new review
@reviews_bp.route('/reviews', methods=['POST'])
def submit_review():
    '''
    Endpoint to submit a review for a specified dish.
    ---
    tags:
      - review-rating-service
    parameters:
      - name: body
        in: body
        required: true
        schema:
          id: Review
          required:
            - dish_id
            - rating
          properties:
            dish_id:
              type: integer
              description: The ID of the dish being reviewed
              example: 1
            rating:
              type: integer
              description: The rating of the dish out of 5
              example: 4
            review:
              type: string
              description: Comments from the reviewer
              example: "Pretty good. Could be saltier."
    responses:
      201:
        description: Review submitted.
        properties:
            id:
              type: integer
              example: 3
            message:
              type: string
              example: "Review submitted."
            _links:
              type: object
              properties:
                collection:
                  type: object
                  properties:
                    href:
                      type: string
                      example: "/api/v1/reviews/5/dish"
                    method:
                      type: string
                      example: "GET"
                submit:
                  type: object
                  properties:
                    href:
                      type: string
                      example: "/api/v1/reviews"
                    method:
                      type: string
                      example: "POST"
                delete:
                  type: object
                  properties:
                    href:
                      type: string
                      example: "/api/v1/reviews/3"
                    method:
                      type: string
                      example: "DELETE"
                self:
                  type: object
                  properties:
                    href:
                      type: string
                      example: "/api/v1/reviews/3"
                    method:
                      type: string
                      example: "GET"
                update:
                  type: object
                  properties:
                    href:
                      type: string
                      example: "/api/v1/reviews/3"
                    method:
                      type: string
                      example: "PUT"
      400:
        description: Invalid input
    '''
    data = request.json

    dish = Dish.query.get(data['dish_id'])
    if not dish:
        return jsonify({"error": "Invalid dish_id"}), 400
    
    new_review = Review(**data)
    db.session.add(new_review)
    db.session.commit()
    
    return review_schema.jsonify({"id": new_review.id, "dish_id": dish.id, "message": "Review submitted"}), 201

# GET /api/v1/reviews/{id}: Retrieve review details
@reviews_bp.route('/reviews/<int:id>', methods=['GET'])
def get_review(id):
    '''
    Endpoint to get a specified review.
    ---
    tags:
      - review-rating-service
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: ID of the review.
        example: 1
    responses:
      200:
        description: A review.
        schema:
          properties:
            id:
              type: integer
              example: 1
            dish_id:
              type: integer
              example: 3
            rating:
              type: integer
              example: 4
            review:
              type: string
              example: "Pretty good. Could be saltier."
            created_at:
              type: string
              example: "2024-11-14 00:16:48.193448"
            updated_at:
              type: string
              example: "2024-11-15 00:16:48.193448"
            _links:
              type: object
              properties:
                collection:
                  type: object
                  properties:
                    href:
                      type: string
                      example: "/api/v1/reviews/5/dish"
                    method:
                      type: string
                      example: "GET"
                submit:
                  type: object
                  properties:
                    href:
                      type: string
                      example: "/api/v1/reviews"
                    method:
                      type: string
                      example: "POST"
                delete:
                  type: object
                  properties:
                    href:
                      type: string
                      example: "/api/v1/reviews/3"
                    method:
                      type: string
                      example: "DELETE"
                self:
                  type: object
                  properties:
                    href:
                      type: string
                      example: "/api/v1/reviews/3"
                    method:
                      type: string
                      example: "GET"
                update:
                  type: object
                  properties:
                    href:
                      type: string
                      example: "/api/v1/reviews/3"
                    method:
                      type: string
                      example: "PUT"
      404:
        description: Review not found.
    '''
    review = db.session.query(Review).get(id)
    if not review:
        return jsonify({"error": "Review not found"}), 404
    return review_schema.jsonify(review), 200

# PUT /api/v1/reviews/{id}: Update review details
@reviews_bp.route('/reviews/<int:id>', methods=['PUT'])
def update_review(id):
    '''
    Endpoint to edit a specified review.
    ---
    tags:
      - review-rating-service
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: ID of the review.
        example: 1
      - name: body
        in: body
        required: true
        schema:
          properties:
            rating:
              type: integer
              example: 4
            review:
              type: string
              example: "Pretty good. Could be saltier."
    responses:
      200:
        description: Review updated.
        schema:
          properties:
            id:
              type: integer
              example: 3
            message:
              type: string
              example: "Review updated."
            _links:
              type: object
              properties:
                collection:
                  type: object
                  properties:
                    href:
                      type: string
                      example: "/api/v1/reviews/5/dish"
                    method:
                      type: string
                      example: "GET"
                submit:
                  type: object
                  properties:
                    href:
                      type: string
                      example: "/api/v1/reviews"
                    method:
                      type: string
                      example: "POST"
                delete:
                  type: object
                  properties:
                    href:
                      type: string
                      example: "/api/v1/reviews/3"
                    method:
                      type: string
                      example: "DELETE"
                self:
                  type: object
                  properties:
                    href:
                      type: string
                      example: "/api/v1/reviews/3"
                    method:
                      type: string
                      example: "GET"
                update:
                  type: object
                  properties:
                    href:
                      type: string
                      example: "/api/v1/reviews/3"
                    method:
                      type: string
                      example: "PUT"
      404:
        description: Review not found.
    '''
    updated_data = request.json
    review = db.session.query(Review).get(id)
    if not review:
        return jsonify({"error": "Review not found"}), 404
    if 'rating' in updated_data:
        review.rating = updated_data['rating']
    if 'review' in updated_data:
        review.review = updated_data['review']
    review.updated_at = datetime.now()
    db.session.commit()
    return review_schema.jsonify({"id": review.id, "dish_id": review.dish_id, "message": "Review updated"}), 200

# DELETE /api/v1/reviews/{id}: Delete a review
@reviews_bp.route('/reviews/<int:id>', methods=['DELETE'])
def delete_review(id):
    '''
    Endpoint to delete a specified review.
    ---
    tags:
      - review-rating-service
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: ID of the review.
        example: 1
    responses:
      204:
        description: No content.
      404:
        description: Review not found.
    '''
    review = db.session.query(Review).get(id)
    if not review:
        return jsonify({"error": "Review not found"}), 404
    db.session.delete(review)
    db.session.commit()
    return jsonify({'message': 'Review successfully deleted'}), 204
