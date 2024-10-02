from flask import Flask, request, jsonify
import time

app = Flask(__name__)

# In-memory storage for dishes, reviews, and their images (this would typically be a database or cloud storage)
dishes = [{"id": 1, "name": "Pizza", "description": "Cheese and tomato pizza", "category": "Main Course", "dietary_info": "Vegetarian"}]
reviews = [{"id": 1, "dish_id": 1, "content": "Great pizza!"}]
dish_images = {}
review_images = {}
next_dish_id = 2
next_review_id = 2
next_image_id = 1

# Helper function to generate image metadata
def generate_image_metadata(image):
    global next_image_id
    image_metadata = {
        "image_id": next_image_id,
        "filename": image.filename,
        "content_type": image.content_type,
        "upload_timestamp": time.time(),
        "file_size": len(image.read())  # in bytes
    }
    next_image_id += 1
    return image_metadata

# POST /dishes/{id}/images: Upload images for a particular dish
@app.route('/dishes/<int:id>/images', methods=['POST'])
def upload_dish_image(id):
    if id not in [dish['id'] for dish in dishes]:
        return jsonify({"error": "Dish not found"}), 404

    if 'image' not in request.files:
        return jsonify({"error": "No image provided"}), 400

    image = request.files['image']
    image_metadata = generate_image_metadata(image)

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
    image_metadata = generate_image_metadata(image)

    if id not in review_images:
        review_images[id] = []

    review_images[id].append(image_metadata)

    return jsonify({"message": "Image uploaded", "image_metadata": image_metadata}), 201

if __name__ == '__main__':
   app.run(host='0.0.0.0', port=5001)
