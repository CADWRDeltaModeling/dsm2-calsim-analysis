"""
Functions for generating DSM2/CalSim analysis config YAML files.
"""
import pathlib
import shutil

import click


_DEFAULT_SCENARIOS = (
    "1ex_2020c:scenarios/1ex_2020c.dss",
    "9b_v2_2020:scenarios/9b_v2_2020.dss",
)
_DEFAULT_EC_SCENARIOS = (
    "1ex_2020:scenarios/1ex_2020_EC_p.dss",
    "7pp_2020:scenarios/7pp_2020_EC_p.dss",
)
_DEFAULT_CALSIM_FILE = "scenarios/calsim.dss"


def parse_scenario(value):
    """Parse a 'name:path' scenario string into a dict."""
    parts = value.split(":", 1)
    if len(parts) != 2:
        raise click.BadParameter(
            f"Expected format NAME:PATH, got: {value!r}"
        )
    return {"name": parts[0].strip(), "fpath": parts[1].strip()}


def write_yaml(path, data):
    """Write a config dict to a YAML file with clean formatting."""
    import yaml

    class _StrDumper(yaml.Dumper):
        pass

    def _str_representer(dumper, value):
        return dumper.represent_scalar("tag:yaml.org,2002:str", value)

    _StrDumper.add_representer(str, _str_representer)

    with open(path, "w") as f:
        yaml.dump(data, f, Dumper=_StrDumper, default_flow_style=False, allow_unicode=True)


def build_flow_config(scenarios, calsim_file, period):
    return {
        "output_locations": "info/DSM2_bnd_loc.csv",
        "scenarios": scenarios,
        "variable": "FLOW",
        "interval": "1MON",
        "calsim_file": calsim_file,
        "period": period,
        "plots": [
            {"type": "plot_step_w_variable_station_filters",
             "options": {"yaxis_name": "Monthly Mean Flow (cfs)", "title": "Flow Monthly Mean Timelines"}},
            {"type": "plot_bar_monthly_w_controls",
             "options": {"yaxis_name": "Monthly Mean Flow (cfs)", "title": "Flow Monthly Barcharts of Monthly Mean"}},
            {"type": "plot_exceedance_w_variable_station_filters",
             "options": {"yaxis_name": "Monthly Mean Flow (cfs)", "title": "Flow Monthly Mean Exceedances"}},
            {"type": "plot_box_w_variable_station_filters",
             "options": {"xaxis_name": "Monthly Mean Flow (cfs)", "title": "Flow Monthly Mean Box-Whiskers"}},
        ],
    }


def build_ec_config(ec_scenarios, calsim_file, period):
    return {
        "output_locations": "info/DSM2_ec_loc_stds.csv",
        "scenarios": ec_scenarios,
        "variable": "EC-MEAN",
        "interval": "1DAY",
        "calsim_file": calsim_file,
        "delta_standards": [
            {"name": "D1641 AG WI",      "fpath": "info/D1641_AG_wiDelta.csv", "variable": "EC-MEAN-14DAY"},
            {"name": "D1641 AG South",   "fpath": "info/D1641_AG_sDelta.csv",  "variable": "EC-MEAN-30DAY"},
            {"name": "D1641 AG Export",  "fpath": "info/D1641_AG_export.csv",  "variable": "EC-MEAN-30DAY"},
            {"name": "D1641 FWS SJR",    "fpath": "info/D1641_FWS_SJR.csv",   "variable": "EC-MEAN-14DAY"},
            {"name": "D1641 FWS Suisun", "fpath": "info/D1641_FWS_Suisun.csv","variable": "EC-MAX-MEAN"},
            {"name": "D1641 MI 250",     "fpath": "info/D1641_MI_250.csv",     "variable": "Chloride-MEAN"},
            {"name": "D1641 MI 150",     "fpath": "info/D1641_MI_150.csv",     "variable": "Chloride-MEAN"},
        ],
        "period": period,
        "plots": [
            {"type": "plot_step_w_regulation",
             "options": {"yaxis_name": "14-day running average EC - standard (mmhos/cm)",
                         "title": "EC 14-Day Mean for D1641_AG West&Interior Delta Timelines",
                         "delta_standard": "D1641 AG WI"}},
            {"type": "plot_exceedance_w_regulation",
             "options": {"yaxis_name": "14-day running average EC - standard (mmhos/cm)",
                         "title": "EC 14-Day Mean for D1641_AG West&Interior Delta Exceedances",
                         "delta_standard": "D1641 AG WI"}},
            {"type": "plot_step_w_regulation",
             "options": {"yaxis_name": "30-day running average EC - standard (mmhos/cm)",
                         "title": "EC 30-Day Mean for D1641_AG South Delta Timelines",
                         "delta_standard": "D1641 AG South"}},
            {"type": "plot_exceedance_w_regulation",
             "options": {"yaxis_name": "30-day running average EC - standard (mmhos/cm)",
                         "title": "EC 30-Day Mean for D1641_AG South Delta Exceedances",
                         "delta_standard": "D1641 AG South"}},
            {"type": "plot_step_w_regulation",
             "options": {"yaxis_name": "30-day running average EC - standard (mmhos/cm)",
                         "title": "EC 30-Day Mean for D1641_AG Export Timelines",
                         "delta_standard": "D1641 AG Export"}},
            {"type": "plot_exceedance_w_regulation",
             "options": {"yaxis_name": "30-day running average EC - standard (mmhos/cm)",
                         "title": "EC 30-Day Mean for D1641_AG Export Exceedances",
                         "delta_standard": "D1641 AG Export"}},
            {"type": "plot_step_w_regulation",
             "options": {"yaxis_name": "14-day running average EC - standard (mmhos/cm)",
                         "title": "EC 14-Day Mean for D1641_FWS San Joaquin River Timelines",
                         "delta_standard": "D1641 FWS SJR"}},
            {"type": "plot_exceedance_w_regulation",
             "options": {"yaxis_name": "14-day running average EC - standard (mmhos/cm)",
                         "title": "EC 14-Day Mean for D1641_FWS San Joaquin River Exceedances",
                         "delta_standard": "D1641 FWS SJR"}},
            {"type": "plot_step_w_regulation",
             "options": {"yaxis_name": "EC Monthly Mean of Daily Max (mmhos/cm)",
                         "title": "EC Monthly Mean of Daily Max for D1641_FWS Suisun Timelines",
                         "delta_standard": "D1641 FWS Suisun"}},
            {"type": "plot_exceedance_w_regulation",
             "options": {"yaxis_name": "Diff in EC scenario-standard (mmhos/cm)",
                         "title": "EC Monthly Mean of Daily Max for D1641_FWS Suisun Exceedances",
                         "delta_standard": "D1641 FWS Suisun"}},
            {"type": "plot_step_w_regulation",
             "options": {"yaxis_name": "Chloride Daily (mg/L)",
                         "title": "Chloride Daily for D1641 MI 250 Timelines",
                         "delta_standard": "D1641 MI 250"}},
            {"type": "plot_exceedance_w_regulation",
             "options": {"yaxis_name": "Chloride Daily - standard (mg/L)",
                         "title": "Chloride Daily for D1641 MI 250 Exceedances",
                         "delta_standard": "D1641 MI 250"}},
            {"type": "plot_step_w_regulation",
             "options": {"yaxis_name": "Number of days in year under regulation (day)",
                         "title": "Yearly number of days for D1641 MI 150 Timelines",
                         "delta_standard": "D1641 MI 150"}},
            {"type": "plot_exceedance_w_regulation",
             "options": {"yaxis_name": "Number of days under regulation - standard (day)",
                         "title": "Yearly number of days for D1641 MI 150 Exceedances",
                         "delta_standard": "D1641 MI 150"}},
            {"type": "plot_step_w_variable_station_filters",
             "options": {"yaxis_name": "Daily Mean EC (mmhos/cm)", "title": "EC Daily Mean Timelines"}},
            {"type": "plot_bar_monthly_w_controls",
             "options": {"yaxis_name": "Daily Mean EC (mmhos/cm)", "title": "EC Monthly Barcharts of Daily Mean"}},
            {"type": "plot_exceedance_w_variable_station_filters",
             "options": {"yaxis_name": "Daily Mean EC (mmhos/cm)", "title": "EC Daily Mean Exceedances"}},
            {"type": "plot_box_w_variable_station_filters",
             "options": {"yaxis_name": "Daily Mean EC (mmhos/cm)", "title": "EC Daily Mean Box-Whiskers"}},
        ],
    }


