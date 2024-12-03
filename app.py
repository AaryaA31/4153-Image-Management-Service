from flask import Flask
from flask_cors import CORS
from flasgger import Swagger
from config import config_db
from flask_marshmallow import Marshmallow
from middleware import before_request_logging, after_request_logging
from routes.review_routes import reviews_bp
from routes.redirect_routes import redirect_bp


app = Flask(__name__)
CORS(app)
config_db(app)
ma = Marshmallow(app)

template = {
  "swagger": "2.0",
  "info": {
    "title": "Image Rating Service",
    "version": "0.0.1"
  },
  "host": "localhost:8000", 
  "schemes": [
    "http",
  ],
}

swagger = Swagger(app, template=template)

app.before_request(before_request_logging)
app.after_request(after_request_logging)

app.register_blueprint(reviews_bp, url_prefix="/api/v1")
app.register_blueprint(redirect_bp)

if __name__ == '__main__':
    app.run(port=8000)
