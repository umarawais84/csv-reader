import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os


def create_continents_graph(
    csv_file,
    custom_title=None,
    custom_x_labels=None,  # list/tuple in display order OR dict old->new
    label_map=None,  # dict of index label remapping for legend
    y_unit="percent",  # "percent" or "proportion"
):
    """
    Create a multi-line graph from a CSV where rows are series (e.g., continents)
    and columns are categories along the x-axis.

    Parameters:
    - csv_file (str): Path to the CSV file. First column is treated as the index (series names).
    - custom_title (str, optional): Title for the plot. Defaults to filename stem.
    - custom_x_labels (list/tuple|dict, optional):
        * If list/tuple: explicit labels for x-ticks in the same order as the CSV columns.
        * If dict: mapping of original column names -> display names.
        * If None: use CSV column names.
    - label_map (dict, optional): Mapping of original index labels -> legend display labels.
    - y_unit (str): "percent" (0..100) or "proportion" (0.0..1.0). For "proportion",
      if values look like percents (max>1), they are auto-scaled by 100.
    """
    # Load and coerce numeric values
    df = pd.read_csv(csv_file, index_col=0)
    df = df.apply(pd.to_numeric, errors="coerce")

    # Apply legend label mapping (index rename)
    if label_map:
        df = df.rename(index=label_map)

    # X labels handling
    x_tick_labels = None
    if isinstance(custom_x_labels, dict):
        df = df.rename(columns=custom_x_labels)
    elif isinstance(custom_x_labels, (list, tuple)):
        if len(custom_x_labels) != df.shape[1]:
            raise ValueError(
                f"custom_x_labels length {len(custom_x_labels)} != number of columns {df.shape[1]}"
            )
        x_tick_labels = list(custom_x_labels)

    # Drop empty rows/cols
    df = df.dropna(how="all")
    df = df.dropna(axis=1, how="all")
    if df.empty:
        raise ValueError("No numeric data to plot after cleaning the CSV.")

    # Normalize if proportion requested and data looks like percents
    if y_unit == "proportion":
        try:
            max_val = np.nanmax(df.values.astype(float))
            if max_val > 1.0 + 1e-9:
                df = df / 100.0
        except Exception:
            pass

    # Prepare figure/axes and x coordinates
    fig, ax = plt.subplots(figsize=(10, 6))
    columns = list(df.columns)
    x = np.arange(len(columns))
    if x_tick_labels is None:
        x_tick_labels = columns

    # Plot each row as a line (one per series)
    for idx, row in df.iterrows():
        y = row.values.astype(float)
        ax.plot(x, y, marker="o", linewidth=2, label=str(idx))

    # Labels, title, grid, and limits
    if y_unit == "proportion":
        ax.set_ylabel("Proportion", fontsize=12)
        ax.set_ylim(0.0, 1.0)
    else:
        ax.set_ylabel("Percent", fontsize=12)
        ax.set_ylim(0, 100)

    title = custom_title if custom_title else os.path.splitext(os.path.basename(csv_file))[0]
    ax.set_title(title, fontsize=14, loc="center")

    ax.set_xticks(x)
    ax.set_xticklabels(x_tick_labels, rotation=0)
    ax.grid(True, alpha=0.3)

    # Add legend only after plotting
    handles, labels = ax.get_legend_handles_labels()
    if handles:
        ax.legend(bbox_to_anchor=(1.05, 1), loc="upper left")

    fig.tight_layout()

    # Save figure
    base_name = os.path.splitext(csv_file)[0]
    output_file = f"{base_name}_recreated.png"
    fig.savefig(output_file, dpi=300, bbox_inches="tight")
    plt.close(fig)

    print(f"Graph saved as '{output_file}'")
    return output_file


if __name__ == "__main__":
    # Example label mappings
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

    # If CSV values are 0–100 and y_unit="proportion", they will be auto-scaled to 0–1.
    create_continents_graph(
        "cont_81_.csv",
        "81",
        x_label_map,
        legend_label_map,
        y_unit="proportion",
    )