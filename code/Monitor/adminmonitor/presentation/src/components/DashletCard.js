import React, { Component } from "react";
import Card from "@material-ui/core/Card";
import CardContent from "@material-ui/core/CardContent";
import Divider from "@material-ui/core/Divider";
import Switch from "@material-ui/core/Switch";

class DashletCard extends Component {
  
  componentDidMount() {
  }

  render() {
    
    return (
      
      <Card className="card">
        <CardContent className="content">
            <ul>
                {this.props.content}
            </ul>
          <Divider className="divider" light />
            <Switch onChange={this.props.onChange} checked={this.props.checked}/>
        </CardContent>
      </Card>
      
    );
  }
}

export default DashletCard;