import sys
sys.path.insert(0, r'C:\Users\wesle\OneDrive\Documentos\UFPI\ESII\WiseBuilder\src')

from flask import Flask
from endpoints.api import blueprint

app = Flask(__name__)
app.register_blueprint(blueprint)

if __name__ == "__main__":
    app.run(debug=True)
