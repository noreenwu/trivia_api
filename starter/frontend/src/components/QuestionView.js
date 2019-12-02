import React, { Component } from 'react';

import '../stylesheets/App.css';
import Question from './Question';
import Search from './Search';
import $ from 'jquery';

const QUESTIONS_PER_PAGE = 6
const API_SERVER = 'http://localhost:5000'

class QuestionView extends Component {
  constructor(){
    super();
    this.state = {
      questions: [],
      page: 1,
      totalQuestions: 0,
      categories: {},
      currentCategory: null,
    
    }
  }

  componentDidMount() {
    this.getQuestions();
  }

  getQuestions = () => {

    $.ajax({
      // url: `http://localhost:5000/questions?page=${this.state.page}`, 
      url: `${API_SERVER}/questions?page=${this.state.page}`, 

      type: "GET",
      datatType: "jsonp",
      success: (result) => {
        this.setState({
          questions: Object.values(result.questions),
          totalQuestions: result.total_questions,
          // totalQuestions: 9,
          categories: result.categories,
          currentCategory: result.currentCategory
        })
        return;
      },
      error: (error) => {
        alert('Questions Unable to load questions. Please try your request again')
        return;
      }
    })
  }

  selectPage(num) {
    console.log("selectPage current category is ", this.state.currentCategory)
    if (this.state.currentCategory === null) {
      this.setState({page: num}, () => this.getQuestions());
    }
    else {
      this.setState({page: num}, () => this.getByCategory(this.state.currentCategory, this.state.page));
    }
  }

  createPagination(){
    let pageNumbers = [];
    let maxPage = Math.ceil(this.state.totalQuestions / QUESTIONS_PER_PAGE)
    for (let i = 1; i <= maxPage; i++) {
      pageNumbers.push(
        <span
          key={i}
          className={`page-num ${i === this.state.page ? 'active' : ''}`}
          onClick={() => {this.selectPage(i)}}>{i}
        </span>)
    }
    return pageNumbers;
  }

  getByCategory= (id, pg) => {
    console.log("getByCategory")
    $.ajax({
      url: `http://localhost:5000/categories/${id}/questions?page=${pg}`, 
      // url: `http://localhost:5000/categories/${id}/questions`, 

      type: "GET",
      success: (result) => {
         this.setState({
           questions: Object.values(result.questions),
           totalQuestions: result.total_questions,
           currentCategory: result.currentCategory })
         return;
      },
      error: (error) => {
        alert('QuestionsUnable to load questions. Please try your request again', error)
        return;
      }
    })
  }

  submitSearch = (searchTerm) => {
    $.ajax({
      url: `http://localhost:5000/questions/search`, 
      type: "POST",
      dataType: 'json',
      contentType: 'application/json',
      data: JSON.stringify({searchTerm: searchTerm}),
      // xhrFields: {
      //   withCredentials: true
      // },
      crossDomain: true,
      success: (result) => {
        this.setState({
          questions: Object.values(result.questions),
          totalQuestions: result.total_questions,
          currentCategory: result.currentCategory })
        return;
      },
      error: (error) => {
        alert('SEARCH Unable to load questions. Please try your request again')
        return;
      }
    })
  }

  questionAction = (id) => (action) => {
    if(action === 'DELETE') {
      if(window.confirm('are you sure you want to delete the question?')) {
        $.ajax({
          url: `http://localhost:5000/questions/${id}`, 
          type: "DELETE",
          success: (result) => {
            this.getQuestions();
          },
          error: (error) => {
            alert('Unable to load questions. Please try your request again')
            return;
          }
        })
      }
    }
  }

  render() {
    return (
      <div className="question-view">
        <div className="categories-list">
          <h2 className="title" onClick={() => {this.getQuestions()}}>Categories</h2>
          <ul>
            {Object.keys(this.state.categories).map((id, ) => (
              <li className="category-container" key={id} onClick={() => {this.getByCategory(id, 1)}}>
                <div className="category-name">{this.state.categories[id]}</div>
                <img className="category" alt={``} src={`${this.state.categories[id]}.svg`}/>

              </li>
            ))}
          </ul>
          <Search submitSearch={this.submitSearch}/>
        </div>
        <div className="questions-list">
          <h2 className="title">Questions</h2>
          {this.state.questions.map((q, ind) => (
            <Question
              key={q.id}
              question={q.question}
              answer={q.answer}
              category={this.state.categories[q.category]} 
              difficulty={q.difficulty}
              questionAction={this.questionAction(q.id)}
            />
          ))}
          <div className="pagination-menu">
            {this.createPagination()}
          </div>
        </div>

      </div>
    );
  }
}

export default QuestionView;
