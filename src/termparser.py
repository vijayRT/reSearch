from requests_html import HTMLSession
from matplotlib import pyplot as plt
import operator
class TermParser:

    def __init__(self):
        self.allterms = []
        self.termdict = {}
    def labautopedia(self):
        session = HTMLSession()
        r = session.get('http://www.labautopedia.org/mw/List_of_programming_and_computer_science_terms')
        termlist = [x.text.split(" -")[0] for x in r.html.find('#mw-content-text > ul > li > b')]
        noabbrtermlist = []
        for term in termlist:
            if ":" in term and u"\xa0" not in term:
                term = term.split(": ")[1]
            if len(term.split(" ")) < 3:
                noabbrtermlist.append(term)
        self.allterms += [x for x in noabbrtermlist if len(x.split(" ")) > 1]

    def webopedia(self):
        session = HTMLSession()
        webopediasession = session.get("https://www.webopedia.com/Computer_Science/2")
        column1links = [x.absolute_links for x in webopediasession.html.find('#category_index_listing', first=True).find('#listing-column_1 > li > a')]
        column2links = [x.absolute_links for x in webopediasession.html.find('#category_index_listing', first=True).find('#listing-column_2 > li > a')]
        alllinks = column1links + column2links
        webopediatermlist = []
        for linkset in alllinks:
            link = list(linkset)[0]
            linksession = session.get(link)
            categoryterms = [x.text for x in linksession.html.find('#category_index_listing > #listing-column_1 > li > a') if len(x.text.split(" ")) > 1]
            webopediatermlist += categoryterms  
        self.allterms += webopediatermlist

    def constructTermCountDict(self):
        for term in self.allterms:
            self.termdict[term] = 0
    
    def wordOccurenceGraph(self):
        wordlist = []
        countlist = []
        for key, value in sorted(self.termdict.items() ,  key=lambda x: x[1], reverse=True):
            wordlist.append(key)
            countlist.append(value)
            print(key, value)
        plt.barh(wordlist[10:0:-1], countlist[10:0:-1])
        plt.xlabel("Word Count")
        plt.ylabel("Words")
        plt.show()