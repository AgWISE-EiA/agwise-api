from flask import Flask, render_template

from api_v1.routes import api_v1

app = Flask(__name__)

app.register_blueprint(api_v1, url_prefix='/api/v1')


@app.route('/', methods=['GET'])
def index():  # put application's code here
    return render_template("index.html")


if __name__ == '__main__':
    app.debug = True
    app.run(debug=True)
