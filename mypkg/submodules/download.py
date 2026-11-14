import json
import pandas as pd
from urllib.request import Request, urlopen
import re

def download_data(name, career=True):
    # process playername to be case insensitive
    split_name = name.split(" ")
    player_name = ""
    for word in split_name:
        player_name += word[0].upper() + word[1:]

    # extract json
    if career:
        filename = player_name + "Career.js"
    else:
        filename = player_name + ".js"

    url = "https://www.tennisabstract.com/jsmatches/"+filename
    request = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urlopen(request, timeout=30) as response:
        text = response.read().decode("utf-8")

    if not career:
        dob = text.split("var dob=", 1)[1].split(";", 1)[0].strip()
        return pd.to_datetime(dob, format="%Y%m%d")
    
    # Parse the match array inside the JavaScript file
    start = text.index("[[")
    matches, _ = json.JSONDecoder().raw_decode(text[start:])

    data = pd.DataFrame(matches)
    return data