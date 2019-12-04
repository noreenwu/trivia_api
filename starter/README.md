# Project: Trivia API
# Noreen Wu
# December 2019



##Introduction

The Trivia API is a RESTful API that supports queries and updates to trivia questions.
A client application can retrieve existing questions and answers in the form of quizzes,
and can also add to and delete from the pool of questions. In addition to being viewable by
category, questions are each marked with a difficulty level. Questions can be searched for 
by keyword or by word fragment.


##Getting Started

Base URL: The backend server may be run on the localhost on port 5000, which is set
as a proxy in the frontend configuration.

Authentication: This version of the application does not require authentication or
API keys.

Error Handling: Errors are returned as JSON objects in this format:

{
    "success": False, 
    "error": 400,
    "message": "Bad request"
}

The API may return 3 error types when requests fail:
   400: Bad request
   404: Resource not found
   422: Not processable


##Resource endpoint library

GET /categories

    Returns a categories object containing category id as key and category name as value, 
    plus a success value.

    Sample: curl http://localhost:5000/categories

    {
        "categories": {
        "1": "Science", 
        "2": "Art", 
        "3": "Geography", 
        "4": "History", 
        "5": "Entertainment", 
        "6": "Sports"
        }, 
        "success": true
    }

GET /questions 
GET /questions?page=<int:id>

    Note that all endpoints that return questions 
    (/questions, /categories/<id>/questions, and questions/search)
    return the same information. 
    
    Returns the categories object, a currentCategory field (may be null), a questions object with
    question number as key and a question object as the value, a total_questions value and a success value.

    currentCategory will be null if the questions returned are not from a particular category.
    The total_questions value reflects the total number of questions that could be returned
    without pagination.

    Not specifying a page number will result in page 1 being returned, with QUESTIONS_PER_PAGE
    (set to 10) questions being shown on each full page. 

    Sample:

    $ curl http://localhost:5000/questions?page=2
    {
    "categories": {
        "1": "Science", 
        "2": "Art", 
        "3": "Geography", å
        "4": "History", 
        "5": "Entertainment", 
        "6": "Sports"
    }, 
    "currentCategory": null, 
    "questions": {
        "1": {
        "answer": "Agra", 
        "category": 3, 
        "difficulty": 2, 
        "id": 15, 
        "question": "The Taj Mahal is located in which Indian city?"
        }, 
        "2": {
        "answer": "Escher", 
        "category": 2, 
        "difficulty": 1, 
        "id": 16, 
        "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
        }, 
        "3": {
        "answer": "Mona Lisa", 
        "category": 2, 
        "difficulty": 3, 
        "id": 17, 
        "question": "La Giaconda is better known as what?"
        }, 
        "4": {
        "answer": "One", 
        "category": 2, 
        "difficulty": 4, 
        "id": 18, 
        "question": "How many paintings did Van Gogh sell in his lifetime?"
        }, 
        "5": {
        "answer": "Jackson Pollock", 
        "category": 2, 
        "difficulty": 2, 
        "id": 19, 
        "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
        }, 
        "6": {
        "answer": "The Liver", 
        "category": 1, 
        "difficulty": 4, 
        "id": 20, 
        "question": "What is the heaviest organ in the human body?"
        }, 
        "7": {
        "answer": "Alexander Fleming", 
        "category": 1, 
        "difficulty": 3, 
        "id": 21, 
        "question": "Who discovered penicillin?"
        }, 
        "8": {
        "answer": "Blood", 
        "category": 1, 
        "difficulty": 4, 
        "id": 22, 
        "question": "Hematology is a branch of medicine involving the study of what?"
        }, 
        "9": {
        "answer": "Scarab", 
        "category": 4, 
        "difficulty": 4, 
        "id": 23, 
        "question": "Which dung beetle was worshipped by the ancient Egyptians?"
        }, 
        "10": {
        "answer": "Ozymandias", 
        "category": 4, 
        "difficulty": 3, 
        "id": 34, 
        "question": "What is the Greek name for Rameses II?"
        }
    }, 
    "success": true, 
    "total_questions": 24
}

