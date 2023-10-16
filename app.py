import os
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

from sqlalchemy.sql import func

from api_v1.routes import api_v1
from potato.agwise_potato import AgWisePotato

load_dotenv()

app = Flask(__name__)

db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")
db_name = os.getenv("DB_NAME")

# app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}'
# db = SQLAlchemy(app)


app.register_blueprint(api_v1, url_prefix='/api/v1')


@app.route('/', methods=['GET'])
def index():  # put application's code here
    return render_template("index.html")


if __name__ == '__main__':
    app.debug = True
    app.run(debug=True)
