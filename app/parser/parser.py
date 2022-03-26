import requests 
from bs4 import BeautifulSoup
import time

from datetime import datetime




headers = {
        "user-agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36"

    }
url = "https://cointelegraph.com/"


# def get_first_news():
#     printing = False
#     r = requests.get(url=url, headers = headers)

#     soup = BeautifulSoup(r.text,"lxml")

#     news_dict = {}
#     separate_text_terminal(True, printing)

#     article_cards = soup.find_all("li", class_ = "posts-listing__item")
#     for article in article_cards:
#         if is_topic(article):
#             article_title = article.find("a", class_ = "post-card__title-link").text.strip()
#             article_date = article.find("footer", class_ = "post-card__footer").find("time").get("datetime")
#             article_time = article.find("footer", class_ = "post-card__footer").find("time").text.strip()
#             article_desc = article.find("div", class_ = "post-card__text-wrp").find("p").text.strip()
#             article_url = get_link(url, article.find("a").get("href")[1:])
#             article_id = get_article_id(article_url)

#             news_dict[article_id]= {
#                 "article_date" : article_date,
#                 "article_time" : get_time(article_date, article_time),
#                 "article_title" : article_title,
#                 "article_desc" : article_desc,
#                 "article_url" : article_url
#                     }
#             if printing:
#                     print(f"{article_title} \n{article_url} \n{article_date}\n{article_time}\n{article_desc}")
#         if printing: 
#             print("\n")

    

#     separate_text_terminal(False,printing)

def is_topic(article):
     if article.find("a", class_ = "post-card__title-link") is not None:
            if article.find("footer", class_ = "post-card__footer") is not None:
                if article.find("footer", class_ = "post-card__footer").find("time") is not None:
                    if article.find("div", class_ = "post-card__text-wrp") is not None:
                        return True
            return False

def get_current_news():
    r = requests.get(url=url, headers = headers)

    soup = BeautifulSoup(r.text,"lxml")

    article_cards = soup.find_all("li", class_ = "posts-listing__item")
    fresh_news = {}
    for article in article_cards:
        if is_topic(article):
            article_url = get_link(url, article.find("a").get("href")[1:])
            article_id = get_article_id(article_url)
            
            article_title = article.find("a", class_ = "post-card__title-link").text.strip()
            article_date = article.find("footer", class_ = "post-card__footer").find("time").get("datetime")
            article_time = article.find("footer", class_ = "post-card__footer").find("time").text.strip()
            article_desc = article.find("div", class_ = "post-card__text-wrp").find("p").text.strip()

            fresh_news[article_id]={
                "article_date" : article_date,
                "article_time" : get_time(article_date, article_time),
                "article_title" : article_title,
                "article_description" : article_desc,
                "article_link" : article_url
            }
    return fresh_news


def get_time(d, n):
    datesecs = datetime.strptime(d, "%Y-%m-%d").timestamp()
    quan_time, text_time = n.split(' ')[0], n.split(' ')[1]

    time_dictionary = {'minute' : 60, 'minutes' : 60, 'hour' : 3600, 'hours' : 3600}
    
    if text_time not in time_dictionary:
        return time.time()- 60*60*24

    datecur = time.time() -  time_dictionary[text_time]*int(quan_time)

    return datecur

def get_link(url, link):
    if url in link:
        return link
    else:
        return url + link

def get_article_id(article_url):
    return article_url.split("/")[-1]


def main():
    #get_first_news()
    counter = 1 + 1
    #check_news_update()

if __name__ == "__main__":
    main()

main()

        



