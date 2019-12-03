import React, { Component } from 'react';
import $ from 'jquery';

import '../stylesheets/QuizView.css';

import { API_SERVER } from '../constants'

const questionsPerPlay = 5; 

class QuizView extends Component {
  constructor(props){
    super();
    this.state = {
        quizCategory: null,
        previousQuestions: [], 
        numTotalQuestions: 0,
        showAnswer: false,
        categories: {},
        numCorrect: 0,
        currentQuestion: {},
        guess: '',
        forceEnd: false
    }
  }

  componentDidMount(){
    $.ajax({
      url: `${API_SERVER}/categories`, //TODO: update request URL
      type: "GET",
      success: (result) => {
        this.setState({ categories: result.categories })
        return;
      },
      error: (error) => {
        alert('Unable to load categories. Please try your request again')
        return;
      }
    })
  }

  selectCategory = ({type, id=0}) => {
    this.setState({quizCategory: {type, id}}, this.getNextQuestion)
  }

  handleChange = (event) => {
    this.setState({[event.target.name]: event.target.value})
  }

  getNextQuestion = () => {
    const previousQuestions = [...this.state.previousQuestions]
    if(this.state.currentQuestion.id) { previousQuestions.push(this.state.currentQuestion.id) }
    if ((this.state.previousQuestions.length > 0) && (this.state.previousQuestions.length ===  this.state.numTotalQuestions-1)) {
        console.log("no more questions, force end")
        this.setState({
          forceEnd: true
        })
        return
    }

    $.ajax({
      url: `${API_SERVER}/quizzes`, //TODO: update request URL
      type: "POST",
      dataType: 'json',
      contentType: 'application/json; charset=utf-8',
      data: JSON.stringify({
        previous_questions: previousQuestions,
        quiz_category: this.state.quizCategory
      }),
      // xhrFields: {
      //   withCredentials: true
      // },
      crossDomain: true,
      success: (result) => {
        this.setState({
          showAnswer: false,
          previousQuestions: previousQuestions,
          numTotalQuestions: result.total_questions,          
          currentQuestion: result.question,
          guess: '',
          forceEnd: result.question ? false : true
        })
        return;
      },
      error: (error) => {
        alert('Unable to load question. Please try your request again')
        return;
      }
    })
  }

  submitGuess = (event) => {
    event.preventDefault();
    //const formatGuess = this.state.guess.replace(/[.,\/#!$%\^&\*;:{}=\-_`~()]/g,"").toLowerCase()
    let evaluate =  this.evaluateAnswer()
    this.setState({
      numCorrect: !evaluate ? this.state.numCorrect : this.state.numCorrect + 1,
      showAnswer: true,
    })
  }

  restartGame = () => {
    this.setState({
      quizCategory: null,
      previousQuestions: [], 
      showAnswer: false,
      numCorrect: 0,
      currentQuestion: {},
      guess: '',
      forceEnd: false
    })
  }

  renderPrePlay(){
      return (
          <div className="quiz-play-holder">
              <div className="choose-header">Choose Category</div>
              <div className="category-holder">
                  <div className="play-category" onClick={this.selectCategory}>ALL</div>
                  {Object.keys(this.state.categories).map(id => {
                  return (
                    <div
                      key={id}
                      value={id}
                      className="play-category"
                      onClick={() => this.selectCategory({type:this.state.categories[id], id})}>
                      {this.state.categories[id]}
                    </div>
                  )
                })}
              </div>
          </div>
      )
  }

  renderFinalScore(){
    return(
      <div className="quiz-play-holder">
        <div className="final-header"> Your Final Score is {this.state.numCorrect}</div>
        <div className="play-again button" onClick={this.restartGame}> Play Again? </div>
      </div>
    )
  }


  checkMultiWordResponse = (guessArray, answerArray) => {
    console.log("checking multiwordresponse: ", guessArray, answerArray)
    for (let g of guessArray) {
      if (g !== 'the') {
        if (! answerArray.includes(g)) {
          return false
        }
      }
    }

    for (let a of answerArray) {
      if (a !== 'the') {
        if (! guessArray.includes(a)) {
          return false
        }
      }
    }
    return true
  }

  evaluateAnswer = () => {

    const formattedGuess = this.state.guess.replace(/[.,\/#!$%\^&\*;:{}=\-_`~()]/g,"").toLowerCase()
    const formattedAnswer = this.state.currentQuestion.answer.toLowerCase()
    const answerArray = formattedAnswer.split(' ')
    const guessArray = formattedGuess.split(' ')


    return this.checkMultiWordResponse(guessArray, answerArray)

  }

  renderCorrectAnswer(){
    //const formatGuess = this.state.guess.replace(/[.,\/#!$%\^&\*;:{}=\-_`~()]/g,"").toLowerCase()
    let evaluate =  this.evaluateAnswer()
    let displayNext = ''


    if (this.state.previousQuestions.length <  this.state.numTotalQuestions-1) {
      displayNext = 'Next Question'
    }
    else {
      displayNext = "How'd I do?"
    }
                                                        
    return(
      <div className="quiz-play-holder">
        <div className="quiz-question">{this.state.currentQuestion.question}</div>
        <div className={`${evaluate ? 'correct' : 'wrong'}`}>{evaluate ? "You were correct!" : "You were incorrect"}</div>
        <div className="quiz-answer">{this.state.currentQuestion.answer}</div>
        <div className={`next-question button`} onClick={this.getNextQuestion}>{displayNext} </div>
      </div>
    )
  }

  renderPlay(){
    return this.state.previousQuestions.length === questionsPerPlay || this.state.forceEnd
      ? this.renderFinalScore()
      : this.state.showAnswer 
        ? this.renderCorrectAnswer()
        : (
          <div className="quiz-play-holder">
            <div className="quiz-question">{this.state.currentQuestion.question}</div>
            <form onSubmit={this.submitGuess}>
              <input type="text" name="guess" onChange={this.handleChange}/>
              <input className="submit-guess button" type="submit" value="Submit Answer" />
            </form>
          </div>
        )
  }


  render() {
    return this.state.quizCategory
        ? this.renderPlay()
        : this.renderPrePlay()
  }
}

export default QuizView;
