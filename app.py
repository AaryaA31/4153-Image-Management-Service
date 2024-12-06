from flask import Flask
from flask_cors import CORS
from flasgger import Swagger
from config import config_db
from flask_marshmallow import Marshmallow
from middleware import before_request_logging, after_request_logging
from routes.image_routes import images_bp
from routes.redirect_routes import redirect_bp


application = Flask(__name__)
CORS(application)
config_db(application)
ma = Marshmallow(application)

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

swagger = Swagger(application, template=template)

application.before_request(before_request_logging)
application.after_request(after_request_logging)

application.register_blueprint(images_bp, url_prefix="/api/v1")
application.register_blueprint(redirect_bp)

if __name__ == '__main__':
    application.run(port=5000)
