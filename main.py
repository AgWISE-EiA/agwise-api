from flask import Flask, render_template, jsonify
from flask_openapi3 import Info, Tag, OpenAPI, Server
from pydantic import BaseModel

from app.core import limiter
from app.routes import api_v1

info = Info(title="AgWise API", version="1.0.0")

servers = [
    Server(url="http://127.0.0.1:5000"),
    Server(url="https://akilimo.org:5000"),
]

# app = Flask(__name__)
app = OpenAPI(__name__,
              info=info,
              servers=servers)

# app.register_blueprint(api_v1, url_prefix='/api/v1')
app.register_api(api_v1)

app.config['RATELIMIT_HEADERS_ENABLED'] = True
app.json.sort_keys = False

limiter.init_app(app)


@app.route('/', methods=['GET'])
@limiter.exempt
def index():  # put application's code here
    return render_template("index.html")


@app.route('/search', methods=['GET'])
@limiter.exempt
def form():  # put application's code here
    return render_template("form-filter.html")


@app.errorhandler(429)
def rate_limit_error(error):
    status_code = 429
    response = jsonify({
        "error": str(error),
        "status": status_code
    })
    response.status_code = status_code  # Set the status code for error responses
    return response


@app.errorhandler(Exception)
def handle_error(error):
    status_code = 500
    response = jsonify({
        "error": str(error),
        "status": status_code
    })
    response.status_code = status_code  # Set the status code for error responses
    return response


if __name__ == '__main__':
    app.debug = True
    app.run(debug=True)
