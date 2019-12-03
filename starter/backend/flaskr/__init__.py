import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
import logging
from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 6
MOST_DIFFICULT_RATING = 5


# ------------------------------------------------------------------------------
#  Retrieve the categories from the database and return them in an object format.
#  This is typically called from an endpoint that needs to return categories
#  as part of its results, such as /questions
# ------------------------------------------------------------------------------
def get_all_categories():

  error = False
  try: 
    categories = Category.query.all()
  except:
    error = True

  if error:
    abort(422)

  i = 1
  cat_obj = {}
  for c in categories:
    cat_obj[i] = c.type
    i = i+1
    
  return cat_obj


# ------------------------------------------------------------------------------
#  Is valid category: return True if the supplied category id exists in the db
# ------------------------------------------------------------------------------
def is_valid_category(id):

  error = False
  try: 
    categories = Category.query.all()
  except:
    error = True
      
  if error:
    abort(422)    

  catList = []
  for cat in categories:
    catList.append(cat.id)

  if id in catList:
    return True
  else:
    return False


# ------------------------------------------------------------------------------
#  Given array of Question objects, return object, using index as key
# ------------------------------------------------------------------------------
def format_question_array(questions):
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
    return jsonify({ "success": True })
                 

# ------------------------------------------------------------------
#  is_valid_difficulty: Is the difficulty rating between 1 and MOST_DIFFICULT_RATING
# ------------------------------------------------------------------
def is_valid_difficulty(rating):
  if rating > 0 and rating <= MOST_DIFFICULT_RATING:
    return True
  return False  


# ------------------------------------------------------------------
#  get_questions_package: Several endpoints utilize this general questions packager.
#  The endpoints for getting (/questions), questions by category
#  (/categories/<int:id>/questions) and search for question
#  (/questions/search) all retrieve different batches of questions,
#  and then those questions need to be packaged by specified page
#  into a json object. That work is done here
# ------------------------------------------------------------------
def get_questions_package(page, questions, cat):
  startIdx = (page-1) * QUESTIONS_PER_PAGE    

  if startIdx > len(questions):
    abort(404)

  else:
    endIdx = (page * QUESTIONS_PER_PAGE)

    endIdx = min(endIdx, len(questions))          

    thisPageQuestions = questions[startIdx:endIdx]
    num_questions_this_page = len(thisPageQuestions)

    q_obj = {}
    q_obj = format_question_array(thisPageQuestions)

    qresults = { 'questions': q_obj,
                 'total_questions': len(questions),
                 'categories': get_all_categories(),
                 'currentCategory': cat,                
                 'success': True }


    return jsonify(qresults)


#----------------------------------------------------------------------------
#  get_term: given a Search Term, return a lower case version, enclosed with %
#----------------------------------------------------------------------------
def get_term(term):    
  term_lower = term.lower()
  term_lower = '%' + term_lower + '%'
  return term_lower


# ----------------------------------------------------------------------------
#  format_question: Put a Question returned from the database into key:value format
# ----------------------------------------------------------------------------
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
  db = SQLAlchemy(app)

 
  cors = CORS(app, resources={r"/*": {"origins": "*"}})


  @app.after_request
  def after_request(response):
      # response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
      response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
      return response

#------------------------------------------------------------------------------------------
#  The endpoint /categories (GET) returns an object of all available categories.
#------------------------------------------------------------------------------------------
  @app.route('/categories')
  def get_categories():

      error = False
      try:
        categories = Category.query.all()
      except:
        error = True


      if error:
        abort(422)  

      i = 1
      cat_obj = {}
      for c in categories:
         cat_obj[i] = c.type
         i = i+1
      app.logger.info(cat_obj)
      categories = {'categories': cat_obj}
      return jsonify(categories)


# -------------------------------------------------------------------------------------------
#  /categories/<int:id>/questions (GET) returns the questions that will appear 
#  on the specified page. There are 10 pages per question (const defined above)
# -------------------------------------------------------------------------------------------
  @app.route('/categories/<int:id>/questions')
  def get_questions_by_cat(id):
      page = request.args.get('page', 1, type=int)

      error = False
      if not is_valid_category(id):
        abort(404)

      try:
        questions = Question.query.filter_by(category=id).all()
      except:
        error = True

      if error:
        abort(404)

      return get_questions_package(page, questions, id)


# -------------------------------------------------------------------------------------------
#  /questions (GET) returns questions from all categories that will appear on the specified page
# -------------------------------------------------------------------------------------------
  @app.route('/questions')
  def get_questions():
      page = request.args.get('page', 1, type=int)

      questions = Question.query.all()

      return get_questions_package(page, questions, None)


