from flask import request, Blueprint
from flask_restful import Resource, Api, reqparse, fields, marshal_with, marshal
from flask_jwt_extended import jwt_required, get_jwt_identity
from .models import db, Ebook, User, Section, Request, ReadBook, Feedback
from .auth import librarian_required, user_required
from flask import jsonify
from flask_restful import abort
from datetime import datetime, timedelta
from sqlalchemy import or_



#         Section API         #

section_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'description': fields.String,
    'created_at': fields.DateTime,
    'ebooks': fields.List(fields.Nested({
        'id': fields.Integer,
        'title': fields.String,
        'authors': fields.String,
        'content': fields.String,
        'rating': fields.Float,
        'total_ratings': fields.Integer,
        'total_borrows': fields.Integer,
        'sections': fields.List(fields.Nested({
            'id': fields.Integer,
            'name': fields.String,
        })),
        'created_at': fields.DateTime,
    }))
}

section_parser = reqparse.RequestParser()
section_parser.add_argument('name', type=str, required=True, help='Name is required')
section_parser.add_argument('description', type=str)


class SectionListAPI(Resource):
    def get(self):
        sections = Section.query.all()
        result = []
        for section in sections:
            section_data = marshal(section, section_fields)
            section_data['ebooks'] = marshal(section.ebooks, ebook_fields)
            result.append(section_data)
        return result, 200

    @jwt_required()
    @librarian_required
    def post(self):
        args = section_parser.parse_args()

        # Check if a section with the given name already exists
        existing_section = Section.query.filter_by(name=args['name']).first()
        if existing_section:
            return {'message': 'A section with this name already exists'}, 400

        new_section = Section(
            name=args['name'],
            description=args.get('description')
        )
        db.session.add(new_section)
        db.session.commit()

        return marshal(new_section, section_fields), 201


class SectionAPI(Resource):
    @marshal_with(section_fields)
    def get(self, section_id):
        section = Section.query.get_or_404(section_id)
        return section, 200

    @jwt_required()
    @librarian_required
    @marshal_with(section_fields)
    def put(self, section_id):
        section = Section.query.get_or_404(section_id)
        args = section_parser.parse_args()
        section.name = args['name']
        section.description = args.get('description')
        db.session.commit()
        return section, 200

    @jwt_required()
    @librarian_required
    def delete(self, section_id):
        section = Section.query.get_or_404(section_id)

        # Check if the section has any books
        if section.ebooks:
            return {'message': 'Cannot delete section. It still contains books.'}, 400

        try:
            db.session.delete(section)
            db.session.commit()
            return {'message': 'Section deleted successfully'}, 200
        except Exception as e:
            db.session.rollback()
            return {'message': f'An error occurred while deleting the section: {str(e)}'}, 500


ebook_fields = {
    'id': fields.Integer,
    'title': fields.String,
    'authors': fields.String,
    'content': fields.String,
    'rating': fields.Float,
    'total_ratings': fields.Integer,
    'total_borrows': fields.Integer,
    'sections': fields.List(fields.Nested({
        'id': fields.Integer,
        'name': fields.String,
    })),
    'created_at': fields.DateTime,
}

ebook_parser = reqparse.RequestParser()
ebook_parser.add_argument('title', type=str, required=True, help='Title is required')
ebook_parser.add_argument('authors', type=str, required=True, help='Authors are required')
ebook_parser.add_argument('content', type=str, required=True, help='Content is required')
ebook_parser.add_argument('section_ids', type=list, required=True, help='Section IDs are required')


class EbookListAPI(Resource):
    @marshal_with(ebook_fields)
    def get(self):
        # Here the limit is 5, because I am using it to show the 5 most recent books only
        ebooks = Ebook.query.order_by(Ebook.created_at.desc()).limit(5).all()
        return ebooks, 200

    @jwt_required()
    @librarian_required
    def post(self):
        data = request.get_json()
        ebook = Ebook.query.filter_by(title=data['title']).first()
        if ebook:
            return {'message': 'A book with this title already exists'}, 400

        if not data['section_ids'] or len(data['section_ids']) == 0:
            abort(400, message="At least one section must be selected")

        if data['section_ids'] is None:
            return {'message': 'Section IDs are required'}, 400

        new_ebook = Ebook(title=data['title'], authors=data['authors'], content=data['content'],
                          section_ids=data['section_ids'])

        db.session.add(new_ebook)
        db.session.commit()

        return marshal(new_ebook, ebook_fields), 201


