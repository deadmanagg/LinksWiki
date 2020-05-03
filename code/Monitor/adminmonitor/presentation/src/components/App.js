import React, { Component } from "react";
import { render } from "react-dom";
import ElasticSearch from "./ElasticSearch.js";
import Kafka from "./Kafka.js";
import Zookeeper from "./Zookeeper.js";
import Listener from "./Listener.js";
import PushToES from "./PushToES.js";
import GusHistory from "./GusHistory.js";
import Analytics from "./Analytics.js";
import MainAppServer from "./MainAppServer.js";


class App extends Component {

  render() {
    return (
        <React.Fragment>
            <Zookeeper />
            <Kafka />
            <ElasticSearch />
            <MainAppServer />
            <Listener />
            <PushToES />
            <Analytics />
            <GusHistory />
        </React.Fragment>
    );
  }
}

export default App;

const container = document.getElementById("app");
render(<App />, container);