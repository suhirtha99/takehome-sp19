import React, { Component } from 'react'

class Counter extends Component {
  constructor(props) {
    super(props);
    this.count = props["initial_count"];
  }

  state = {count: this.count};
  handleIncrement = () => {
    this.setState({count: this.count + 1});
    this.count += 1;
  }

  handleDecrement = () => {
    this.setState({count: this.count - 1});

    this.count -= 1;
  }
  render() {
    return (
      <div>
        <p>
        {this.count}
        </p>
        <button onClick={this.handleIncrement}>Increment</button>
        <button onClick={this.handleDecrement}>Decrement</button>
      </div>
    )
  }
}

export default Counter