# -------------------------------------------------------------------------------------------
#  /questions/search (POST) returns questions that include the user-provided search term. 
#  Both the search term and the question are lowercased to ignore case.
# -------------------------------------------------------------------------------------------
  @app.route('/questions/search', methods=['POST'])
  def search_questions():


      if not request.json or not 'searchTerm' in request.json:
          abort(400)

      if not 'page' in request.json:
        page = 1
      else:
        page = request.get_json()['page']

      term = request.get_json()['searchTerm']

      search_term = get_term(term)

      error = False
      try:
        questions = Question.query.filter(Question.question.ilike(search_term)).all()
      except:
        error = True
        app.logger.info("error occurred on search, aborting...")

      if error:
          abort(422)
      
      
      return get_questions_package(page, questions, None)
    

# -------------------------------------------------------------------------------------------
#  /questions/<int:id> (DELETE) retrieves the question specified by id in the url and
#  deletes it from the database
# -------------------------------------------------------------------------------------------
  @app.route('/questions/<int:id>', methods=['DELETE'])
  def delete_question(id):

    error = False
    try:
      the_question = Question.query.filter_by(id=id).first()
      the_question.delete()
      app.logger.info("deleting %s", the_question.question)
      # db.session.delete(the_question)
      db.session.commit()
    except:
      error = True
      app.logger.info("error occurred while trying to delete a question. Sorry...")

    if error:
      abort(422)      

    return success_obj()


# -------------------------------------------------------------------------------------------
#  /questions/add (POST) accepts new question text, new answer text and difficulty 
#  and category from the Add Question form in the user interface. If not all the 
#  data is provided, then an error type 400 is returned, otherwise the new question is added
# -------------------------------------------------------------------------------------------
  @app.route('/questions/add', methods=['POST'])
  def add_new_questions():

    question_text = request.get_json()['question']
    answer_text = request.get_json()['answer']
    difficulty_rating = int(request.get_json()['difficulty'])
    category_setting = int(request.get_json()['category'])

    have_all_data = False
    if question_text.strip() and answer_text.strip() and is_valid_difficulty(difficulty_rating) and is_valid_category(category_setting):
      have_all_data = True


    if not request.json or not have_all_data:
        abort(400)    

    error = False
    try:
      # insert new question into db
      new_question = Question(question=question_text,answer=answer_text,
                              difficulty=difficulty_rating,category=category_setting)

      db.session.add(new_question)                              
      db.session.commit()
      return success_obj()
    except:
      error = True
      app.logger.info("error occurred in adding a new question, aborting...")

    if error:
        abort(422)


# -------------------------------------------------------------------------------------------
#  /quizzes (POST) returns a random question from the specified category (or from the
#  general pool of questions if ALL is specified). Questions that have already been
#  posed this session are omitted; they are passed in as previous_questions from the front-end
# -------------------------------------------------------------------------------------------
  @app.route('/quizzes', methods=['POST'])
  def get_quiz_question():
    # given category and list of previous question ids, return a random remaining question from the category

    app.logger.info("in /quizzes")
    if not request.json or not 'previous_questions' in request.json:
        abort(400)  

    quiz_cat = request.json['quiz_category']
    quiz_category_id = quiz_cat['id']

    previous_questions = request.get_json()['previous_questions']

    if previous_questions is None:
      previous_questions = []

    error = False
    try:
        if quiz_category_id == 0:  # if user selects All categories
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

# ---------------------------------------------------------------------------
#  If user specifies a page beyond which there are questions, return a 404
#  There is nothing defined at localhost:5000/, so that also returns 404
# ---------------------------------------------------------------------------
  @app.errorhandler(404)
  def not_found(error):
      return jsonify({
          "success": False,
          "error": 404,
          "message": "Resource not found"
      }), 404

# ---------------------------------------------------------------------------
# This error is triggered if something faulty happened on the server side,
# such as not being able to make a database request
# ---------------------------------------------------------------------------
  @app.errorhandler(422)
  def cannot_process(error):
      return jsonify({
          "success": False,
          "error": 422,
          "message": "Something wrong; cannot process"
      }), 422

# ---------------------------------------------------------------------------
# This is an error caused by improper use of an endpoint, or insufficient
# or incorrect input values, such as an blank question text when creating a question
# ---------------------------------------------------------------------------
  @app.errorhandler(400)
  def cannot_process(error):
      return jsonify({
          "success": False,
          "error": 400,
          "message": "400: Bad request"
      }), 400
  return app

