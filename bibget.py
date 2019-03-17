from urllib.request import Request, urlopen, quote
from bs4 import BeautifulSoup
import re
import sys, getopt

# takes URL, returns beautiful soup
def request_page(url):
    header = {'User-Agent': 'Mozilla/5.0', "Cookie":"GSP=CF=4"}
    request = Request(url, headers=header)
    response = urlopen(request)
    html = response.read()
    htmlsoup = BeautifulSoup(html, features="lxml")
    return htmlsoup

'''
Takes any search string, returns a list of links to google scholar bibTeX citations
Thanks to venthur/gscholar
'''
def google_scholar_query(searchstr):
    searchstr = '/scholar?q=' + quote(searchstr)
    url = "https://scholar.google.com" + searchstr
    htmlsoup = request_page(url)
    with open("test.html", "w+") as f:
        f.write(str(htmlsoup))

    refs_list = []
    refre = re.compile(r'https://scholar.googleusercontent.com(/scholar\.bib\?[^"]*)')
    for div in htmlsoup.find_all("div", {"class":"gs_ri"}):
        title, author, bib_link = "", "", ""
        title = div.h3.text
        author = div.find("div", {"class":"gs_a"}).text
        for link in div.find_all("a"):
            link_url = link.get("href")
            if refre.search(link_url):
                bib_link = link_url
        refs_list.append((title, author, bib_link))
    return refs_list

def return_bib(scholar_bib_url):
    bib = request_page(scholar_bib_url).p.text
    return bib

def main(argv):
    try:
        opts, args = getopt.getopt(argv, "lbuf")
        # print(opts)
        # print(args)
    except getopt.GetoptError:
        print("failed")
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-l':
            links = google_scholar_query(args[0])
            for link in links:
                print("\t".join(link))
        if opt == '-f':
            links = google_scholar_query(args[0])
            print("\t".join(links[0]))
        if opt == '-b':
            links = google_scholar_query(args[0])
            first_link = links[0][2]
            ref = return_bib(first_link)
            print(ref)
        if opt == '-u':
            link = sys.stdin.read().split("\t")[2]
            ref = return_bib(link)
            print(ref)

if __name__ == "__main__":
   main(sys.argv[1:])