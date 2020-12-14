import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

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
        cats = Category.query.all()
        return jsonify([cat.format() for cat in cats])

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
            result = Question.filterBy(id=question_id).delete()
        except:
            abort(500)

        return result

    '''
    @TODO: 
    Create an endpoint to DELETE question using a question ID. 

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page. 
    '''

    '''
    @TODO: 
    Create an endpoint to POST a new question, 
    which will require the question and answer text, 
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab, 
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.  
    '''

    '''
    @TODO: 
    Create a POST endpoint to get questions based on a search term. 
    It should return any questions for whom the search term 
    is a substring of the question. 

    TEST: Search by any phrase. The questions list will update to include 
    only question that include that string within their question. 
    Try using the word "title" to start. 
    '''

    '''
    @TODO: 
    Create a GET endpoint to get questions based on category. 

    TEST: In the "List" tab / main screen, clicking on one of the 
    categories in the left column will cause only questions of that 
    category to be shown. 
    '''

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
