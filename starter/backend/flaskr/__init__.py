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

# return success obj
# --------------------
def success_obj():
    return jsonify({ "success": True,
             "body": "hello",
           })

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
    qresults['success'] = True
    # app.logger.info("results for questions %d", len(qresults['questions']))
    return jsonify(qresults)


#----------------------------------------------------------------------------#
#  Given a Search Term, Return a Lower Case Version, Enclosed with %
#----------------------------------------------------------------------------#
def get_term(term):    
  term_lower = term.lower()
  term_lower = '%' + term_lower + '%'
  return term_lower

#  Format a Question

def format_question(question):
  return {'id': question.id,
          'question': question.question,
          'answer': question.answer,
          'difficulty': question.difficulty,
          'category': question.category }   
         

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
#   cors = CORS(app)

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
      categories = {'categories': cat_obj}
      return jsonify(categories)



  @app.route('/categories/<int:id>/questions')
  def get_questions_by_cat(id):
      page = request.args.get('page', 1, type=int)

      questions = Question.query.filter_by(category=id).all()

      return get_questions_package(page, questions)



  @app.route('/questions')
  def get_questions():
      page = request.args.get('page', 1, type=int)

      questions = Question.query.all()

      return get_questions_package(page, questions)

  # @app.route('/questions/search', methods=['OPTIONS'])          
  # def handle_options():
  #     app.logger.info("options here")
  #     return success_obj()

  @app.route('/questions/search', methods=['POST'])
  def search_questions():
      app.logger.info("in /questions/search")
      if not request.json or not 'searchTerm' in request.json:
          abort(400)

      page = request.args.get('page', 1, type=int)  # change for POST

      data = request.get_json('searchTerm')
      term = data['searchTerm']
      search_term = get_term(term)

      error = False
      try:
        questions = Question.query.filter(Question.question.ilike(search_term)).all()
      except:
        error = True
        app.logger.info("error occurred on search, aborting...")

      if error:
          abort(422)
      
      
      return get_questions_package(page, questions), 201
    
  '''
  @TODO: (done)
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
  @TODO:  (done)
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


  @app.route('/quizzes', methods=['POST'])
  def get_quiz_question():
    # given category, previous questions, return a random remaining question from the category

    ## WHAT HAPPENS IF ALL IS SELECTED?

    app.logger.info("in /quizzes")
    if not request.json or not 'previous_questions' in request.json:
        abort(400)  

    quiz_cat = request.json['quiz_category']
    quiz_category_id = quiz_cat['id']

    previous_questions = request.get_json()['previous_questions']
    # app.logger.info("previous_questions was %s", quiz_cat)    

    # app.logger.info("previous_questions was %s", previous_questions)    

    if previous_questions is None:
      previous_questions = []

    error = False
    try:
        if quiz_category_id == 0:
          questions = Question.query.filter(~Question.id.in_(previous_questions)).all()
          tot_questions = len(Question.query.all())
        else:  
          questions = Question.query.filter(Question.category==quiz_category_id).filter(~Question.id.in_(previous_questions)).all()
          tot_questions = len(Question.query.filter(Question.category==quiz_category_id).all())

    except:
        error = True
        app.logger.info("error occurred on querying for quiz data, aborting...")

    if error:
        abort(422)
    else:
        result = {}
        if len(questions) == 0:
            result['question'] = jsonify({'id': 0,
                                          'question': '',
                                          'answer': '',
                                          'difficulty': -1,
                                          'category': 0})
            return jsonify(result)
            
        result['total_questions'] = tot_questions
        if len(questions) > 1:
            rand_idx = random.randint(0, len(questions)-1)
            result['question'] = format_question(questions[rand_idx])

            return jsonify(result)
        else:
            result['question'] = format_question(questions[0])
            return jsonify(result)

  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  @app.errorhandler(404)
  def not_found(error):
      return jsonify({
          "success": False,
          "error": 404,
          "message": "Not found"
      }), 404

  @app.errorhandler(422)
  def cannot_process(error):
      return jsonify({
          "success": False,
          "error": 422,
          "message": "Something wrong; cannot process"
      }), 422

  @app.errorhandler(400)
  def cannot_process(error):
      return jsonify({
          "success": False,
          "error": 400,
          "message": "400: Bad request"
      }), 400
  return app

