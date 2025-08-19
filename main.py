import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os


def create_continents_graph(
    csv_file,
    custom_title=None,
    custom_x_labels=None,
    label_map=None,
    y_unit="percent",  # "percent" or "proportion"
):
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
    y_unit (str, optional):
        - "percent" (default): y-axis from 0 to 100 with label "Percent".
        - "proportion": y-axis from 0.0 to 1.0 with label "Proportion".
          If the data appears to be in 0–100 scale (max > 1), it will be auto-scaled by dividing by 100.
    """
    df = pd.read_csv(csv_file, index_col=0)

    # If proportions are requested but the data looks like percents, normalize to 0..1
    if y_unit == "proportion":
        try:
            max_val = np.nanmax(df.values.astype(float))
            if max_val > 1.0 + 1e-9:
                df = df / 100.0
        except Exception:
            # If conversion fails, proceed without normalization
            pass
    if y_unit == "proportion":
        plt.ylabel("Proportion", fontsize=12)
    else:
        plt.ylabel("Percent", fontsize=12)

    title = custom_title if custom_title else os.path.splitext(os.path.basename(csv_file))[0]
    plt.title(title, fontsize=14, loc="center")

    plt.grid(True, alpha=0.3)
    plt.legend(bbox_to_anchor=(1.05, 1), loc="upper left")

    # Set y-axis limits based on chosen unit
    if y_unit == "proportion":
        plt.ylim(0.0, 1.0)
    else:
        plt.ylim(0, 100)

    plt.tight_layout()

    # Generate output filename
    base_name = os.path.splitext(csv_file)[0]
    output_file = f"{base_name}_recreated.png"
    plt.savefig(output_file, dpi=300, bbox_inches="tight")

    print(f"Graph saved as '{output_file}'")
    return output_file


if __name__ == "__main__":
    # Default usage with original CSV file (percent scale)
    # create_continents_graph("5_continents_81.csv")

    # Example with:
    # - custom title,
    # - x-axis label mapping (dict),
    # - legend label mapping (dict),
    # - y-axis as proportion (0.0–1.0)
    x_label_map = {
        "V1": "Alpha",
        "V2": "Delta",
        "V3": "Omi BA.1",
        "V4": "Omi BA.2",
        "V5": "Other Omi",
    }

    legend_label_map = {
        "NAm": "N. Amer.",
        "SAm": "S. Amer.",
        "Eur": "Europe",
        "Asia": "Asia",
        "Afr": "Africa",
    }

    # Use y_unit="proportion" for 0.0–1.0 scale with "Proportion" label.
    # If the CSV values are 0–100, they will be auto-scaled to 0–1.
    # create_continents_graph("cont_071525_17943_.csv", y_unit="proportion")

    create_continents_graph("cont_81_.csv", "81", x_label_map, legend_label_map, y_unit="proportion")