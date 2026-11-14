from .submodules.download import download_data
import pandas as pd
import re


def get_tennis_data(player_name):
    # input: player name string
    # output: data frame 
    data = download_data(player_name)

    # proces file 
    data = data[[0, 1, 2, 4, 11, 16]].rename(
        columns={
            0: "date",
            1: "tournament",
            2: "surface",
            4: "result",
            11: "opponent_name",
            16: "opponent_age_or_birthdate"
        }
    )

    data["date"] = pd.to_datetime(data["date"].astype("string"), format="%Y%m%d", errors="coerce")
    player_birthdate = pd.to_datetime(str(download_data(player_name, career=False)))

    raw = data["opponent_age_or_birthdate"].astype("string").str.strip()
    is_birthdate = raw.str.fullmatch(r"\d{8}", na=False)

    opponent_birthdate = pd.to_datetime(
        raw.where(is_birthdate), format="%Y%m%d", errors="coerce"
    )
    age_from_birthdate = (data["date"] - opponent_birthdate).dt.days / 365.25
    age_from_file = pd.to_numeric(raw.where(~is_birthdate), errors="coerce")

    data["opponent_age"] = age_from_file.where(~is_birthdate, age_from_birthdate)
    data["player_age"] = (data["date"] - player_birthdate).dt.days / 365.25
    data["age_diff"] = data["player_age"] - data["opponent_age"]

    return data.dropna(subset=["age_diff"])
