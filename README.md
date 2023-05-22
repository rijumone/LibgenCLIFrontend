# LibgenCLIFrontend

React frontend wrapper over [Libgen](http://libgen.lc/).

Borrowed some code from [Libgen-CLI](https://github.com:kriticalflare/Libgen-CLI.git). Thanks!

## Demo
[Here](http://get-books.zapto.org:5006/)

## Screenshot
<img src="https://i.postimg.cc/FRHmyXZH/Screenshot-2023-02-19-at-23-46-45.png" />

## Structure
Project consists of a Flask backend and a React frontend.

## What's working
Barebones UI which will submit a form with a search term and render a table with book titles and direct download links.

## TODO:
### Frontend
- [x] Import a modern UI library. e.g. [MUI](https://mui.com/).

- [x] Show a loader when the form is submitted, hide it when the call completes, both success and failure.

- [ ] Improve the UI of the above loader.

- [ ] Disable form when one request is ongoing.

- [ ] Show an error message for failure.

- [ ] Add support for filters and parameters

### Backend
- [x] Additional DEBUG logs.

- [x] Return partial data where possible.

- [x] Improve performance to reduce time taken per request.

- [ ] Add support for filters and parameters

## General
- [ ] Add production deployment implementation