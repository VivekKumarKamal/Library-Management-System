from backend.python_files import db
from flask_login import UserMixin
from sqlalchemy import func, ForeignKey
from datetime import datetime, timedelta
from passlib.hash import pbkdf2_sha256 as sha256

# This association table is created automatically by SQLAlchemy
book_section = db.Table('book_section',
    db.Column('book_id', db.Integer, db.ForeignKey('ebooks.id'), primary_key=True),
    db.Column('section_id', db.Integer, db.ForeignKey('sections.id'), primary_key=True)
)

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    is_librarian = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)

    requests = db.relationship('Request', backref='user', cascade='all, delete')
    read_books = db.relationship('ReadBook', backref='user', cascade='all, delete')
    feedbacks = db.relationship('Feedback', backref='user', cascade='all, delete')

    def __init__(self, name, email, password, is_librarian=False):
        self.name = name
        self.email = email
        self.password_hash = self.generate_hash(password)
        self.is_librarian = is_librarian

    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)

    @staticmethod
    def verify_hash(password, hash):
        return sha256.verify(password, hash)

    def set_password(self, password):
        self.password_hash = sha256.hash(password)

    # def verify_hash(self, password):
    #     return self.verify_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.name}>'


class Section(db.Model):
    __tablename__ = 'sections'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    ebooks = db.relationship('Ebook', secondary=book_section, back_populates='sections')

    def __init__(self, name, description=None):
        self.name = name
        self.description = description

    def __repr__(self):
        return f'<Section {self.name}>'


class Ebook(db.Model):
    __tablename__ = 'ebooks'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), unique=True, nullable=False)
    authors = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    rating = db.Column(db.Float, nullable=True, default=0.0) # this is the average rating
    total_ratings = db.Column(db.Integer, nullable=True, default=0)
    total_borrows = db.Column(db.Integer, nullable=True, default=0)

    sections = db.relationship('Section', secondary=book_section, back_populates='ebooks')

    requests = db.relationship('Request', backref='ebook', cascade='all, delete')
    read_books = db.relationship('ReadBook', backref='ebook', cascade='all, delete')
    feedbacks = db.relationship('Feedback', backref='ebook', cascade='all, delete')

    def __init__(self, title, authors, content, section_ids):
        self.title = title
        self.authors = authors
        self.content = content
        for section_id in section_ids:
            section = Section.query.get(section_id)
            if section:
                self.sections.append(section)

    def add_rating(self, new_rating):
        self.rating = (self.rating * self.total_ratings + new_rating) / (self.total_ratings + 1)
        self.total_ratings += 1

    def __repr__(self):
        return f'<Ebook {self.title} by {self.authors}>'


class Request(db.Model):
    __tablename__ = 'requests'

    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(20), nullable=False, default='pending')  # pending, granted, revoked
    request_date = db.Column(db.DateTime, default=datetime.utcnow)
    issue_date = db.Column(db.DateTime, nullable=True)
    return_date = db.Column(db.DateTime, nullable=True)
    due_date = db.Column(db.DateTime, nullable=True)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    ebook_id = db.Column(db.Integer, db.ForeignKey('ebooks.id'), nullable=False)

    read_book = db.relationship('ReadBook', backref='request', uselist=False)

    def __init__(self, user_id, ebook_id):
        self.user_id = user_id
        self.ebook_id = ebook_id

    def __repr__(self):
        return f'<Request {self.id} - User {self.user_id} - Ebook {self.ebook_id}>'


class ReadBook(db.Model):
    __tablename__ = 'read_books'

    id = db.Column(db.Integer, primary_key=True)
    read_date = db.Column(db.DateTime, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    ebook_id = db.Column(db.Integer, db.ForeignKey('ebooks.id'), nullable=False)
    request_id = db.Column(db.Integer, db.ForeignKey('requests.id'), nullable=False, unique=True)

    def __init__(self, user_id, ebook_id, request_id):
        self.user_id = user_id
        self.ebook_id = ebook_id
        self.request_id = request_id

    def __repr__(self):
        return f'<ReadBook {self.id} - User {self.user_id} - Ebook {self.ebook_id} - Request {self.request_id}>'

class Feedback(db.Model):
    __tablename__ = 'feedbacks'
    __table_args__ = (db.UniqueConstraint('user_id', 'ebook_id', name='uq_user_ebook_feedback'),)

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    rating = db.Column(db.Integer, nullable=False)
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    ebook_id = db.Column(db.Integer, db.ForeignKey('ebooks.id'), nullable=False)

    def __init__(self, content, user_id, ebook_id, rating):
        self.content = content
        self.user_id = user_id
        self.ebook_id = ebook_id
        self.rating = rating

    def __repr__(self):
        return f'<Feedback {self.id} by User {self.user_id} for Ebook {self.ebook_id}>'