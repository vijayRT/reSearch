from flask import Flask
from flask import request
from src.searcher import search

app = Flask(__name__)

@app.route("/search")
def getSearchResults():
    return (search(request.args.get('query')))

if __name__ == "__main__":
    app.run(debug=True)