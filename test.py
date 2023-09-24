import requests
import os
from dotenv import load_dotenv

load_dotenv()

url = "https://newsapi.org/v2/top-headlines"
response = requests.get(
    url,
    params={
        "apiKey": os.getenv('NEWSAPI_API_KEY'),
        "language": "en",
        "sources": "bbc-news,the-verge,google-news",
        "pageSize": 5
    }
)
# Export the data for use in future steps
results = response.json()
articles = results['articles']
headlines = [line['title'] for line in articles]
print(headlines)