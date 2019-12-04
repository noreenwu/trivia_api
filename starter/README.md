# Project: Trivia API
# Noreen Wu
# November 2019



##Introduction

The Trivia API is a RESTful API that supports queries and updates to questions and their categories.
A client application can retrieve existing questions and answers in the form of quizzes,
and can also add to and delete from the pool of questions. In addition to being viewable by
category, questions are marked with a difficulty level. Questions can be searched by keyword or
word fragment.


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

The API will return 3 error types when requests fail:
   400: Bad request
   404: Resource not found
   422: Not processable


Resource endpoint library

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

    All endpoints that return questions (/questions, /categories/<id>/questions, and questions/search)
    return the same information. 
    
    Returns the categories object, a currentCategory field (may be null), a questions object with
    question number as key and a question object as the value, a total_questions value and a success value.

    currentCategory will be null if the questions returned are not from a particular category.
    The total_questions value reflects the total number of questions that could be returned
    without pagination.

    Not specifying a page number will result in page 1 being returned, with QUESTIONS_PER_PAGE
    questions being shown on each full page. 

    Sample:
    

GET /categories/<int:id>/questions

POST /questions/search

DELETE /questions/<int:id>

POST /questions/add

POST /quizzes



Sample request
Arguments including data types
Response object including status codes and data types