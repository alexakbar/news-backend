import requests
import mysql.connector
from datetime import datetime

# create connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="1234qwerty",
    database="newspaper_backend"
)

cursor = db.cursor()

# API Key NewsAPI.org
newsapi_key = "6df4cce49cf44e9aa30bcc6ea5caba79"

# API Key The Guardian
guardian_key = "test"

# API Key NY Times
nytimes_key = "cMMFA47N2OLC1TFpLGrCdNv0AJB5SxT6"

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
            sql = "INSERT INTO news (title,description,url,image,publishedAt,source,category) VALUES (%s,%s,%s,%s,%s,%s,%s)"
            val = (article['title'],article['description'],article['url'],article['urlToImage'],date,'newsapi',category[0],)
            cursor.execute(sql, val)
            db.commit()
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
        sql = "INSERT INTO news (title,url,publishedAt,source,category) VALUES (%s,%s,%s,%s,%s)"
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
        sql = "INSERT INTO news (title,description,url,image,publishedAt,source,category) VALUES (%s,%s,%s,%s,%s,%s,%s)"
        val = (article['title'],article['abstract'],article['url'],article['multimedia'][0]['url'],date,'nytimes',article['section'],)
        cursor.execute(sql, val)
        db.commit()
        print('Inserted '+article['title']+' from nytimes.com')

# print success
print('Success insert news from nytimes.com');

# close connection
cursor.close()
db.close()

