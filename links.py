import requests
from bs4 import BeautifulSoup

def make_query_string ():
    q = input("query: ")
    q = q.lower().replace(' ','+')
    return "https://www.google.com/search?&q="+q

def recieve_search_links ():
    root_url = make_query_string ()
    data = requests.get(root_url).text
    links = BeautifulSoup(data, 'html.parser').find_all('a', href=True)

    temp = []
    for link in links:
        temp.append(link['href'])
    return parse_links(temp)

def parse_links (links):
    temp = []
    for link in links:
        if link[:4] == '/url':
            temp.append(link[7:])
    return temp 

def parse_page (url):
    data = requests.get(url).text
    text = BeautifulSoup (data, 'html.parser').text
    return text

def make_word_list (text):
    words = text.lower().split()
    temp = []
    for word in words:
        if len(word) == 0:
            pass
        else:
            temp.append(word)
    return temp 

def keywords (wordlist):
    hotwords = dict()
    for word in wordlist:
        if word not in hotwords.keys():
            hotwords[word] = 1
        else:
            hotwords[word] += 1

    hotwords = dict (sorted(hotwords.items(), key=lambda item: item[1], reverse=True))
    return clean_word_relevance (hotwords)

def clean_word_relevance (wordmap):
    temp = list()
    bad_words = ['for', 'in', 'a', 'the', 'but','is', '&', 'if']
    bw_count = 0
    for word in wordmap.items():    
        if word[-1] != 1:
            if word[0] not in bad_words:
                temp.append(word)
            else:
                bw_count += 1
    return temp

def main ():
    search_links = recieve_search_links ()

    print ()
    for link in search_links:
        print(link)
        page = parse_page(link)
        wl = make_word_list(page)
        print ("length: "+str(len(page)))
        print (keywords(wl))
    print ()

if __name__ == '__main__':
    main ()
