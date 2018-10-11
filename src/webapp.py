from flask import Flask
from flask import request
from searcher import searchdblp, getFileFromDir

app = Flask(__name__)

@app.route("/search")
def getSearchResults():
    return (searchdblp(request.args.get('query')))


@app.route("/file/<filename>")
def getFile(filename):
    return (getFileFromDir(filename))

if __name__ == "__main__":
    app.run(debug=True)

