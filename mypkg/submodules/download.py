import json
import pandas as pd
from urllib.request import Request, urlopen

def download_data(name):
    # process playername to be case insensitive
    split_name = name.split(" ")
    player_name = ""
    for word in split_name:
        player_name += word[0].upper() + word[1:]

    # extract json
    filename = player_name + ".js"
    url = "https://www.tennisabstract.com/jsmatches/"+filename
    request = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urlopen(request, timeout=30) as response:
        text = response.read().decode("utf-8")

    # Parse the match array inside the JavaScript file
    start = text.index("[[")
    matches, _ = json.JSONDecoder().raw_decode(text[start:])

    data = pd.DataFrame(matches)

    return data