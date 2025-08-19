# Heat-health warning system preventing rising global heat-related mortality in a warming climate: projections through 2090

---

## Overview
Core code for heatwave-related mortality and early warning benefits.
The uploaded script `core_pipeline.py` implements the **four key components** of the analysis:

1. **Baseline threshold (97.5th percentile)**  
   - Combine baseline temperature files and compute the 97.5th percentile for each grid cell.  

2. **Heatwave days**  
   - Count the number of days above the baseline threshold for future climate scenarios.  

3. **Excess deaths (ED)**  
   - Calculate annual excess deaths.

4. **Early warning benefits**  
   - Estimate benefits for population ≥65 and <65 years, based on reduced risk per heatwave day.  

This simplified version contains only the **core logic**.  
Large raw datasets and intermediate heavy processing steps are omitted.  

---

## File description

- `core_pipeline.py` — main script, organized into four functions (`calculate_baseline_threshold`, `count_heatwave_days`, `calculate_excess_deaths`, `calculate_early_warning_benefits`).  
  Each function can be run independently by providing the corresponding input files.  

---

