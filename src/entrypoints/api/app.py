import sys, os

sys.path.insert(0, os.getcwd())

from flask import Flask
from endpoints.api import blueprint

app = Flask(__name__)
app.register_blueprint(blueprint)

if __name__ == "__main__":
    app.run(debug=True)
