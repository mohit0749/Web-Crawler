
import urllib2
def get_page(url):
    try:
        return urllib2.urlopen(url).read()
    except:
        return ''
    return ""

def union(a, b):
    for e in b:
        if e not in a:
            a.append(e)

def get_next_target(page):
    start_link = page.find('<a href=')
    if start_link == -1: 
        return None, 0
    start_quote = page.find('"', start_link)
    end_quote = page.find('"', start_quote + 1)
    url = page[start_quote + 1:end_quote]
    return url, end_quote
            
def get_all_links(page):
    links = []
    while True:
        url, endpos = get_next_target(page)
        if url:
            links.append(url)
            page = page[endpos:]
        else:
            break
    return links

def lookup(index, keyword):
    if keyword in index:
        return index[keyword]
    else:
        return []
def add_to_index(index, keyword, url):
    if keyword in index:
        if url not in index[keyword]:
               index[keyword].append(url)
        else:return        
    else:
        index[keyword] = [url]

def add_page_to_index(index, url, content):
    words = content.split()
    for word in words:
        add_to_index(index, word, url)
    

def compute_ranks(graph):
    d = 0.8 # damping factor
    numloops = 10
    ranks = {}
    npages = len(graph)
    for page in graph:
        ranks[page] = 1.0 / npages
    for i in range(0, numloops):
        newranks = {}
        for page in graph:
            newrank = (1 - d) / npages
            for inlink in graph:
                if page in graph[inlink]:
                   newrank=newrank+(ranks[inlink]*d)/len(graph[inlink])
            newranks[page] = newrank
        ranks = newranks
    return ranks   

def crawl_web(seed): # returns index, graph of inlinks
    tocrawl = [seed]
    crawled = []
    graph = {}  # <url>, [list of pages it links to]
    index = {}
    maxcrawl=5
    print "\nSearchig your results..."
    while tocrawl: 
        page = tocrawl.pop()
        if page not in crawled:
            if maxcrawl<0:break
            content = get_page(page)
            add_page_to_index(index, page, content)
            outlinks = get_all_links(content)
            graph[page] = outlinks
            union(tocrawl, outlinks)
            crawled.append(page)
            maxcrawl-=1
    return index, graph
def qs(pages,ranks):
    if len(pages)>1:
        piv=ranks[pages[0]]
        i=1
        j=1
        for j in range(1,len(pages)):
            if ranks[pages[j]]>piv:
                pages[i],pages[j]=pages[j],pages[i]
                i+=1
        pages[i-1],pages[0]=pages[0],pages[i-1]
        qs(pages[1:i],ranks)
        qs(pages[i+1:],ranks)

def newlookup(index,ranks,keywords):
    pages=lookup(index,keywords)
    if pages==[]:
        print "Result not found"
        return 
    print "\nPrinting the Found results:\n"
    qs(pages,ranks)
    num=0
    for i in pages:
        num+=1
        print str(num)+' : '+i+'\n'
        
print "Enter the Seed Page :"
seed_page=raw_input()
print "Enter What you want to search :"
search_term=raw_input()

index,graph=crawl_web(seed_page)
rank=compute_ranks(graph)
print 'Search Compltete.'
newlookup(index,rank,search_term)
                  
