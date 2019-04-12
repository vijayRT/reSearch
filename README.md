# re-Search

Project for MSc CS course 538: Information Retrieval

Search engine for indexing, searching, and retrieval of ~1 million academic research papers. (thus the name)

Dataset used: [AMiner DBLP Citation Network](https://aminer.org/citation)

## Libraries used and concepts implemented:
* Used [Whoosh](https://whoosh.readthedocs.io/en/latest/intro.html) for indexing and searching
* Implemented PageRank using [graph-tool](https://graph-tool.skewed.de/)
* Performed Word embedding using [FastText](https://fasttext.cc/) 
* Used scikit-learn to cluster similar research papers
* Flask to use the search engine as an API, served through a [frontend](https://github.com/vijayRT/re-SearchVue) written using Vue.js

![](https://i.imgur.com/124oLuZ.png)
