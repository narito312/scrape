# import requests
# import os
# import pprint

# def getBookByTitle(title):
#     response = requests.get(f"https://api.mangadex.org/manga?title={title}&limit=1")
#     data = response.json()
#     data = data.get("data")
#     attributes = data[0].get('attributes')
#     title = attributes.get('title')
#     pprint.pprint(title)

# getBookByTitle("one")

import requests
import pprint

def searchTitles(title, limit):
    url = "https://api.mangadex.org/manga"
    params = {
        "limit": limit,
        "title": title,
        "includedTagsMode": "AND",
        "excludedTagsMode": "OR",
        "contentRating[]": ["safe", "suggestive", "erotica"],
        "order[latestUploadedChapter]": "desc",
    }

    headers = {"accept": "application/json"}

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        #pprint.pprint(data)
        return data  # Print the response JSON
    else:
         print(f"Error: {response.status_code}")

data = searchTitles("hello", 19)

for manga in data["data"]:
    print(manga["attributes"]["description"].get("en"))#["title"]["en"])




