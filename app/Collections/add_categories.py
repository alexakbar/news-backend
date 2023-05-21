import requests
import mysql.connector
from slugify import slugify

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


# insert categories from api newsapi.org
url = f"https://newsapi.org/v2/sources"
response = requests.get(url,{
    'apiKey': newsapi_key
})
data = response.json()
sources = data['sources']
for source in sources:
    category = source['category']
    slug = slugify(source['category'])

    # check if category exists
    sql = "SELECT * FROM categories WHERE name = %s and source = %s"
    val = (category,'newsapi',)
    cursor.execute(sql, val)
    result = cursor.fetchall()
    if len(result) == 0:
        # insert category
        sql = "INSERT INTO categories (name,source,slug) VALUES (%s,%s,%s)"
        val = (category,'newsapi',slug,)
        cursor.execute(sql, val)
        db.commit()
    
# print
print('Success insert categories from newsapi.org');

# insert categories from api theguardian.com
url = f"https://content.guardianapis.com/sections"
response = requests.get(url, {
    'api-key': guardian_key
})
data = response.json()
sections = data['response']['results']
for section in sections:
    category = section['webTitle']
    slug = slugify(section['webTitle'])

    # check if category exists
    sql = "SELECT * FROM categories WHERE name = %s and source = %s"
    val = (category,'theguardian',)
    cursor.execute(sql, val)
    result = cursor.fetchall()
    if len(result) == 0:
        # insert category
        sql = "INSERT INTO categories (name,source,slug) VALUES (%s,%s,%s)"
        val = (category,'theguardian',slug,)
        cursor.execute(sql, val)
        db.commit()
# print
print('Success insert categories from theguardian.com');

# insert categories from api nytimes.com
url = "https://api.nytimes.com/svc/news/v3/content/section-list.json"
response = requests.get(url, {
    'api-key': nytimes_key
})
data = response.json()
sections = data['results']
for section in sections:
    category = section['section']
    slug = slugify(section['section'])
    
    # check if category exists
    sql = "SELECT * FROM categories WHERE name = %s and source = %s"
    val = (category,'nytimes',)
    cursor.execute(sql, val)
    result = cursor.fetchall()
    if len(result) == 0:
        # insert category
        sql = "INSERT INTO categories (name,source,slug) VALUES (%s,%s,%s)"
        val = (category,'nytimes',slug,)
        cursor.execute(sql, val)
        db.commit()
        
# print
print('Success insert categories from nytimes.com');

# close connection
db.close()


