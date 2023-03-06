import React from "react";
import ReactDOM from "react-dom/client";
import "./index.css";

class LibgenApp extends React.Component {
  render() {
    // const bar = "qux"
    return (
      <>
        <SearchBox />
        {/* <Table foo={bar}/> */}
      </>
    );
  }
}

class SearchBox extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      data: null,
    };
  }
  handleSubmit = (event) => {
    event.preventDefault();
    console.log(this.input.value);
    fetch("http://albumart-gen.hopto.org:5005?searchterm=" + this.input.value, {
    // fetch("http://localhost:5000?searchterm=" + this.input.value, {
      method: "GET",
      // body: formData
    })
      .then((response) => response.json())
      .then((data) => this.setState({ data }));
  };
  render() {
    return (
      <>
        <form onSubmit={this.handleSubmit}>
          <label>
            Search:
            <input type="text" ref={(input) => (this.input = input)} />
          </label>
          <button type="submit">Submit</button>
        </form>
        {this.state.data && (
          <table>
            <tbody>
              {this.state.data.map((book) => (
                <tr key={book.title}>
                  <td>{book.title}</td>
                  <td>
                    <a href={book.mirror_list} rel="noreferrer" target="_blank">
                      {book.mirror_list}
                    </a>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </>
    );
  }
}
// ========================================

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(<LibgenApp />);