class EbookAPI(Resource):
    @jwt_required()
    def get(self, ebook_id):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        ebook = Ebook.query.get_or_404(ebook_id)

        if user.is_librarian:
            # Librarians have access to all books
            return marshal(ebook, ebook_fields), 200

        # For regular users, if they have an approved request
        request = Request.query.filter_by(user_id=user_id, ebook_id=ebook_id, status='granted').first()

        if not request:
            return {'message': 'You do not have access to this book'}, 403

        return marshal(ebook, ebook_fields), 200

    @jwt_required()
    @librarian_required
    def put(self, ebook_id):
        ebook = Ebook.query.get_or_404(ebook_id)
        data = request.get_json()

        if not data:
            return {'message': 'No input data provided'}, 400

        ebook.title = data.get('title', ebook.title)
        ebook.authors = data.get('authors', ebook.authors)
        ebook.content = data.get('content', ebook.content)

        if 'section_ids' in data:
            new_sections = []
            for section_id in data['section_ids']:
                section = Section.query.get(section_id)
                if section:
                    new_sections.append(section)
                else:
                    return {'message': f'Section with id {section_id} not found'}, 400
            ebook.sections = new_sections

        try:
            db.session.commit()
            return marshal(ebook, ebook_fields), 200
        except Exception as e:
            db.session.rollback()
            return {'message': f'An error occurred while updating the ebook: {str(e)}'}, 500

    @jwt_required()
    @librarian_required
    def delete(self, ebook_id):
        ebook = Ebook.query.get_or_404(ebook_id)
        try:
            db.session.delete(ebook)
            db.session.commit()
            return {'message': 'Ebook deleted successfully'}, 200
        except Exception as e:
            db.session.rollback()
            return {'message': f'An error occurred while deleting the ebook: {str(e)}'}, 500



# Request API
request_fields = {
    'id': fields.Integer,
    'status': fields.String,
    'request_date': fields.DateTime,
    'issue_date': fields.DateTime,
    'return_date': fields.DateTime,
    'due_date': fields.DateTime,
    'user_id': fields.Integer,
    'user_name': fields.String(attribute=lambda x: x.user.name),
    'ebook_id': fields.Integer,
    'ebook_title': fields.String(attribute=lambda x: x.ebook.title),
    'ebook_author': fields.String(attribute=lambda x: x.ebook.authors)
}

request_parser = reqparse.RequestParser()
request_parser.add_argument('status', type=str, required=True)


class RequestListAPI(Resource):
    @jwt_required()
    @librarian_required
    def get(self):
        requests = Request.query.all()
        return marshal(requests, request_fields), 200

    @jwt_required()
    @user_required
    def post(self):
        user_id = get_jwt_identity()
        user = User.query.get_or_404(user_id)
        data = request.get_json()
        ebook_id = data.get('ebook_id')

        if not ebook_id:
            return {'message': 'Ebook ID is required'}, 400

        ebook = Ebook.query.get_or_404(ebook_id)

        active_requests = Request.query.filter(
            Request.user_id == user_id,
            Request.status.in_(['pending', 'granted'])
        ).count()

        if active_requests >= 5:
            return {'message': 'You have reached the maximum limit of active requests'}, 400

        existing_request = Request.query.filter_by(
            user_id=user_id, ebook_id=ebook_id, status='pending'
        ).first()

        if existing_request:
            return {'message': 'A request for this book is already pending'}, 400

        new_request = Request(user_id=user_id, ebook_id=ebook_id)
        db.session.add(new_request)
        db.session.commit()

        return marshal(new_request, request_fields), 201


class RequestAPI(Resource):
    @jwt_required()
    @marshal_with(request_fields)
    def get(self, request_id):
        user_id = get_jwt_identity()
        user = User.query.get_or_404(user_id)
        request_obj = Request.query.get_or_404(request_id)

        if user.is_librarian or request_obj.user_id == user_id:
            return request_obj, 200
        else:
            return {'message': 'Unauthorized'}, 403

    @jwt_required()
    @librarian_required
    def put(self, request_id):
        request_obj = Request.query.get_or_404(request_id)
        data = request.get_json()
        new_status = data.get('status')

        if new_status not in ['pending', 'granted', 'returned', 'revoked']:
            return {'message': 'Invalid status'}, 400

        request_obj.status = new_status

        if new_status == 'granted':
            request_obj.issue_date = datetime.utcnow()
            request_obj.due_date = datetime.utcnow() + timedelta(days=14)  # Set due date to 14 days from now
        elif new_status in ['returned', 'revoked']:
            request_obj.return_date = datetime.utcnow()

        db.session.commit()
        return marshal(request_obj, request_fields), 200


class UserRequestsAPI(Resource):
    @jwt_required()
    @user_required
    @marshal_with(request_fields)
    def get(self):
        user_id = get_jwt_identity()
        requests = Request.query.filter_by(user_id=user_id).all()
        return requests, 200


# ReadBook API
read_book_fields = {
    'id': fields.Integer,
    'read_date': fields.DateTime,
    'user_id': fields.Integer,
    'ebook_id': fields.Integer,
    'request_id': fields.Integer
}

read_book_parser = reqparse.RequestParser()
read_book_parser.add_argument('user_id', type=int, required=True)
read_book_parser.add_argument('ebook_id', type=int, required=True)
read_book_parser.add_argument('request_id', type=int, required=True)


class ReadBookListAPI(Resource):
    @jwt_required()
    @user_required
    @marshal_with(read_book_fields)
    def get(self, user_id):
        user = User.query.get_or_404(user_id)
        return ReadBook.query.filter_by(user_id=user_id).all(), 200

    @jwt_required()
    @user_required
    def post(self):
        args = read_book_parser.parse_args()
        new_read_book = ReadBook(
            user_id=args['user_id'],
            ebook_id=args['ebook_id'],
            request_id=args['request_id']
        )
        db.session.add(new_read_book)
        db.session.commit()
        return marshal(new_read_book, read_book_fields), 201


