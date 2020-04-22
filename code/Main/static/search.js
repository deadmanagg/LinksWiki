const API_URL = 'http://localhost:8000/search/?q='
const ANALYTICS_API_URL = 'http://localhost:8000/analytics/'


class SearchBox extends React.Component {
  
  state = {
      data: [],
      loading: 'DD'
  };
  componentDidMount() {
    
  }
  
  searchAndUpdateResult(event) {
    if (event.keyCode == 13){
        var test = document.getElementById('searchTerm').value;
        const url = API_URL+test
        axios.get(url).then(response => response.data)
        .then((data) => {
          this.setState({data, loading: 'EE'});
          
         })
       }
  
  }
  
  sendForAnalytics = (event) => {
  
      var term = document.getElementById('searchTerm').value;
      var result = this.state.data
      var selectedLink = event.target.href
      
      var data = {
          "searchTerm": term,
          "result" : result,
          "selectedLink" :selectedLink
      }
      
      axios.post(ANALYTICS_API_URL, { data })
      .then(res => {
        console.log(res);
        console.log(res.data);
      })
  }
  formHref (d){
      return <a href={d.url} target="_blank" onClick={this.sendForAnalytics}>{d.url}   ===> {d.title}</a>
  
  }
  render() {
    
    const { data, loading } = this.state;
    
    return (
    <>
        <div className="heading">
            <input name='searchTerm' id='searchTerm' type='text' onKeyUp={this.searchAndUpdateResult.bind(this)}></input>
        </div>
        <div>            
                    {data.map(d => <div className="resultLinks"> {this.formHref(d)}</div>)}
        </div>
    </>
    );
  }
}

ReactDOM.render(
  <SearchBox />,
  document.getElementById('like_button_container'));