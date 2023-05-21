import requests
import mysql.connector

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

# API Key NY Times
nytimes_key = "cMMFA47N2OLC1TFpLGrCdNv0AJB5SxT6"

# insert authors from api newsapi.org
url = "https://newsapi.org/v2/sources"
response = requests.get(url, {
    'apiKey': newsapi_key
})
data = response.json()
sources = data['sources']
for source in sources:
    author = source['name']
    # check if author exists
    sql = "SELECT * FROM authors WHERE name = %s and source = %s"
    val = (author,'newsapi',)
    cursor.execute(sql, val)
    result = cursor.fetchall()
    if len(result) == 0:
        # insert author
        sql = "INSERT INTO authors (name,source) VALUES (%s,%s)"
        val = (author,'newsapi',)
        cursor.execute(sql, val)
        db.commit()

# print
print('Success insert authors from newsapi.org');

# insert authors from api nytimes.com
url = "https://api.nytimes.com/svc/news/v3/content/section-list.json"
response = requests.get(url, {
    'api-key': nytimes_key
})
data = response.json()
sections = data['results']
for section in sections:
    author = section['display_name']
    # check if author exists
    sql = "SELECT * FROM authors WHERE name = %s and source = %s"
    val = (author,'nytimes',)
    cursor.execute(sql, val)
    result = cursor.fetchall()
    if len(result) == 0:
        # insert author
        sql = "INSERT INTO authors (name,source) VALUES (%s,%s)"
        val = (author,'nytimes',)
        cursor.execute(sql, val)
        db.commit()

# print
print('Success insert authors from nytimes.com');
