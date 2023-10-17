from flask import Flask, render_template
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from app.routes.routes import api_v1

app = Flask(__name__)

app.register_blueprint(api_v1, url_prefix='/api/v1')

app.config['RATELIMIT_HEADERS_ENABLED'] = True

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://",
)


@app.route('/', methods=['GET'])
@limiter.exempt
def index():  # put application's code here
    return render_template("index.html")


if __name__ == '__main__':
    app.debug = True
    app.run(debug=True)
