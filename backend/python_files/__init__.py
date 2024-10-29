from flask import Flask
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from datetime import timedelta
from flask_cors import CORS

db = SQLAlchemy()
DB_NAME = 'lib_ms.sqlite3'


def db_initialization():
    from .models import User

    # Check if the librarian already exists
    db.create_all()

    librarian = User.query.filter_by(is_librarian=True).first()

    # Add librarian if not exists
    if not librarian:
        default_librarian = User(
            name='Librarian',
            email='librarian@gmail.com',  # Default username
            password='librarian',  # Default password (should be changed)
            is_librarian=True
        )
        db.session.add(default_librarian)
        db.session.commit()
        print("Default librarian added to the database.")
    else:
        print("Librarian already exists in the database.")


def create_app():
    app = Flask(__name__)
    CORS(app)
    
    app.debug = True
    app.config['SECRET_KEY'] = "This project(LibMS) is created by Vivek."
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['JWT_SECRET_KEY'] = 'hello vivek'

    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=5)
    app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=30)

    jwt = JWTManager(app)

    db.init_app(app)
    api = Api(app)

    from .models import User
    from .models import Section
    from .models import Ebook
    from .models import Request

    from .controllers import views
    from .auth import auth

    app.register_blueprint(views)
    app.register_blueprint(auth)

    from .api import SectionAPI, SectionListAPI, EbookAPI, EbookListAPI, StatisticsAPI, ReadBookListAPI, SearchAPI, RequestListAPI, RequestAPI, UserRequestsAPI, ReturnBookAPI, ReturnedBooksAPI, FeedbackAPI, UserFeedbackAPI

    api.add_resource(EbookListAPI, '/api/ebooks')
    api.add_resource(EbookAPI, '/api/ebooks/<int:ebook_id>')

    api.add_resource(SectionListAPI, '/api/sections')
    api.add_resource(SectionAPI, '/api/sections/<int:section_id>')

    api.add_resource(RequestListAPI, '/api/requests')
    api.add_resource(RequestAPI, '/api/requests/<int:request_id>')
    api.add_resource(UserRequestsAPI, '/api/user/requests')
    api.add_resource(ReadBookListAPI, '/api/read-books/<int:user_id>')
    api.add_resource(ReturnedBooksAPI, '/api/returned-books')
    api.add_resource(StatisticsAPI, '/api/statistics')
    api.add_resource(SearchAPI, '/api/search')
    api.add_resource(ReturnBookAPI, '/api/return-book/<int:request_id>')
    api.add_resource(FeedbackAPI, '/api/feedback', '/api/feedback/<int:ebook_id>')
    api.add_resource(UserFeedbackAPI, '/api/user/feedbacks')

    from .celery_config import celery
    celery.conf.update(app.config)
    
    return app, api