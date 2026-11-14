import pandas as pd
import matplotlib.pyplot as plt
from math import ceil, floor

def plot_tennis_data(df):
    
    fig, ax = plt.subplots(figsize=(14, 8))
    for result, color, label in [
        ("W", "skyblue", "Matches won"),
        ("L", "#843c87", "Matches lost"),

    ]: 
        subset = df[df["result"] == result]
        ax.scatter(
        subset["player_age"],
        subset["age_diff"],
        color=color,
        label=label,
        s=20,
        alpha=0.8
    )

    ax.legend(
        loc="upper center",
        bbox_to_anchor=(0.5, 1.10),
        ncol=2,
        frameon=False
    )

    ages = df["player_age"].dropna()
    title = "Player’s Professional Matches"

    if not ages.empty:
        min_age = floor(ages.min())
        max_age = ceil(ages.max())
        title += f", Ages {min_age}–{max_age}"

        ticks = list(range(min_age, max_age + 1, 2))
        if ticks[-1] != max_age:
            ticks.append(max_age)

        ax.set_xticks(ticks)
        ax.set_xlim(min_age - 0.5, max_age + 0.5)

    ax.set_title(title, pad=65, fontweight="bold")

    ax.xaxis.tick_top()
    ax.xaxis.set_label_position("top")

    ax.set_yticks([-20, -10, 0, 10, 20])
    ax.set_yticklabels(["−20", "−10", "Same age", "+10", "+20 years"])

    ax.set_axisbelow(True)
    ax.grid(alpha=0.25)
    plt.show()
    return fig