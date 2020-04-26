import React, { Component } from "react";
import Card from "@material-ui/core/Card";
import CardContent from "@material-ui/core/CardContent";
import Divider from "@material-ui/core/Divider";

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
            toggleButton
        </CardContent>
      </Card>
      
    );
  }
}

export default DashletCard;