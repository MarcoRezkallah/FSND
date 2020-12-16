import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category, db

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET, POST, PUT, PATCH, Delete, OPTIONS')
        return response

    @app.route('/categories')
    def GET_categorys():
        categoriesQuery = Category.query.all()
        categories = [categorie.format() for categorie in categoriesQuery]
        categoriesDict = {}
        for cat in categories:
            categoriesDict[cat['id']] = cat['type']

        return jsonify(categoriesDict)

    @app.route('/questions')
    def GET_questions():
        clientpage = request.args.get('page', type=int, default=1)
        if clientpage < 1:
            abort(404)
        page = clientpage - 1
        limit = request.args.get('limit', type=int, default=10)

        if limit < 1:
            abort(416)

        count = Question.query.count()

        offset = page * limit
        if offset > count:
            abort(416)

        questionsQuery = Question.query.limit(limit).offset(offset).all()
        questions = [question.format() for question in questionsQuery]

        categoriesQuery = Category.query.all()
        categories = [categorie.format() for categorie in categoriesQuery]
        categoriesDict = {}
        for cat in categories:
            categoriesDict[cat['id']] = cat['type']

        result = {
            "questions": questions,
            "total_questions": count,
            "categories": categoriesDict,
        }

        return jsonify(result)

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def DELETE_questions(question_id):
        try:
            result = Question.query.filter_by(id=question_id).delete()
            db.session.commit()
            if result < 1:
                abort(404)
        except Exception as e:
            abort(500)
        return jsonify(result)

    @app.route('/questions', methods=['POST'])
    def POST_questions():
        data = request.get_json()

        try:
            q = Question(data['question'], data['answer'],
                         data['category'], data['difficulty'])
            q.insert()
        except Exception as e:
            abort(500)
        return jsonify(q.format())

    @app.route('/questions/search', methods=['POST'])
    def SEARCH_questions():
        data = request.get_json()

        count = Question.query.count()

        questionsQuery = Question.query.filter(
            Question.question.ilike('%{}%'.format(data['searchTerm']))).all()
        questions = [question.format() for question in questionsQuery]

        result = {
            "questions": questions,
            "total_questions": count,
        }

        return jsonify(result)

    @app.route('/categories/<int:category_id>/questions')
    def GET_category_questions(category_id):
        count = Question.query.count()
        questionsQuery = Question.query.filter_by(
            category='{}'.format(category_id)).all()
        print(questionsQuery)
        questions = [question.format() for question in questionsQuery]
        result = {
            "questions": questions,
            "total_questions": count,
        }
        return jsonify(result)

    '''
    @TODO: 
    Create a POST endpoint to get questions to play the quiz. 
    This endpoint should take category and previous question parameters 
    and return a random questions within the given category, 
    if provided, and that is not one of the previous questions. 

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not. 
    '''

    '''
    @TODO: 
    Create error handlers for all expected errors 
    including 404 and 422. 
    '''
    return app
