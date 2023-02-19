from loguru import logger
from flask import Flask, request
from flask_cors import CORS
from utils import search_title

app = Flask(__name__)
CORS(app)


@app.route('/')
def hello_world():
    searchterm = request.args.get('searchterm', None)
    logger.debug(f'searchterm: {searchterm}')
    if not searchterm:
        return []
    try:
        return search_title(searchterm)
    except Exception as _e:
        logger.critical(str(_e))
        return []
