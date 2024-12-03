from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

load_dotenv(override=True)

db = SQLAlchemy()

def config_db(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = \
    '{engine}+pymysql://{user}:{password}@{host}:{port}/{database}'.format(
        engine=os.getenv("DB_ENGINE"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        database=os.getenv('DB_NAME_1'),
    )

    app.config['SQLALCHEMY_BINDS'] = {
        'dish_db': '{engine}+pymysql://{user}:{password}@{host}:{port}/{database}'.format(
            engine=os.getenv('DB_ENGINE'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            host=os.getenv('DB_HOST'),
            port=os.getenv('DB_PORT'),
            database=os.getenv('DB_NAME_2'),
        ),
    }

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['CORS_HEADERS'] = 'Content-Type'
    app.config['CORS_SUPPORTS_CREDENTIALS'] = True
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

    db.init_app(app)
    with app.app_context():
        db.create_all()
