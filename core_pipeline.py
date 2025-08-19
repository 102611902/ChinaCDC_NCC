"""
Core analysis pipeline: Baseline threshold, Heatwave days, Excess deaths (ED), and Early warning benefits.

This simplified code is adapted from the full analysis in:
[Your paper citation, DOI]

Note:
- Large raw datasets are NOT included here.
- Example toy data can be placed in ./data/example/ for demonstration.
- File paths should be adapted to your own directory structure.
"""

import pandas as pd
import numpy as np
import os

# --------------------------------------------------
# 1. Baseline threshold (97.5th percentile)
# --------------------------------------------------
def calculate_baseline_threshold(baseline_dir, output_file):
    """
    Combine baseline temperature files and compute 97.5th percentile per grid cell.

    Parameters
    ----------
    baseline_dir : str
        Path to baseline CSV files.
    output_file : str
        Output CSV with baseline 97.5th percentile values.
    """
    files = [os.path.join(baseline_dir, f) for f in os.listdir(baseline_dir) if f.endswith(".csv")]
    dfs = [pd.read_csv(f) for f in files]
    baseline_all = pd.concat(dfs, axis=1)

    # Compute 97.5 percentile along rows
    percent975 = baseline_all.quantile(0.975, axis=1)
    percent975.to_csv(output_file, index=False)
    print(f"Baseline 97.5th percentile saved to {output_file}")


# --------------------------------------------------
# 2. Heatwave days (days above threshold)
# --------------------------------------------------
def count_heatwave_days(future_dir, threshold_file, output_dir):
    """
    Count number of days above baseline 97.5th percentile for each scenario/model.

    Parameters
    ----------
    future_dir : str
        Path to future climate data (organized by scenario/model/year).
    threshold_file : str
        CSV file with baseline 97.5th percentile values.
    output_dir : str
        Directory to save heatwave days counts.
    """
    threshold = pd.read_csv(threshold_file)

    for scenario in os.listdir(future_dir):
        scen_path = os.path.join(future_dir, scenario)
        for model in os.listdir(scen_path):
            model_path = os.path.join(scen_path, model)
            for fname in os.listdir(model_path):
                year = fname[-8:-4]
                data = pd.read_csv(os.path.join(model_path, fname))
                data.rename(columns={'Unnamed: 0': 'FID'}, inplace=True)
                FID = data['FID']
                temps = data.drop(columns=['FID'])

                # Boolean mask where temp >= threshold
                exceed = temps.ge(threshold['Percent975'], axis=0)
                counts = exceed.sum(axis=1)

                out = pd.DataFrame({"FID": FID, "HeatwaveDays": counts})
                outname = os.path.join(output_dir, f"{scenario}_{model}_{year}.csv")
                out.to_csv(outname, index=False)
    print(f"Heatwave days results saved to {output_dir}")


# --------------------------------------------------
# 3. Excess deaths (ED = ER * D)
# --------------------------------------------------
def calculate_excess_deaths(er_file, mortality_file, output_file):
    """
    Compute annual excess deaths using ER values and mortality data.

    Parameters
    ----------
    er_file : str
        CSV with annual ER values per grid.
    mortality_file : str
        CSV with annual mean daily deaths per grid.
    output_file : str
        Output CSV with ED values.
    """
    ER = pd.read_csv(er_file)
    D = pd.read_csv(mortality_file)

    df_out = pd.DataFrame()
    df_out['FID'] = ER['FID']

    for col in ER.columns[1:]:  # skip FID
        year = col.split("_")[-1]
        # ED = ER * D (per year)
        df_out[f"ED_{year}"] = ER[col] * D[f"Deaths-{year}"]

    df_out.to_csv(output_file, index=False)
    print(f"Excess deaths saved to {output_file}")


# --------------------------------------------------
# 4. Early warning benefits
# --------------------------------------------------
def calculate_early_warning_benefits(heatwave_file, pop65_file, pop_u65_file, output_file):
    """
    Estimate early warning benefits for populations >=65 and <65.

    Parameters
    ----------
    heatwave_file : str
        CSV with annual heatwave days per grid.
    pop65_file : str
        CSV with >=65 population per grid per year.
    pop_u65_file : str
        CSV with <65 population per grid per year.
    output_file : str
        Output CSV with benefits.
    """
    df_hw = pd.read_csv(heatwave_file)
    df65 = pd.read_csv(pop65_file)
    df_u65 = pd.read_csv(pop_u65_file)

    df_out = pd.DataFrame()
    df_out['FID'] = df_hw['FID']

    for col in df_hw.columns[1:]:
        year = col.split("_")[-1]
        # Benefits: days * population * rate
        benefit = (df65[f"Pop65-{year}"] * df_hw[col]) * 5/1e6 \
                  + (df_u65[f"PopU65-{year}"] * df_hw[col]) * 0.0127/1e6
        df_out[f"Benefit_{year}"] = benefit

    df_out.to_csv(output_file, index=False)
    print(f"Early warning benefits saved to {output_file}")


# --------------------------------------------------
# Main pipeline (example usage)
# --------------------------------------------------
if __name__ == "__main__":
    # Example (paths must be adapted to your data)
    # Step 1
    # calculate_baseline_threshold("data/baseline/", "outputs/baseline_percent975.csv")

    # Step 2
    # count_heatwave_days("data/future/", "outputs/baseline_percent975.csv", "outputs/heatwave_days/")

    # Step 3
    # calculate_excess_deaths("data/example/ER.csv", "data/example/mortality.csv", "outputs/excess_deaths.csv")

    # Step 4
    # calculate_early_warning_benefits("data/example/heatwave_days.csv",
    #                                  "data/example/pop65.csv",
    #                                  "data/example/popu65.csv",
    #                                  "outputs/early_warning_benefits.csv")

    print("Core pipeline ready. Uncomment steps above to run with your data.")
