## Description
__Responsibilities__: Handles submission of text reviews and ratings, as well as retrieving reviews for a particular dish.

__Endpoints__:
- POST /api/v1/reviews: Submit a new review
- GET /api/v1/reviews: Retrieve a list of all reviews
- GET /api/v1/reviews/{id}: Retrieve review details
- PUT /api/v1/reviews/{id}: Update review details
- DELETE /api/v1/reviews/{id}: Delete a review
More detailed documentation can be found at /apidocs

## How to Run
1. Create a virtual environment and install dependencies in `requirements.txt`
2. Run `flask run --host=0.0.0.0 --port=8000`