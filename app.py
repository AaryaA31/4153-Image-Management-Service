from flask import Flask, request, jsonify
import time
import uuid
import boto3  # for S3 storage
from botocore.exceptions import NoCredentialsError

app = Flask(__name__)

# Configuration for AWS S3 (replace with your actual bucket name and credentials)
S3_BUCKET = 'your-s3-bucket-name'
S3_REGION = 'your-region'
s3_client = boto3.client('s3', region_name=S3_REGION)

# In-memory storage for dishes, reviews, and their metadata (use a database for persistence)
dishes = [{"id": 1, "name": "Pizza", "description": "Cheese and tomato pizza", "category": "Main Course", "dietary_info": "Vegetarian"}]
reviews = [{"id": 1, "dish_id": 1, "content": "Great pizza!"}]
dish_images = {}  # stores image metadata, real image files are stored in S3
review_images = {}

next_dish_id = 2
next_review_id = 2

# Helper function to generate image metadata and upload to S3
def generate_image_metadata(image, entity_type, entity_id):
    image_id = str(uuid.uuid4())  # generate a unique image ID
    file_extension = image.filename.rsplit('.', 1)[-1].lower()
    s3_filename = f"{entity_type}/{entity_id}/{image_id}.{file_extension}"
    
    # Upload image to S3
    try:
        image.seek(0)  # Ensure we're reading from the start of the file
        s3_client.upload_fileobj(image, S3_BUCKET, s3_filename, ExtraArgs={'ContentType': image.content_type})
    except NoCredentialsError:
        return {"error": "Credentials not available"}

    image_metadata = {
        "image_id": image_id,
        "filename": image.filename,
        "content_type": image.content_type,
        "upload_timestamp": time.time(),
        "file_size": image.content_length,
        "s3_url": f"https://{S3_BUCKET}.s3.{S3_REGION}.amazonaws.com/{s3_filename}"
    }
    return image_metadata

# POST /dishes/{id}/images: Upload images for a particular dish
@app.route('/dishes/<int:id>/images', methods=['POST'])
def upload_dish_image(id):
    if id not in [dish['id'] for dish in dishes]:
        return jsonify({"error": "Dish not found"}), 404

    if 'image' not in request.files:
        return jsonify({"error": "No image provided"}), 400

    image = request.files['image']
    image_metadata = generate_image_metadata(image, "dishes", id)

    if "error" in image_metadata:
        return jsonify({"error": image_metadata["error"]}), 500

    if id not in dish_images:
        dish_images[id] = []

    dish_images[id].append(image_metadata)

    return jsonify({"message": "Image uploaded", "image_metadata": image_metadata}), 201

# GET /dishes/{id}/images: Retrieve all images for a particular dish
@app.route('/dishes/<int:id>/images', methods=['GET'])
def get_dish_images(id):
    if id not in [dish['id'] for dish in dishes]:
        return jsonify({"error": "Dish not found"}), 404

    images = dish_images.get(id, [])

    return jsonify(images), 200

# GET /reviews/{id}/images: Retrieve images associated with a particular review
@app.route('/reviews/<int:id>/images', methods=['GET'])
def get_review_images(id):
    if id not in [review['id'] for review in reviews]:
        return jsonify({"error": "Review not found"}), 404

    images = review_images.get(id, [])

    return jsonify(images), 200

# POST /reviews/{id}/images: Upload images for a particular review
@app.route('/reviews/<int:id>/images', methods=['POST'])
def upload_review_image(id):
    if id not in [review['id'] for review in reviews]:
        return jsonify({"error": "Review not found"}), 404

    if 'image' not in request.files:
        return jsonify({"error": "No image provided"}), 400

    image = request.files['image']
    image_metadata = generate_image_metadata(image, "reviews", id)

    if "error" in image_metadata:
        return jsonify({"error": image_metadata["error"]}), 500

    if id not in review_images:
        review_images[id] = []

    review_images[id].append(image_metadata)

    return jsonify({"message": "Image uploaded", "image_metadata": image_metadata}), 201

if __name__ == '__main__':
   app.run(host='0.0.0.0', port=5001)
