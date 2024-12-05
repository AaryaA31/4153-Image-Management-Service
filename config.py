from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text  # Import text for raw SQL queries

db = SQLAlchemy()

def config_db(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin:password@image-management-service.cpyygk6aylwd.us-east-1.rds.amazonaws.com:3306/image_management'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    with app.app_context():
        pass  # Database is already set up; no need to create tables.

app = Flask(__name__)

# Configure the app with the database
config_db(app)

# Define a simple route to test the connection
@app.route('/test-db', methods=['GET'])
def test_db():
    try:
        # Use SQLAlchemy's text for raw SQL
        with db.engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            return "Database connection successful! Result: {}".format(result.fetchone()), 200
    except Exception as e:
        return "Database connection failed: {}".format(str(e)), 500

if __name__ == '__main__':
    app.run(debug=True)
