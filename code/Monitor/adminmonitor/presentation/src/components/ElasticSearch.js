import React, { Component } from "react";
import { render } from "react-dom";
import DashletCard from "./DashletCard.js";

class ElasticSearch extends Component {

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
          this.startElasticSearch();
      }else{
          this.stopElasticSearch();
      }
      
  }
  
  checkStatus(){
      clearInterval(this.timer);
      fetch("esstatus")
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
  
  startElasticSearch() {
      fetch("startes")
          .then(response => {
            if (response.status > 400) {
              return this.setState(() => {
                return { placeholder: "Something went wrong!" };
              });
            }
            
            this.changeStatusToChecking();
            this.timer = setTimeout(() => this.checkStatus(), 10000);
          });
          
  }
  
  stopElasticSearch(){
      fetch("stopes")
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
      <DashletCard content={"ElasticSearch " + this.state.data['status']} checked={this.state.data['status'] === "Running" ? true : false} onChange={this.onChange}/>
      
    );
  }
}

export default ElasticSearch;