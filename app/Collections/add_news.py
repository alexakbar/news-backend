import requests
import mysql.connector
import os
from datetime import datetime
from dotenv import load_dotenv

# Load the Laravel environment variables
dotenv_path = os.path.join(os.path.dirname(__file__), '../../.env')
load_dotenv(dotenv_path)

# create connection
db = mysql.connector.connect(
    host=os.getenv('DB_HOST'),
    user= os.getenv('DB_USERNAME'),
    passwd= os.getenv("DB_PASSWORD"),
    database= os.getenv("DB_DATABASE")
)

cursor = db.cursor()

# API Key NewsAPI.org
newsapi_key = os.getenv("NEWS_API_KEY")

# API Key The Guardian
guardian_key = os.getenv("THE_GUARDIAN_API_KEY")

# API Key NY Times
nytimes_key = os.getenv("NYTIMES_API_KEY")

# author
authors = []

# insert news each categories from api newsapi.org
# get categories first
sql = "SELECT * FROM categories WHERE source = %s"
val = ('newsapi',)
cursor.execute(sql,val)
categories = cursor.fetchall()
for category in categories:
    name = category[2]
    # get news
    url = "https://newsapi.org/v2/top-headlines"
    response = requests.get(url,{
        'apiKey': newsapi_key,
        'category': name
    })
    data = response.json()
    articles = data['articles']
    for article in articles:
        # check if news exists
        sql = "SELECT * FROM news WHERE title = %s and source = %s"
        val = (article['title'],'newsapi',)
        cursor.execute(sql, val)
        result = cursor.fetchall()
        if len(result) == 0:
            # convert date
            date = datetime.strptime(article['publishedAt'], '%Y-%m-%dT%H:%M:%SZ')
            # insert news
            sql = "INSERT INTO news (title,description,url,image,published_at,source,category,author) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
            val = (article['title'],article['description'],article['url'],article['urlToImage'],date,'newsapi',category[1],article['author'],)
            cursor.execute(sql, val)
            db.commit()
            # check author is not null
            if article['author'] != None:
                authors.append(article['author'])

            print('Inserted '+article['title']+' from newsapi.org')

# print success
print('Success insert news from newsapi.org');

# insert news from api theguardian.com
url = "https://content.guardianapis.com/search"
response = requests.get(url, {
    'api-key': guardian_key
})
data = response.json()
articles = data['response']['results']
for article in articles:
    # check if news exists
    sql = "SELECT * FROM news WHERE title = %s and source = %s"
    val = (article['webTitle'],'theguardian',)
    cursor.execute(sql, val)
    result = cursor.fetchall()
    if len(result) == 0:
        # convert date
        date = datetime.strptime(article['webPublicationDate'], '%Y-%m-%dT%H:%M:%SZ')
        # insert news
        sql = "INSERT INTO news (title,url,published_at,source,category) VALUES (%s,%s,%s,%s,%s)"
        val = (article['webTitle'],article['webUrl'],date,'theguardian',article['sectionName'],)
        cursor.execute(sql, val)
        db.commit()
        print('Inserted '+article['webTitle']+' from theguardian.com')

# print success
print('Success insert news from theguardian.com');

# insert news from api nytimes.com
url = "https://api.nytimes.com/svc/topstories/v2/home.json"
response = requests.get(url, {
    'api-key': nytimes_key
})
data = response.json()
articles = data['results']
for article in articles:
    # check if news exists
    sql = "SELECT * FROM news WHERE title = %s and source = %s"
    val = (article['title'],'nytimes',)
    cursor.execute(sql, val)
    result = cursor.fetchall()
    if len(result) == 0:
        # convert date
        date = datetime.strptime(article['published_date'], '%Y-%m-%dT%H:%M:%S%z')
        # insert news
        sql = "INSERT INTO news (title,description,url,image,published_at,source,category) VALUES (%s,%s,%s,%s,%s,%s,%s)"
        val = (article['title'],article['abstract'],article['url'],article['multimedia'][0]['url'],date,'nytimes',article['section'],)
        cursor.execute(sql, val)
        db.commit()
        if article['byline'] != "":
            if (article['byline'].split('By ').__len__() > 1):
                authors.append(article['byline'].split('By ')[1])
                print(article['byline'].split('By ')[1])
        
        print('Inserted '+article['title']+' from nytimes.com')

# print success
print('Success insert news from nytimes.com');

# add authors
for author in authors:
    # check if author exists
    sql = "SELECT * FROM authors WHERE name = %s"
    val = (author,)
    cursor.execute(sql, val)
    result = cursor.fetchall()
    if len(result) == 0:
        # insert author
        sql = "INSERT INTO authors (name) VALUES (%s)"
        val = (author,)
        cursor.execute(sql, val)
        db.commit()

# print success
print('Success insert authors');
        

# close connection
cursor.close()
db.close()

