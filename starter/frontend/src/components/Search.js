import React, { Component } from 'react'

class Search extends Component {
  state = {
    query: '',
  }

  getInfo = (event) => {
    event.preventDefault();
    this.props.submitSearch(this.state.query)
  }

  handleInputChange = () => {
    this.setState({
      query: this.search.value
    })
  }

  render() {
    return (
      <form onSubmit={this.getInfo}>
        <input
          type="search"
          placeholder="Search questions..."
          ref={input => this.search = input}
          onChange={this.handleInputChange}
        />
        <input disabled={this.state.query === ''} type="submit" value="Submit" className="button"/>
      </form>
    )
  }
}

export default Search
