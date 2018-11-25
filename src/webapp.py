from flask import Flask
from flask import request
from searcher import Search
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)
search = Search()
app.config['CORS_HEADERS'] = 'Content-Type'
@app.route("/search")
@cross_origin()
def getSearchResults():
    return (search.searchdblp(request.args.get('query')))


@app.route("/file/<filename>")
@cross_origin()
def getFile(filename):
    return (search.getFileFromDir(filename))


@app.route("/autocomplete")
@cross_origin()
def autocomplete():
    print(request.args.get('query'))
    return (search.autocomplete(request.args.get('query')))

@app.route("/similar/<fileid>")
@cross_origin()
def similar(fileid):
    print(request.args.get('query'))
    return (search.getSimilarDocuments(fileid))


if __name__ == "__main__":
    app.run(debug=True)
    
