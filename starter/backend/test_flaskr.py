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
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
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

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.


    """
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


    # test creation of a new question
    def test_create_question(self):
        res = self.client().post('/questions/add', json={ 'question': 'test question?',
                                                          'answer': 'test answer',
                                                          'category': 1,
                                                          'difficulty': 1} )
        data = json.loads(res.data)
        question = Question.query.filter_by(answer="calf").first()

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
        res = self.client().post('/questions/add', json={'question': 'question with no answer',
                                                         'answer': '',
                                                         'category': 1,
                                                         'difficulty': 1})

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)


    # test bad category returns 400
    def test_incorrect_create_question(self):
        res = self.client().post('/questions/add', json={'question': 'question with no category',
                                                         'answer': 'answer but no category',
                                                         'category': -1,
                                                         'difficulty': 1})

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)

    # test bad difficulty rating returns 400
    def test_incorrect_create_question2(self):
        res = self.client().post('/questions/add', json={'question': 'question with bad difficulty rating',
                                                         'answer': 'answer bad difficulty rating',
                                                         'category': 1,
                                                         'difficulty': -1})

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)



    # def test_delete_question(self):
    #     res = self.client().delete('/questions/<int> id')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()