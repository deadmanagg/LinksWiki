import React, { Component } from "react";
import { render } from "react-dom";
import RefreshIcon from '@material-ui/icons/Refresh';
import Card from "@material-ui/core/Card";
import CardContent from "@material-ui/core/CardContent";

class Analytics extends Component {

  constructor(props) {
    super(props);
    this.state = {
      data: {
          last_execution_time: "Checking..."
      },
      loaded: false,
      placeholder: "Loading"
    };
    this.onRefresh = this.onRefresh.bind(this);
  }

  componentDidMount() {
      this.checkStatus();
  }

  onRefresh(event) {
      this.checkStatus();      
  }
  
  checkStatus(){
      clearInterval(this.timer);
      fetch("lastexecutiongus")
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
  
  copyCodeToClipboard(){
      var textField = document.createElement('textarea')
      textField.innerText = 'python /Users/deepansh.aggarwal/Study/Projects/LinksWiki/code/GUS/GusHistoryUpdate.py'
      document.body.appendChild(textField)
      textField.select()
      document.execCommand('copy')
      textField.remove()
  }
  
  render() {
    
    return (
    <Card className="card">
        <CardContent className="content">
            <ul>
                GUS Updated on <b> {this.state.data['last_execution_time']} </b>
                
                <button onClick={() => this.copyCodeToClipboard()}>Copy Command</button>
            </ul>             
            <RefreshIcon onClick={this.onRefresh} /> 
        </CardContent>
      </Card>
      );
  }
}

export default Analytics;