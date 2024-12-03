from flask import Blueprint, jsonify, request
from models import Image, db
from datetime import datetime

# Register Blueprint
images_bp = Blueprint('images', __name__)

# POST /api/v1/reviews/{id}/images: Add or Update an Image for a Review
@images_bp.route('/reviews/<int:review_id>/images', methods=['POST'])
def add_or_update_image(review_id):
    '''
    Endpoint to add or update an image for a specified review.
    ---
    tags:
      - review-image-service
    parameters:
      - name: review_id
        in: path
        type: integer
        required: true
        description: ID of the review.
        example: 1
      - name: image
        in: formData
        type: file
        required: true
        description: The image file to upload.
    responses:
      201:
        description: Image added/updated.
      400:
        description: Invalid input.
      404:
        description: Review not found.
    '''
    if 'image' not in request.files:
        return jsonify({"error": "No image file provided"}), 400

    # Get the uploaded file
    file = request.files['image']
    binary_data = file.read()

    # Check if the image already exists for the review
    image = Image.query.filter_by(review_id=review_id).first()

    if image:
        # Update existing image
        image.image_data = binary_data
        image.updated_at = datetime.now()
        message = "Image updated."
    else:
        # Add new image
        image = Image(review_id=review_id, image_data=binary_data)
        db.session.add(image)
        message = "Image added."

    db.session.commit()
    return jsonify({"message": message, "review_id": review_id}), 201


# GET /api/v1/reviews/{id}/images: Retrieve the Image for a Review
@images_bp.route('/reviews/<int:review_id>/images', methods=['GET'])
def get_image(review_id):
    '''
    Endpoint to get the image for a specified review.
    ---
    tags:
      - review-image-service
    parameters:
      - name: review_id
        in: path
        type: integer
        required: true
        description: ID of the review.
        example: 1
    responses:
      200:
        description: Image retrieved.
        content:
          image/jpeg: {}
      404:
        description: Image not found.
    '''
    image = Image.query.filter_by(review_id=review_id).first()
    if not image:
        return jsonify({"error": "Image not found"}), 404

    # Return the binary data as a response
    return (image.image_data, 200, {'Content-Type': 'image/jpeg'})


# DELETE /api/v1/reviews/{id}/images: Delete the Image for a Review
@images_bp.route('/reviews/<int:review_id>/images', methods=['DELETE'])
def delete_image(review_id):
    '''
    Endpoint to delete the image for a specified review.
    ---
    tags:
      - review-image-service
    parameters:
      - name: review_id
        in: path
        type: integer
        required: true
        description: ID of the review.
        example: 1
    responses:
      204:
        description: No content.
      404:
        description: Image not found.
    '''
    image = Image.query.filter_by(review_id=review_id).first()
    if not image:
        return jsonify({"error": "Image not found"}), 404

    db.session.delete(image)
    db.session.commit()
    return jsonify({"message": "Image successfully deleted"}), 204
