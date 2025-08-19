import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os


def create_continents_graph(csv_file, custom_title=None, custom_x_labels=None, label_map=None):
    """
    Create a line graph from CSV data with continents.

    Parameters:
    csv_file (str): Path to the CSV file
    custom_title (str, optional): Custom title for the graph. If None, uses filename.
    custom_x_labels (list|dict, optional):
        - If list/tuple: Display labels in the same order as the CSV columns (length must match).
        - If dict: Mapping of original CSV column names -> display names (e.g., {"V1": "alpha"}).
        - If None: Uses the CSV column names as-is.
    label_map (dict, optional):
        Mapping of original legend labels (index values) -> display names
        (e.g., {"NAm": "N. Amer."}). If None, uses index values as-is.
    """
    df = pd.read_csv(csv_file, index_col=0)

    plt.figure(figsize=(12, 8))

    colors = {
        "S Amer": "#1f77b4",  # Blue
        "SAm": "#1f77b4",
        "South America": "#1f77b4",
        "N Amer": "#ff7f0e",  # Orange
        "NAm": "#ff7f0e",
        "North America": "#ff7f0e",
        "Eur": "#2ca02c",     # Green
        "Europe": "#2ca02c",
        "Asia": "#17becf",    # Light blue
        "Afr": "#9467bd",     # Purple
        "Africa": "#9467bd",
    }

    # Build x-axis labels
    if isinstance(custom_x_labels, dict):
        # Map each original column to a display label; default to the original name if missing
        x_labels = [custom_x_labels.get(col, col) for col in df.columns]
    elif isinstance(custom_x_labels, (list, tuple, pd.Index, np.ndarray)):
        if len(custom_x_labels) != len(df.columns):
            raise ValueError(
                f"custom_x_labels has length {len(custom_x_labels)} but there are {len(df.columns)} CSV columns."
            )
        x_labels = list(custom_x_labels)
    elif custom_x_labels is None:
        x_labels = df.columns.tolist()
    else:
        raise TypeError("custom_x_labels must be a list/tuple/array, a dict, or None.")

    # Plot each continent/series
    for series_name in df.index:
        y_values = df.loc[series_name].values
        display_label = label_map.get(series_name, series_name) if label_map else series_name

        plt.plot(
            x_labels,
            y_values,
            marker="o",
            linewidth=2,
            markersize=6,
            color=colors.get(series_name, None),  # fall back to matplotlib default if not found
            label=display_label,
        )

    plt.xlabel("Variables", fontsize=12)
    plt.ylabel("Percent", fontsize=12)

    title = custom_title if custom_title else os.path.splitext(os.path.basename(csv_file))[0]
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


if __name__ == "__main__":
    # Default usage with original CSV file
    create_continents_graph("5_continents_81.csv")

    # Example with:
    # - custom title,
    # - x-axis label mapping (dict),
    # - legend label mapping (dict)
    x_label_map = {
        "V1": "alpha",
        "V2": "bravo",
        "V3": "charlie",
        "V4": "delta",
        "V5": "echo",
    }

    legend_label_map = {
        "NAm": "N. Amer.",
        "SAm": "S. Amer.",
        "Eur": "Europe",
        "Asia": "Asia",
        "Afr": "Africa",
  
    }