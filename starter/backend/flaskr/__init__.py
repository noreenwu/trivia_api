import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
import logging
from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

# ------------------------------------------------------------------------------
#  Retrieve the categories from the database and return them in an object format
# ------------------------------------------------------------------------------
def get_all_categories():
  categories = Category.query.all()
  i = 1
  cat_obj = {}
  for c in categories:
    cat_obj[i] = c.type
    i = i+1
  return cat_obj

# ------------------------------------------------------------------------------
#  Given array of Question objects, return object, using index as key
# ------------------------------------------------------------------------------
def get_all_questions(questions):
  i = 1
  q_obj = {}
  for q in questions:
    q_obj[i] = { 'id': q.id, 
                'question': q.question,
                'answer': q.answer,
                'difficulty': q.difficulty,
                'category': q.category }
    i = i + 1    
  return q_obj  

def get_questions_package(page, questions):
  startIdx = (page-1) * QUESTIONS_PER_PAGE    
  # app.logger.info("total questions %d",len(questions))

  if startIdx > len(questions):
    # app.logger.info("startIdx ")
    # app.logger.info("questions length %d", len(questions))
    return jsonify({0: 'empty'})   # actually return other info and only questions would be empty

  else:
    endIdx = (page * QUESTIONS_PER_PAGE)

    endIdx = min(endIdx, len(questions))          
    # app.logger.info("and the ending index is %d", endIdx)

    thisPageQuestions = questions[startIdx:endIdx]
    num_questions_this_page = len(thisPageQuestions)
    # app.logger.info("thispagequestions is %d", num_questions_this_page)

    q_obj = {}
    q_obj = get_all_questions(thisPageQuestions)

    qresults = {}
    qresults['questions'] = q_obj
    qresults['total_questions'] = len(questions)
    qresults['categories'] = get_all_categories()
    # app.logger.info("results for questions %d", len(qresults['questions']))
    return jsonify(qresults)


def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  app.logger.info("hello")

  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
#   cors = CORS(app, resources={r"/questions/*": {"origins": "*"}})
  cors = CORS(app, resources={r"/*": {"origins": "*"}})

  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
      response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
      response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
      return response

  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/messages')
  def get_messages():
      return 'Hello, messages'

  @app.route('/categories')
#   @cross_origin
  def get_categories():
      categories = Category.query.all()

    #   str = ""
      i = 1
      cat_obj = {}
      for c in categories:
        #  str = str + ' ' + c.type
         cat_obj[i] = c.type
         i = i+1
      app.logger.info(cat_obj)
      return jsonify(cat_obj)







  @app.route('/categories/<int:id>/questions')
  def get_questions_by_cat(id):
      page = request.args.get('page', 1, type=int)


      questions = Question.query.filter_by(category=id).all()
      
      return get_questions_package(page, questions)
    #   startIdx = (page-1) * QUESTIONS_PER_PAGE    
    #   app.logger.info("total questions %d",len(questions))

    #   if startIdx > len(questions):
    #       app.logger.info("startIdx ")
    #       app.logger.info("questions length %d", len(questions))
    #       return jsonify({0: 'empty'})

    #   else:
    #       app.logger.info("getting questions startIdx %d", startIdx)
    #       endIdx = (page * QUESTIONS_PER_PAGE)

    #       endIdx = min(endIdx, len(questions))          
    #       app.logger.info("and the ending index is %d", endIdx)

    #       thisPageQuestions = questions[startIdx:endIdx]
    #       num_questions_this_page = len(thisPageQuestions)
    #       app.logger.info("thispagequestions is %d", num_questions_this_page)
    #       q_obj = {}
    #       i = 1
    #       for q in thisPageQuestions:
    #           q_obj[i] = q.question
    #           i = i + 1
    #       results = {}              
    #       results['questions'] = q_obj 
    #       results['total_questions'] = num_questions_this_page
    #       results['currentCategory'] = id
    #       return jsonify(results)


  @app.route('/questions')
  def get_questions():
      page = request.args.get('page', 1, type=int)

      questions = Question.query.all()

      return get_questions_package(page, questions)

          

  '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''

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

