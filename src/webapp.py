from flask import Flask
from flask import request
from searcher import searchdblp, getFileFromDir
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
@app.route("/search")
@cross_origin()
def getSearchResults():
    return (searchdblp(request.args.get('query')))


@app.route("/file/<filename>")
@cross_origin()
def getFile(filename):
    return (getFileFromDir(filename))

if __name__ == "__main__":
    app.run(debug=True)

