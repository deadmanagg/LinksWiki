import React, { Component } from "react";
import { render } from "react-dom";
import DashletCard from "./DashletCard.js";

class MainAppServer extends Component {

  constructor(props) {
    super(props);
    this.state = {
      data: {
          status: 'Checking...'
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
          this.startMainAppServer();
      }else{
          this.stopMainAppServer();
      }
      
  }
  
  checkStatus(){
      clearInterval(this.timer);
      fetch("wsstatus")
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
  
  startMainAppServer() {
      fetch("startws")
          .then(response => {
            if (response.status > 400) {
              return this.setState(() => {
                return { placeholder: "Something went wrong!" };
              });
            }
            this.changeStatusToChecking();
            this.timer = setTimeout(() => this.checkStatus(), 5000);
          });
          
  }
  
  stopMainAppServer(){
      fetch("stopws")
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
  
  render() {
    
    return (
      <DashletCard content={"Main App Server " + this.state.data['status']} checked={this.state.data['status'] === "Running" ? true : false} onChange={this.onChange}/>
      
    );
  }
}

export default MainAppServer;