GET /categories/<int:id>/questions
GET /categories<int:id>/questions?page=<int:id>

    This endpoint is similar to the /questions endpoint, except that only questions of
    the specified category are returned. The category is specified as an integer
    in the endpoint url. Similar to the /questions endpoint, if the page attribute is omitted
    from the url, then page 1 results are returned.

    Sample:

    $ curl http://localhost:5000/categories/1/questions
    {
    "categories": {
        "1": "Science", 
        "2": "Art", 
        "3": "Geography", 
        "4": "History", 
        "5": "Entertainment", 
        "6": "Sports"
    }, 
    "currentCategory": 1, 
    "questions": {
        "1": {
        "answer": "The Liver", 
        "category": 1, 
        "difficulty": 4, 
        "id": 20, 
        "question": "What is the heaviest organ in the human body?"
        }, 
        "2": {
        "answer": "Alexander Fleming", 
        "category": 1, 
        "difficulty": 3, 
        "id": 21, 
        "question": "Who discovered penicillin?"
        }, 
        "3": {
        "answer": "Blood", 
        "category": 1, 
        "difficulty": 4, 
        "id": 22, 
        "question": "Hematology is a branch of medicine involving the study of what?"
        }
    }, 
    "success": true, 
    "total_questions": 3
    }

POST /questions/search

    Returns a list of questions that match the end user's search term or fragment, in
    the same format as the /questions and /categories/<id>/questions endpoints described above.
    That is, included are the categories object, the currentCategory (null since no category
    can be specified for search), the questions object of objects, a success value, and
    the total questions matching the search term.

    The search term or pattern and the page number must be passed in as a json
    object. 

    The maximum number of returned questions is the number of questions per page, (set to 10).

    Sample:

    $ curl http://localhost:5000/questions/search -H "Content-Type: application/json" -d '{ "searchTerm": "title", "page": 1 }' -X POST
    {
    "categories": {
        "1": "Science", 
        "2": "Art", 
        "3": "Geography", 
        "4": "History", 
        "5": "Entertainment", 
        "6": "Sports"
    }, 
    "currentCategory": null, 
    "questions": {
        "1": {
        "answer": "Maya Angelou", 
        "category": 4, 
        "difficulty": 2, 
        "id": 5, 
        "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
        }, 
        "2": {
        "answer": "Edward Scissorhands", 
        "category": 5, 
        "difficulty": 3, 
        "id": 6, 
        "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
        }
    }, 
    "success": true, 
    "total_questions": 2
    }


DELETE /questions/<int:id>

    Deletes the question of the specified ID, if it exists. On successful deletion, a success value is returned.

    If the specified question does not exist, error code 400 is returned.

    Sample:
    $ curl -X DELETE http://localhost:5000/questions/131
    {
    "deleted": 131, 
    "success": true
    }


POST /questions/add

    Creates a new question in the database. Required data includes the question text, the answer text,
    a difficulty rating and a category. A success value is returned on successful creation of the new question.

    Sample:
    $ curl -X POST http://localhost:5000/questions/add -H "Content-Type: application/json" -d '{"question": "What is a baby goat called?", "answer": "kid", "difficulty": 1, "category": 1}'
    {
    "success": true
    }


POST /quizzes


     Takes as input an array of previous questions that the user has already seen and a quiz category.
     Returns a question object, success value, and the total number of questions in the specified category.
     Does not return questions that are in the previous_questions array.

     Example input:

       { 'previous_questions': [], 
         'quiz_category': { 'type': 'Science', 'id': 1} }


    Sample: 

    $ curl -X POST http://localhost:5000/quizzes -H "Content-Type: application/json" -d '{ "previous_questions": [], "quiz_category": {"type": "Science", "id": 1 }}'
    {
    "question": {
        "answer": "The Liver", 
        "category": 1, 
        "difficulty": 4, 
        "id": 20, 
        "question": "What is the heaviest organ in the human body?"
    }, 
    "success": true, 
    "total_questions": 4
    }

    Sample with previous questions:

    $ curl -X POST http://localhost:5000/quizzes -H "Content-Type: application/json" -d '{ "previous_questions": [10], "quiz_category": {"type": "Sports", "id": 6 }}'
    {
    "question": {
        "answer": "Uruguay", 
        "category": 6, 
        "difficulty": 4, 
        "id": 11, 
        "question": "Which country won the first ever soccer World Cup in 1930?"
    }, 
    "success": true, 
    "total_questions": 2
    }


