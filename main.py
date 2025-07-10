import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os


def create_continents_graph(csv_file, custom_title=None, custom_x_labels=None):
    """
    Create a line graph from CSV data with continents.

    Parameters:
    csv_file (str): Path to the CSV file
    custom_title (str, optional): Custom title for the graph. If None, uses filename.
    custom_x_labels (list, optional): Custom labels for x-axis. If None, uses CSV headers.
    """
    df = pd.read_csv(csv_file, index_col=0)

    plt.figure(figsize=(12, 8))

    colors = {
        "S Amer": "#1f77b4",  # Blue
        "N Amer": "#ff7f0e",  # Orange
        "Eur": "#2ca02c",  # Green
        "Asia": "#17becf",  # Light blue
        "Afr": "#9467bd",  # Purple
    }

    # Use custom x-axis labels if provided, otherwise use CSV headers
    x_labels = custom_x_labels if custom_x_labels else df.columns.tolist()

    for continent in df.index:
        plt.plot(
            x_labels,
            df.loc[continent],
            marker="o",
            linewidth=2,
            markersize=6,
            color=colors.get(continent, "#1f77b4"),
            label=continent,
        )

    plt.xlabel("Variables", fontsize=12)
    plt.ylabel("Percent", fontsize=12)

    # Use custom title if provided, otherwise use filename
    if custom_title:
        title = custom_title
    else:
        title = os.path.splitext(os.path.basename(csv_file))[0]

    plt.title(title, fontsize=14, loc="center")
    plt.grid(True, alpha=0.3)
    plt.legend(bbox_to_anchor=(1.05, 1), loc="upper left")

    plt.ylim(0, 100)

    plt.tight_layout()

    # Generate output filename
    base_name = os.path.splitext(csv_file)[0]
    output_file = f"{base_name}_recreated.png"
    plt.savefig(output_file, dpi=300, bbox_inches="tight")

    print(f"Graph saved as '{output_file}'")
    return output_file


# Example usage - default behavior
if __name__ == "__main__":
    # Default usage with original CSV file
    create_continents_graph("5_continents_81.csv")

    # Example with custom title and x-axis labels
    # create_continents_graph("5_continents_81.csv",
    #                        custom_title="Continental Data Analysis",
    #                        custom_x_labels=["Quarter 1", "Quarter 2", "Quarter 3", "Quarter 4", "Quarter 5"])
