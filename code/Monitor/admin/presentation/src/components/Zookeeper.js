import React, { Component } from "react";
import { render } from "react-dom";
import DashletCard from "./DashletCard.js";

class Zookeeper extends Component {

  constructor(props) {
    super(props);
    this.state = {
      data: {},
      loaded: false,
      placeholder: "Loading"
    };
  }

  componentDidMount() {
    fetch("zookeeperstatus")
      .then(response => {
        if (response.status > 400) {
          return this.setState(() => {
            return { placeholder: "Something went wrong!" };
          });
        }
        return response.json()
      })
      .then(data => {
        this.setState(() => {
          console.log(data);
          return {
            data,
            loaded: true
          };
        });
      });
  }

  render() {
    
    return (
      
      <DashletCard content={this.state.data['status']} />
      
    );
  }
}

export default Zookeeper;