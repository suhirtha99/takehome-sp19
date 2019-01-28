import React, { Component } from 'react'
import Counter from './Counter'

class App extends Component {
  constructor(props) {
    super(props);
    this.id = props["id"];
    this.name = props["name"];
    this.episodes_seen = props["episodes_seen"];
  }
  
  render() {
    return (
      <div>
        <p>{this.name}</p>
        <Counter initial_count={this.episodes_seen}/> 

      </div>
    )
  }
}

export default App
