import React, { Component } from 'react';

import '../stylesheets/App.css';
import Question from './Question';
import Search from './Search';
import $ from 'jquery';
import { timingSafeEqual } from 'crypto';

import { QUESTIONS_PER_PAGE, API_SERVER } from '../constants'


class QuestionView extends Component {
  constructor(){
    super();
    this.state = {
      questions: [],
      page: 1,
      totalQuestions: 0,
      categories: {},
      currentCategory: null,
      currentFunction: this.getQuestions,
      searchTerm: ''
    }
  }

  componentDidMount() {
    this.getQuestions();
  }

  saveCurrentFunction = (newFunc) => {
    this.setState({
      currentFunction : newFunc
    })

  }

  saveSearchTerm = (searchTerm) => {
    this.setState({
      searchTerm: searchTerm
    })
  }

  adjustPageNumber() {
    let numQuestionsAfterDeletion = this.state.totalQuestions - 1
    let numPages = Math.ceil((numQuestionsAfterDeletion) / QUESTIONS_PER_PAGE)

    console.log("num pages is now ", numPages)
    // numPages = Math.ceil(numPages, 1)
    if (numPages === 0) {
      numPages = 1
    }

    if (this.state.page > numPages) {
        this.setState({
          page: numPages
        })
    }
  }

  getQuestions = () => {                // category and pg are determined elsewhere
    this.saveCurrentFunction(this.getQuestions)

    $.ajax({
      // url: `http://localhost:5000/questions?page=${this.state.page}`, 
      url: `${API_SERVER}/questions?page=${this.state.page}`, 

      type: "GET",
      datatType: "jsonp",
      success: (result) => {
        this.setState({
          questions: Object.values(result.questions),
          totalQuestions: result.total_questions,
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
    if (this.state.currentFunction === this.submitSearch ) {
      this.setState({ page: num }, 
                      () => this.submitSearch(this.state.searchTerm));
    }
    else {
      if (this.state.currentCategory === null) {
        this.setState({page: num}, () => this.getQuestions());
      }
      else {
        this.setState({page: num}, () => this.getByCategory(this.state.currentCategory, this.state.page));
      }
    }
  }

  createPagination() {
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
    this.saveCurrentFunction(this.getByCategory)    
    console.log("getByCategory")
 
    $.ajax({
      url: `${API_SERVER}/categories/${id}/questions?page=${pg}`, 
      // url: `${API_SERVER}/categories/${id}/questions`, 

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
    this.saveCurrentFunction(this.submitSearch)
    this.saveSearchTerm(searchTerm)    

    $.ajax({
      url: `${API_SERVER}/questions/search`, 
      type: "POST",
      dataType: 'json',
      contentType: 'application/json',
      data: JSON.stringify({searchTerm: searchTerm, page: this.state.page}),
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
      if(window.confirm('Are you sure you want to delete this question?')) {

        $.ajax({
          url: `${API_SERVER}/questions/${id}`, 
          type: "DELETE",
          success: (result) => {
            this.adjustPageNumber() 
            if (this.state.currentFunction === this.submitSearch ) {
              this.state.currentFunction(this.state.searchTerm)
            }
            else {
              this.state.currentFunction(this.state.currentCategory, this.state.page)
            }
            //this.getQuestions();            
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
