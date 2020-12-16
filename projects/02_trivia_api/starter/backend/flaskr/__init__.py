import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy import func

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

    @app.route('/quizzes', methods=['POST'])
    def POST_quizzes():
        data = request.get_json()

        questionsQuery = Question.query

        if(data['quiz_category']['id'] > 0):
            questionsQuery = questionsQuery.filter(
                Question.category == '{}'.format(data["quiz_category"]["id"]))

        questionsQuery = questionsQuery.filter(
            Question.id.notin_(data['previous_questions'])).order_by(func.random()).limit(1).all()

        question = questionsQuery[0].format() if len(
            questionsQuery) > 0 else None

        return jsonify({
            "question": question
        })
    
    return app
