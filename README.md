# dsm2-calsim-analysis

Python tools for DSM2 and CalSim time series analysis and notebook-based plotting.

## Overview

This package provides utilities for analyzing DSM2 (Delta Simulation Model II) and CalSim water resources model output, including:

- **`dsm2_calsim_analysis.nbplot`** – Interactive notebook plotting tools (Plotly-based) for time series comparison, exceedance curves, and scenario analysis
- **`dsm2_calsim_analysis.utilities`** – Data utilities for reading DSS files, water year type tables, CalSim regulation tables, and computing statistics

## Installation

```bash
pip install git+https://github.com/CADWRDeltaModeling/dsm2-calsim-analysis
```

Or in development mode:

```bash
git clone https://github.com/CADWRDeltaModeling/dsm2-calsim-analysis
cd dsm2-calsim-analysis
pip install -e .
```

## Dependencies

- `pandas`, `numpy`
- `pyhecdss` – for reading HEC-DSS files
- `panel` – for interactive dashboards
- `pyyaml` – for YAML configuration files
- `diskcache` – for caching DSS reads

## Command-line Interface

After installation the `dsm2-calsim-analysis` command is available with two sub-commands.

### `setup` – Generate configuration files

Creates a set of YAML config files and copies the required station/regulation CSV files
into an output directory. Run this once per study to bootstrap a new analysis.

```
dsm2-calsim-analysis setup [OPTIONS]
```

**Options**

| Option | Default | Description |
|---|---|---|
| `--scenario NAME:PATH` | bundled example | Flow/Vernalis scenario (repeat for multiple). |
| `--ec-scenario NAME:PATH` | bundled example | EC scenario DSS file (repeat for multiple). Defaults to `--scenario` values. |
| `--calsim-file PATH` | `scenarios/calsim.dss` | CalSim DSS file used for water-year type classification. |
| `--period-start YYYY-MM-DD` | `1921-01-01` | Start of the analysis period. |
| `--period-end YYYY-MM-DD` | `2020-09-30` | End of the analysis period. |
| `--output-dir DIRECTORY` | `.` | Directory where config files and `info/` CSVs are written. |

**Files produced**

| File | Contents |
|---|---|
| `config_flow.yaml` | Monthly flow timelines, barcharts, exceedance curves, and box-whisker plots |
| `config_ec.yaml` | EC vs all D1641 delta standards (AG, FWS, MI) plus general EC plots |
| `config_ec_vernalis.yaml` | Vernalis EC (`SALINITY-EC`) timelines, barcharts, and exceedance plots |
| `config_ec_ag_west.yaml` | EC vs D1641 AG West & Interior Delta standard only |
| `info/*.csv` | Station location files and D1641 regulation tables (copied from the package) |

**Example**

```bash
dsm2-calsim-analysis setup \
  --scenario "baseline:scenarios/baseline.dss" \
  --scenario "alt1:scenarios/alt1.dss" \
  --ec-scenario "baseline:scenarios/baseline_EC_p.dss" \
  --ec-scenario "alt1:scenarios/alt1_EC_p.dss" \
  --calsim-file "scenarios/calsim.dss" \
  --period-start "1921-01-01" \
  --period-end "2020-09-30" \
  --output-dir my_analysis
```

Running `setup` with no arguments generates configs using the bundled example scenarios
and writes files into the current directory.

---

### `analyze` – Run the interactive dashboard

Launches an interactive Panel/Plotly dashboard for a given config file. The dashboard
opens in a browser window and provides:

- A top-level **dropdown** to switch between the different plot views defined in the config.
- Per-view controls for **Station**, **Variable**, **Water Year Type** toggles, and **Month** toggles (where applicable).
- **Show Data** toggle to display the underlying data table.
- **Save Data** button to export the filtered data as CSV.
- **Export Plots** button to save PNG images for every station.

```
dsm2-calsim-analysis analyze CONFIG_FILE
```

**Example**

```bash
# After running setup:
dsm2-calsim-analysis analyze my_analysis/config_flow.yaml
dsm2-calsim-analysis analyze my_analysis/config_ec.yaml
dsm2-calsim-analysis analyze my_analysis/config_ec_vernalis.yaml
dsm2-calsim-analysis analyze my_analysis/config_ec_ag_west.yaml
```

## Python API

```python
from dsm2_calsim_analysis.nbplot import calsim_dsm2_analysis
from dsm2_calsim_analysis.utilities import read_dss_to_df, read_hist_wateryear_types

# Load a scenario config
config = calsim_dsm2_analysis.load_config("my_analysis/config_flow.yaml")
```

See the [`examples/`](examples/) directory for complete scripts.

## Related Repositories

- [dsm2ui](https://github.com/CADWRDeltaModeling/dsm2ui) – DSM2 interactive UI tools
- [dvue](https://github.com/CADWRDeltaModeling/dvue) – Data visualization UI framework

## License

MIT
