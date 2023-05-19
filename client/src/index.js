import React from "react";

import Button from '@mui/material/Button'
import TextField from '@mui/material/TextField'
import Tooltip from '@mui/material/Tooltip'
import TableContainer from '@mui/material/TableContainer'
import Table from '@mui/material/Table'
import TableHead from '@mui/material/TableHead'
import TableCell from '@mui/material/TableCell'
import TableRow from '@mui/material/TableRow'
import TableBody from '@mui/material/TableBody'

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
      loading: false,
    };
  }
  handleSubmit = (event) => {
    event.preventDefault();
    this.setState({ ...this.state.data, loading: true }) // spread? Like python **args
    console.log(this.input.value);
    fetch("http://albumart-gen.hopto.org:5005?searchterm=" + this.input.value, {
    // fetch("http://localhost:5000?searchterm=" + this.input.value, {
      method: "GET",
      // body: formData
    })
      .then((response) => response.json()) // (response) => response.json() this is a function, will pass the value to the next then()
      .then((data) => this.setState({ data, loading: false }));
  };
  render() {
    return (
      <center>
        <form onSubmit={this.handleSubmit}>
          <Tooltip title="Enter fully or in part" arrow placement="left">
            {/* <TextField variant="standard" label="Title or author" ref={(input) => (this.input = input)} /> */}
            <input type="text" ref={(input) => (this.input = input)} />
          </Tooltip>
          <Button variant="contained" type="submit">Search</Button>
          <span>{ this.state.loading ? 'loading...' : ''}</span>
        </form>
        {this.state.data && (
          <TableContainer
          // component={Paper} 
          variant="outlined"
          >
              <Table aria-label="demo table">
              <TableHead><TableRow>
              <TableCell>Title</TableCell><TableCell>Download link</TableCell>
              </TableRow></TableHead>
              <TableBody>
                {this.state.data.map((book) => (
                  <TableRow key={book.title}>
                    <TableCell>{book.title}</TableCell>
                    <TableCell>
                      <a href={book.mirror_list} rel="noreferrer" target="_blank">
                        {book.mirror_list}
                      </a>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        )}
      </center>
    );
  }
}
// ========================================

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(<LibgenApp />);
