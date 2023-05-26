import requests
import mysql.connector
import os
from slugify import slugify
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