# Feedback API
feedback_fields = {
    'id': fields.Integer,
    'content': fields.String,
    'created_at': fields.DateTime,
    'user_id': fields.Integer,
    'ebook_id': fields.Integer,
    'rating': fields.Integer
}

feedback_parser = reqparse.RequestParser()
feedback_parser.add_argument('content', type=str, required=True, help='Feedback content is required')
feedback_parser.add_argument('ebook_id', type=int, required=True, help='Ebook ID is required')
feedback_parser.add_argument('rating', type=int, required=True, help='Rating is required')


class FeedbackAPI(Resource):
    @jwt_required()
    @user_required
    @marshal_with(feedback_fields)
    def post(self):
        args = feedback_parser.parse_args()
        user_id = get_jwt_identity()

        user = User.query.get_or_404(user_id)
        ebook = Ebook.query.get_or_404(args['ebook_id'])

        feedback = Feedback.query.filter_by(user_id=user_id, ebook_id=ebook.id).first()
        if feedback:
            return {'message': "feedback already exists"}, 400

        new_feedback = Feedback(
            content=args['content'],
            user_id=user_id,
            ebook_id=args['ebook_id'],
            rating=args['rating']
        )

        db.session.add(new_feedback)

        # Update ebook rating and borrow count
        ebook.total_ratings += 1
        ebook.total_borrows += 1
        ebook.rating = ((ebook.rating * (ebook.total_ratings - 1)) + args['rating']) / ebook.total_ratings

        db.session.commit()

        return new_feedback, 201

    @marshal_with(feedback_fields)
    def get(self, ebook_id):
        feedbacks = Feedback.query.filter_by(ebook_id=ebook_id).all()
        return feedbacks, 200


class RequestStatusAPI(Resource):
    @jwt_required()
    @user_required
    def get(self, book_id):
        user_id = get_jwt_identity()
        user = User.query.get_or_404(user_id)

        request = Request.query.filter_by(user_id=user_id, ebook_id=book_id).order_by(
            Request.request_date.desc()).first()

        if request:
            return jsonify({"status": request.status}, 200)
        else:
            return jsonify({"status": "not_requested"})


class StatisticsAPI(Resource):
    @jwt_required()
    @librarian_required
    def get(self):
        active_users = User.query.filter(User.is_active == True).count() - 1
        pending_requests = Request.query.filter_by(status='pending').count()
        ebooks_issued = Request.query.filter_by(status='granted').count()
        ebooks_revoked = Request.query.filter_by(status='revoked').count()

        return {
            'activeUsers': active_users,
            'pendingRequests': pending_requests,
            'ebooksIssued': ebooks_issued,
            'ebooksRevoked': ebooks_revoked
        }, 200


class SearchAPI(Resource):
    @jwt_required()
    def get(self):
        query = request.args.get('q', '')
        if not query:
            return {'message': 'No search query provided'}, 400

        # Search for matching ebooks
        ebooks = Ebook.query.join(Ebook.sections).filter(
            or_(
                Ebook.title.ilike(f'%{query}%'),
                Ebook.authors.ilike(f'%{query}%'),
                Section.name.ilike(f'%{query}%')
            )
        ).distinct().all()

        results = marshal(ebooks, ebook_fields)

        return results, 200


class ReturnBookAPI(Resource):
    @jwt_required()
    @user_required
    def post(self, request_id):
        request = Request.query.get_or_404(request_id)
        user_id = get_jwt_identity()

        if request.user_id != user_id:
            return {'message': 'You are not authorized to return this book'}, 403

        if request.status != 'granted':
            return {'message': 'This book is not currently borrowed by you'}, 400

        request.status = 'returned'
        request.return_date = datetime.utcnow()

        # Create a new ReadBook entry
        read_book = ReadBook(
            user_id=user_id,
            ebook_id=request.ebook_id,
            request_id=request.id
        )

        db.session.add(read_book)
        db.session.commit()

        return {'message': 'Book returned successfully'}, 200


class ReturnedBooksAPI(Resource):
    @jwt_required()
    @user_required
    def get(self):
        user_id = get_jwt_identity()
        returned_revoked_books = Request.query.filter(
            Request.user_id == user_id,
            Request.status.in_(['returned', 'revoked'])
        ).all()
        
        result = []
        for request in returned_revoked_books:
            book_data = {
                'id': request.id,
                'ebook_id': request.ebook_id,
                'ebook_title': request.ebook.title,
                'ebook_author': request.ebook.authors,
                'return_date': str(request.return_date),
                'status': request.status
            }
            result.append(book_data)
        
        return result, 200


class UserFeedbackAPI(Resource):
    @jwt_required()
    @user_required
    def get(self):
        user_id = get_jwt_identity()
        feedbacks = Feedback.query.filter_by(user_id=user_id).all()
        return marshal(feedbacks, feedback_fields), 200
