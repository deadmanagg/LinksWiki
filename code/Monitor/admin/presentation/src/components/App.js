import React, { Component } from "react";
import { render } from "react-dom";
import Zookeeper from "./Zookeeper.js";

class App extends Component {

  render() {
    return (

        <Zookeeper />
    );
  }
}

export default App;

const container = document.getElementById("app");
render(<App />, container);