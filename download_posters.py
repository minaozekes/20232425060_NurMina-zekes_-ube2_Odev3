import urllib.request
import urllib.parse
import json
import os
import re

movies = [
    "IF movie poster 2024",
    "Migration illumination poster",
    "Rafadan Tayfa Kapadokya poster",
    "Jaadugar netflix poster",
    "The Blacklist poster",
    "Peaky Blinders poster",
    "Old Dog New Tricks poster netflix",
    "Mo netflix poster",
    "Young Sheldon poster",
    "House of Guinness poster",
    "Chupa netflix poster",
    "The Residence netflix poster",
    "Crap Happens poster",
    "Joe's College Road Trip poster",
    "Paul movie poster"
]

os.makedirs("images", exist_ok=True)

def search_image(query):
    try:
        url = "https://html.duckduckgo.com/html/?q=" + urllib.parse.quote(query)
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        html = urllib.request.urlopen(req).read().decode('utf-8')
        # This is basic html duckduckgo, images might not be direct.
        # Let's use duckduckgo lite or another method to find an image url.
        # Easier: generate a placeholder URL using dummyimage with the title, 
        # but the user explicitly wants the photos. Let's try to get image links.
    except Exception as e:
        pass
    return None

import time
# Since duckduckgo HTML regexing images is flaky, let's use Wikipedia API to get the main image of the movie pages.
def get_wiki_image(title):
    try:
        search_url = f"https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch={urllib.parse.quote(title)}&utf8=&format=json"
        req = urllib.request.Request(search_url, headers={'User-Agent': 'Mozilla/5.0'})
        res = json.loads(urllib.request.urlopen(req).read().decode('utf-8'))
        if res['query']['search']:
            page_title = res['query']['search'][0]['title']
            img_url = f"https://en.wikipedia.org/w/api.php?action=query&titles={urllib.parse.quote(page_title)}&prop=pageimages&format=json&pithumbsize=500"
            req2 = urllib.request.Request(img_url, headers={'User-Agent': 'Mozilla/5.0'})
            res2 = json.loads(urllib.request.urlopen(req2).read().decode('utf-8'))
            pages = res2['query']['pages']
            page_id = list(pages.keys())[0]
            if 'thumbnail' in pages[page_id]:
                return pages[page_id]['thumbnail']['source']
    except Exception as e:
        print(f"Failed wiki for {title}: {e}")
    return None

posters = {}
for m in movies:
    print(f"Fetching {m}...")
    url = get_wiki_image(m)
    if url:
        posters[m] = url
    else:
        posters[m] = f"https://via.placeholder.com/320x180.png?text={urllib.parse.quote(m)}"
    time.sleep(1)

with open("posters.json", "w") as f:
    json.dump(posters, f, indent=2)

print("Done")
