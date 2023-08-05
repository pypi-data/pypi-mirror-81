from pathlib import Path
import pandas as pd


def load_excavators(cleaned=False):
    """
    Helper function to load excavator toy dataset.

    Hodkiewicz, M., and Ho, M. (2016)
    "Cleaning historical maintenance work order data for reliability analysis"
    in Journal of Quality in Maintenance Engineering, Vol 22 (2), pp. 146-163.

    BscStartDate| Asset | OriginalShorttext | PMType | Cost
    --- | --- | --- | --- | ---
    initialization of MWO | which excavator this MWO concerns (A, B, C, D, E)| natural language description of the MWO| repair (PM01) or replacement (PM02) | MWO expense (AUD)

    Args:
        cleaned (bool): whether to return the original dataset (False) or the dataset with
            keyword extraction rules applied (True), as described in Hodkiewicz and Ho (2016)

    Returns:
        pandas.DataFrame: raw data for use in testing nestor and subsequent workflows
        
    """
    module_path = Path(__file__).parent
    if cleaned:
        csv_filename = module_path / "excavators-cleaned.csv"
    else:
        csv_filename = module_path / "excavators.csv"

    df = pd.read_csv(csv_filename)
    df["BscStartDate"] = pd.to_datetime(df.BscStartDate)
    return df
