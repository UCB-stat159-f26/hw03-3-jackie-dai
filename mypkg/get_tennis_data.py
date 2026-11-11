from .submodules.download import download_data

def get_tennis_data(player_name):
    # input: player name string
    # output: data frame 
    file = download_data(player_name)
    print(file)