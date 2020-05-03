import React, { Component } from "react";
import { render } from "react-dom";
import DashletCard from "./DashletCard.js";

class Listener extends Component {

  constructor(props) {
    super(props);
    this.state = {
      data: {
          status: "Checking..."
      },
      loaded: false,
      placeholder: "Loading"
    };
    this.onChange = this.onChange.bind(this);
    this.checkStatus = this.checkStatus.bind(this);
  }

  componentDidMount() {
      this.checkStatus();
  }

  onChange(event) {
      if(event.currentTarget.checked){
          this.startListener();
      }else{
          this.stopListener();
      }
      
  }
  
  checkStatus(){
      clearInterval(this.timer);
      fetch("listenerstatus")
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
  
  changeStatusToChecking(){
      this.setState(() => {
              return {  data: {
                  status: "Checking..."
              }}
            });
  }
  
  startListener() {
      fetch("startlistener")
          .then(response => {
            if (response.status > 400) {
              return this.setState(() => {
                return { placeholder: "Something went wrong!" };
              });
            }
            this.changeStatusToChecking();
            this.timer = setTimeout(() => this.checkStatus(), 3000);
          });
          
  }
  
  stopListener(){
      fetch("stoplistener")
          .then(response => {
            if (response.status > 400) {
              return this.setState(() => {
                return { placeholder: "Something went wrong!" };
              });
            }
            this.changeStatusToChecking();
            this.timer = setTimeout(() => this.checkStatus());
          });
  }
  
  render() {
    
    return (
      <DashletCard content={"Listener " + this.state.data['status']} checked={this.state.data['status'] === "Running" ? true : false} onChange={this.onChange}/>
      
    );
  }
}

export default Listener;