# Tennis Career Match Analysis

**Jackie Dai · STAT 159 · Homework 3**

This Python package retrieves a player's career match data from [Tennis Abstract](https://www.tennisabstract.com/). It provides two public functions. One returns a pandas DataFrame ready for plotting, and the other uses that DataFrame to recreate the age comparison scatter plot from Homework 2.

## Installation

Install the package directly from GitHub. Replace `YOUR_GITHUB_OWNER` with the account or organization that owns the repository.

```bash
python -m pip install git+https://github.com/YOUR_GITHUB_OWNER/hw03-3-jackie-dai.git
```

## Usage

```python
from mypkg import get_tennis_data, plot_tennis_data

serena = get_tennis_data("Serena Williams")
plot_tennis_data(serena)

nadal = get_tennis_data("Rafael Nadal")
plot_tennis_data(nadal)
```

Player names can be entered as `"serena williams"`, `"Serena Williams"`, or `"SerenaWilliams"`. The scatter plot shows the player's age at the time of each match on the x-axis and the player's age minus the opponent's age on the y-axis, in years. Positive values mean the player was older than the opponent. Points are colored by whether the player won or lost.

## Data source

Tennis Abstract's career match files report opponent ages in two formats. Serena Williams's file provides opponent birth dates, which are used with match dates to calculate ages. Rafael Nadal's file provides opponent ages directly. The package uses those values to put the two files into a common format for plotting. Fetching career data requires an internet connection.

## Reflection

This project proved to be difficult especially because I had never done anything related to developing a package before. I didn't think I would spend that much time on the coding part because I had already done most of the work already in hw2. However, there proved to be a lot of small details that had to be generalized. For example, generalizing to all tennis players introduced inconsistency in the opponents birthdates. For women, it was their birthday date, but for men it was just the age directly. This seemed like a easy fix but it led to more issues beacuse of the way I wrote my download script. Overall I think this project was really helpful and it felt cool to be able to develop a project which I'm sure I'll do again in the future.
