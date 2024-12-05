from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def config_db(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin:password@image-management-service.cpyygk6aylwd.us-east-1.rds.amazonaws.com:3306/image_management'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    with app.app_context():
        pass  # Database is already set up; no need to create tables.
