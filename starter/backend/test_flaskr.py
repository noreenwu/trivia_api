import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = (
            "postgres://{}/{}"
            .format('localhost:5432', self.database_name)
        )
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    # test getting categories
    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])

    # test getting category with wrong endpoint
    def test_get_category_404(self):
        res = self.client().get('/category')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)

    # test getting a page of questions
    def test_get_paginated_questions(self):
        res = self.client().get('/questions?page=2')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['categories'])
        self.assertTrue(data['questions'])

    # test requesting a page beyond the number of possible pages returns 404
    def test_404_sent_requesting_beyond_valid_page(self):
        res = self.client().get('/questions?page=100')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')

    # test getting a page of questions by category
    def test_get_paginated_questions_by_category(self):
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['categories'])
        self.assertTrue(data['questions'])

    # test getting a page of questions by invalid category
    def test_get_paginated_questions_by_invalid_category(self):
        res = self.client().get('/categories/12/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    # test searching for a question
    def test_search_question(self):
        res = self.client().post('/questions/search',
                                 json={'searchTerm': 'Tom',
                                       'page': 1})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['categories'])
        self.assertTrue(data['questions'])

    # test searching for a question with no results and no specified page
        res = (
            self.client()
            .post('/questions/search',
                  json={'searchTerm': 'zoology'})
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    # test searching for a question with no searchTerm
        res = self.client().post('/questions/search')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)

    # test creation of a new question
    def test_create_question(self):
        res = (
            self.client()
                .post('/questions/add',
                      json={'question': 'test question?',
                            'answer': 'test answer',
                            'category': 1,
                            'difficulty': 1})
        )
        data = json.loads(res.data)
        question = (
            Question.query
                    .filter_by(question="test question?")
                    .filter_by(answer="test answer")
                    .first()
        )
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    # test blank question returns 400
    def test_incomplete_create_question(self):
        res = self.client().post('/questions/add', json={'question': '',
                                                         'answer': 'answered',
                                                         'category': 1,
                                                         'difficulty': 1})

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)

    # test blank answer returns 400
    def test_incomplete_create_question2(self):
        res = (
            self.client()
                .post('/questions/add',
                      json={'question': 'question with no answer',
                            'answer': '',
                            'category': 1,
                            'difficulty': 1})
        )

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)

    # test bad category returns 400
    def test_incorrect_create_question(self):
        res = (
            self.client()
                .post('/questions/add',
                      json={'question': 'question with no category',
                            'answer': 'answer but no category',
                            'category': -1,
                            'difficulty': 1})
        )

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)

    # test bad difficulty rating returns 400
    def test_incorrect_create_question2(self):
        res = (
            self.client()
                .post('/questions/add',
                      json={'question': 'question with bad difficulty rating',
                            'answer': 'answer bad difficulty rating',
                            'category': 1,
                            'difficulty': -1})
        )

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)

    # test deletion of a question that exists
    def test_delete_question(self):
        res = self.client().delete('/questions/10')
        data = json.loads(res.data)

        question = Question.query.filter(Question.id == 10).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(question, None)

    # test deletion of a question that does not exist
    def test_delete_nonexistent_question(self):
        res = self.client().delete('/questions/1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad request')

    # test getting a quiz, no previous questions
    def test_get_quiz(self):
        res = (
            self.client()
                .post('/quizzes',
                      json={'previous_questions': [],
                            'quiz_category': {'type': 'Science', 'id': 1}})
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['question'])

    # test getting a quiz without sending previous questions
    def test_get_quiz_without_previous_questions(self):
        res = (
            self.client()
                .post('/quizzes',
                      json={'quiz_category': {'type': 'Science', 'id': 1}})
        )

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)

    # test getting a quiz, no quiz category
    def test_get_quiz(self):
        res = self.client().post('/quizzes', json={'previous_questions': []})

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
