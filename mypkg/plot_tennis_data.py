import pandas as pd
import matplotlib.pyplot as plt

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

    ax.set_title("Player’s Professional Matches, Age 14-40", pad=65, fontweight="bold")
    ax.legend(
        loc="upper center",
        bbox_to_anchor=(0.5, 1.10),
        ncol=2,
        frameon=False
    )

    ax.xaxis.tick_top()
    ax.xaxis.set_label_position("top")

    ax.set_xticks(range(14, 42, 2))

    ax.set_yticks([-20, -10, 0, 10, 20])
    ax.set_yticklabels(["−20", "−10", "Same age", "+10", "+20 years"])

    ax.set_axisbelow(True)
    ax.grid(alpha=0.25)
    plt.savefig('./scatter_plot.png', dpi=300, bbox_inches='tight')
    plt.show()
    return fig