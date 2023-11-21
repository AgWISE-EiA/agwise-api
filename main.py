from flask import Flask, render_template, jsonify

from app.core import limiter
from app.routes import api_v1

app = Flask(__name__)

app.register_blueprint(api_v1, url_prefix='/api/v1')

app.config['RATELIMIT_HEADERS_ENABLED'] = True
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
    response = jsonify({
        "error": str(error),
        "status": 429
    })
    response.status_code = 429  # Set the status code for error responses
    return response


@app.errorhandler(Exception)
def handle_error(error):
    response = jsonify({
        "error": str(error),
        "status": 500
    })
    response.status_code = 500  # Set the status code for error responses
    return response


if __name__ == '__main__':
    app.debug = True
    app.run(debug=True)