def build_ec_vernalis_config(scenarios, calsim_file, period):
    return {
        "output_locations": "info/DSM2_ec_vernalis_loc.csv",
        "scenarios": scenarios,
        "variable": "SALINITY-EC",
        "interval": "1DAY",
        "calsim_file": calsim_file,
        "period": period,
        "plots": [
            {"type": "plot_step_w_variable_station_filters",
             "options": {"yaxis_name": "Daily Mean EC (mmhos/cm)", "title": "EC Daily Mean Timelines"}},
            {"type": "plot_bar_monthly_w_controls",
             "options": {"yaxis_name": "Daily Mean EC (mmhos/cm)", "title": "EC Monthly Barcharts of Daily Mean"}},
            {"type": "plot_exceedance_w_variable_station_filters",
             "options": {"yaxis_name": "Daily Mean EC (mmhos/cm)", "title": "EC Daily Mean Exceedances"}},
            {"type": "plot_box_w_variable_station_filters",
             "options": {"yaxis_name": "Daily Mean EC (mmhos/cm)", "title": "EC Daily Mean Box-Whiskers"}},
        ],
    }


def build_ec_ag_west_config(ec_scenarios, calsim_file, period):
    return {
        "output_locations": "info/DSM2_ec_loc_stds.csv",
        "scenarios": ec_scenarios,
        "variable": "EC-MEAN",
        "interval": "1DAY",
        "calsim_file": calsim_file,
        "delta_standards": [
            {"name": "D1641 AG WI", "fpath": "info/D1641_AG_wiDelta.csv", "variable": "EC-MEAN-14DAY"},
        ],
        "period": period,
        "plots": [
            {"type": "plot_step_w_regulation",
             "options": {"yaxis_name": "14-day running average EC - standard (mmhos/cm)",
                         "title": "EC 14-Day Mean for D1641_AG West&Interior Delta Timelines",
                         "delta_standard": "D1641 AG WI"}},
            {"type": "plot_exceedance_w_regulation",
             "options": {"yaxis_name": "14-day running average EC - standard (mmhos/cm)",
                         "title": "EC 14-Day Mean for D1641_AG West&Interior Delta Exceedances",
                         "delta_standard": "D1641 AG WI"}},
        ],
    }


def copy_info_files(output_dir):
    """Copy bundled info CSVs to output_dir/info/ and return the destination path."""
    info_src = pathlib.Path(__file__).parent.parent / "data" / "info"
    info_dst = pathlib.Path(output_dir) / "info"
    info_dst.mkdir(parents=True, exist_ok=True)
    for csv_file in info_src.glob("*.csv"):
        shutil.copy2(csv_file, info_dst / csv_file.name)
    return info_dst
