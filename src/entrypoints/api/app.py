import os
import sys

sys.path.insert(0, os.getcwd())
print(os.getcwd())
from flask import Flask
from flask_cors import CORS
from endpoints.api import blueprint

app = Flask(__name__)
app.register_blueprint(blueprint)

CORS(app, resources={r"/*": {"origins": "*"}})
if __name__ == "__main__":
    app.run(debug=True)
