# %% [markdown]
# # Python Notebook to Analyze EC Standards
#
# Yu Zhou, 2023-5
#
# This tool is a proto-type to visualize EC standards for LTO DSM2.
#
# The input files are post-processd (daily/monthly) DSS files.

# %%
# Import modules
import pandas as pd

# import plotly.offline as py
# py.init_notebook_mode(connected=True)
import pydelmod.utilities as pdmu
import pydelmod.nbplot as pdmn

# %%
# Read output locations
fpath_output_locations = "./info/DSM2_ec_loc_stds.csv"
df_stations = pd.read_csv(fpath_output_locations, comment="#")
df_stations["ID"] = [x.upper() for x in df_stations["ID"]]
station_ids = df_stations["ID"].values
stations_to_read = df_stations["ID"].values

# %% [markdown]
# # Build Dataframe for All the Analyzed Data

# %%
# Read in scenarios
dir_scenarios = "./scenarios"
scenarios = [
    {
        "name": "1ex_2020",
        "fpath": dir_scenarios + "/1ex_2020_EC_p.dss",
    },
    {
        "name": "7pp_2020",
        "fpath": dir_scenarios + "/7pp_2020_EC_p.dss",
    },
]
# Read water year types
wyt_c3f2020 = dir_scenarios + "/calsim.dss"
df_wyt2020 = pdmu.read_calsim3_wateryear_types(wyt_c3f2020)

# period93 = ['1922-10-1','2015-9-30']
period93 = ["1921-10-1", "2021-9-30"]

# %%
# df_ec = pdmu.prep_df(scenarios,stations_to_read,['EC-MEAN', 'EC-MAX', 'EC-HT-MEAN'],['1DAY', '1MON'],df_wyt2020,period93)
df_ec = pdmu.prep_df(
    scenarios, stations_to_read, ["EC-MEAN"], ["1DAY"], df_wyt2020, period93
)
df_1day = df_ec[df_ec["interval"] == "1DAY"]
df_davg = df_1day[df_1day["variable"] == "EC-MEAN"]

# %% [markdown]
# ## D1641 Agricultural Standards

# %% [markdown]
# Check D1641 details
#
# https://www.waterboards.ca.gov/waterrights/board_decisions/adopted_orders/decisions/d1600_d1649/wrd1641_1999dec29.pdf
#
# Page 182-187, Table 2-3

# %% [markdown]
# ### D1641_AG West&Interior Delta: 14-day running average of daily mean EC

# %%
fpath_d1641_ag = "./info/D1641_AG_wiDelta.csv"
df_reg_ag = pdmu.read_regulations(fpath_d1641_ag, df_wyt2020)
df_reg_ag["value"] = df_reg_ag["value"] * 1000.0  # Convert milli to micro
reg_ag_loc = df_reg_ag.location.unique()
df_stations_reg_ag = df_stations[df_stations["ID"].isin(reg_ag_loc)]
# df_stations_reg_ag

# %%
# df_1day = df_ec[df_ec['interval'] == '1DAY']
# df_davg = df_1day[df_1day['variable'] == 'EC-MEAN']
df_davg_ag = df_davg[df_davg["station"].isin(reg_ag_loc)]

# %%
# Get the time range from the data set
df_reg_ag_ts = pdmu.generate_regulation_timeseries(df_reg_ag, df_davg_ag, freq="D")
df_reg_ag_ts["variable"] = "EC-MEAN-14DAY"
df_reg_ag_ts["scenario_name"] = "D1641 AG WI"
# df_reg_ag_ts.hvplot.line()

# %%
options = {
    "yaxis_name": "14-day running average EC (mmhos/cm)",
    "title": "EC 14-Day Mean for D1641_AG West&Interior Delta Timelines",
}
pdmn.plot_step_w_regulation(df_davg_ag, df_reg_ag_ts, df_stations_reg_ag, options)

# %%
options = {
    "yaxis_name": "14-day running average EC - standard (mmhos/cm)",
    "title": "EC 14-Day Mean for D1641_AG West&Interior Delta Exceedances",
}
pdmn.plot_exceedance_w_regulation(df_davg_ag, df_reg_ag_ts, df_stations_reg_ag, options)

# %% [markdown]
# ### D1641_AG South Delta: 30-day running average of daily mean EC

# %%
fpath_d1641_ag2 = "./info/D1641_AG_sDelta.csv"
df_reg_ag2 = pdmu.read_regulations(fpath_d1641_ag2, df_wyt2020)
df_reg_ag2["value"] = df_reg_ag2["value"] * 1000.0  # Convert milli to micro
reg_ag_loc2 = df_reg_ag2.location.unique()
df_stations_reg_ag2 = df_stations[df_stations["ID"].isin(reg_ag_loc2)]
# df_stations_reg_ag2

# %%
df_davg_ag2 = df_davg[df_davg["station"].isin(reg_ag_loc2)]

# %%
# Get the time range from the data set
df_reg_ag_ts2 = pdmu.generate_regulation_timeseries(df_reg_ag2, df_davg_ag2, freq="D")
df_reg_ag_ts2["variable"] = "EC-MEAN-30DAY"
df_reg_ag_ts2["scenario_name"] = "D1641 AG South"
# df_reg_ag_ts2.hvplot.line()

# %% [markdown]
# O&M:
#
# start checking on Apr.30, check prev30d-avg; if exceed 700, count 30day, the entire month
#
# May.1, if exceed, count 1day
#
# notebook:
#
# didn't follow the 1st
#
# start checking on Apr.1, count days

# %%
options = {
    "yaxis_name": "30-day running average EC (mmhos/cm)",
    "title": "EC 30-Day Mean for D1641_AG South Delta Timelines",
}
pdmn.plot_step_w_regulation(df_davg_ag2, df_reg_ag_ts2, df_stations_reg_ag2, options)

# %%
options = {
    "yaxis_name": "30-day running average EC - standard (mmhos/cm)",
    "title": "EC 30-Day Mean for D1641_AG South Delta Exceedances",
}
pdmn.plot_exceedance_w_regulation(
    df_davg_ag2, df_reg_ag_ts2, df_stations_reg_ag2, options
)

# %% [markdown]
# ### todo, change to monthly

# %% [markdown]
# ### D1641_AG Export Area: monthly average of daily mean EC

# %%
fpath_d1641_ag3 = "./info/D1641_AG_export.csv"
df_reg_ag3 = pdmu.read_regulations(fpath_d1641_ag3, df_wyt2020)
df_reg_ag3["value"] = df_reg_ag3["value"] * 1000.0  # Convert milli to micro
reg_ag_loc3 = df_reg_ag3.location.unique()
df_stations_reg_ag3 = df_stations[df_stations["ID"].isin(reg_ag_loc3)]
# df_stations_reg_ag3

# %%
df_davg_ag3 = df_davg[df_davg["station"].isin(reg_ag_loc3)]

# %%
# Get the time range from the data set
df_reg_ag_ts3 = pdmu.generate_regulation_timeseries(df_reg_ag3, df_davg_ag3, freq="D")
df_reg_ag_ts3["variable"] = "EC-MEAN-30DAY"
df_reg_ag_ts3["scenario_name"] = "D1641 AG Export"
# df_reg_ag_ts3.hvplot.line()

# %%
options = {
    "yaxis_name": "monthly average EC (mmhos/cm)",
    "title": "EC Monthly Mean for D1641_AG Export Timelines",
}
pdmn.plot_step_w_regulation(df_davg_ag3, df_reg_ag_ts3, df_stations_reg_ag3, options)

# %%
options = {
    "yaxis_name": "monthly average EC - standard (mmhos/cm)",
    "title": "EC Monthly Mean for D1641_AG Export Exceedances",
}
pdmn.plot_exceedance_w_regulation(df_davg, df_reg_ag_ts3, df_stations_reg_ag3, options)

# %% [markdown]
# ## D1641 Fish and Wildlife standards

# %% [markdown]
# ### D1641_FWS San Joaquin River: 14-day running average of daily mean EC

# %%
# df_1day = df_ec[df_ec['interval'] == '1DAY']
# df_davg = df_1day[df_1day['variable'] == 'EC-MEAN']

# %%
fpath_d1641_fws_sjr = "./info/D1641_FWS_SJR.csv"
df_reg_fws_sjr = pdmu.read_regulations(fpath_d1641_fws_sjr, df_wyt2020)
df_reg_fws_sjr["value"] = df_reg_fws_sjr["value"] * 1000.0  # Convert milli to micro
reg_fws_sjr_loc = df_reg_fws_sjr.location.unique()
df_stations_reg_fws_sjr = df_stations[df_stations["ID"].isin(reg_fws_sjr_loc)]
# df_stations_reg_fws_sjr

# %%
df_davg_fws_sjr = df_davg[df_davg["station"].isin(reg_fws_sjr_loc)]

# %%
# Get the time range from the data set
df_reg_fws_ts_sjr = pdmu.generate_regulation_timeseries(
    df_reg_fws_sjr, df_davg_fws_sjr, freq="D"
)
df_reg_fws_ts_sjr["variable"] = "EC-MEAN-14DAY"
df_reg_fws_ts_sjr["scenario_name"] = "D1641 FWS SJR"
# df_reg_fws_ts_sjr.hvplot.line()

# %%
options = {
    "yaxis_name": "14-day running average EC (mmhos/cm)",
    "title": "EC 14-Day Mean for D1641_FWS San Joaquin River Timelines",
}
pdmn.plot_step_w_regulation(
    df_davg_fws_sjr, df_reg_fws_ts_sjr, df_stations_reg_fws_sjr, options
)

# %%
options = {
    "yaxis_name": "14-day running average EC - standard (mmhos/cm)",
    "title": "EC 14-Day Mean for D1641_FWS San Joaquin River Exceedances",
}
pdmn.plot_exceedance_w_regulation(
    df_davg_fws_sjr, df_reg_fws_ts_sjr, df_stations_reg_fws_sjr, options
)

# %% [markdown]
# ### D1641_FWS Suisun Area: monthly average of daily max EC

# %%
df_dmax = pdmu.prep_df(
    scenarios, stations_to_read, ["EC-MAX"], ["1DAY"], df_wyt2020, period93
)

# %%
# df_dmax = df_1day[df_1day['variable'] == 'EC-MAX']

# %%
fpath_d1641_fws_suisun = "./info/D1641_FWS_Suisun.csv"
df_reg_fws_suisun = pdmu.read_regulations(fpath_d1641_fws_suisun, df_wyt2020)
df_reg_fws_suisun["value"] = (
    df_reg_fws_suisun["value"] * 1000.0
)  # Convert milli to micro
reg_fws_suisun_loc = df_reg_fws_suisun["location"].unique()
df_stations_reg_fws_suisun = df_stations[df_stations["ID"].isin(reg_fws_suisun_loc)]
# df_stations_reg_fws_suisun

# %%
df_dmax_fws_suisun = df_dmax[df_dmax["station"].isin(reg_fws_suisun_loc)]

# %%
# Get the time range from the data set
df_reg_fws_suisun_ts = pdmu.generate_regulation_timeseries(
    df_reg_fws_suisun, df_dmax_fws_suisun, freq="D"
)
df_reg_fws_suisun_ts["variable"] = "EC-MAX-MEAN"
df_reg_fws_suisun_ts["scenario_name"] = "D1641 FWS Suisun"
# df_reg_fws_suisun_ts.hvplot.line()

# %%
options = {
    "yaxis_name": "EC Monthly Mean of Daily Max (mmhos/cm)",
    "title": "EC Monthly Mean of Daily Max for D1641_FWS Suisun Timelines",
}
pdmn.plot_step_w_regulation(
    df_dmax_fws_suisun, df_reg_fws_suisun_ts, df_stations_reg_fws_suisun, options
)

# %%
options = {
    "yaxis_name": "Diff in EC scenario-standard (mmhos/cm)",
    "title": "EC Monthly Mean of Daily Max for D1641_FWS Suisun Exceedances",
}
pdmn.plot_exceedance_w_regulation(
    df_dmax_fws_suisun, df_reg_fws_suisun_ts, df_stations_reg_fws_suisun, options
)

# %% [markdown]
# D1641-FWS Suisun Stations: monthly average of daily average of two high-tide EC

# %%
# df_1day = df_ec[df_ec['interval'] == '1DAY']
# df_dht = df_1day[df_1day['variable'] == 'EC-HT-MEAN']

# %%
# df_dht

# %%
# fpath_d1641_fwss = './info/D1641_FWS_Standards_Suisun1.csv'
# df_reg_fwss = pdmu.read_regulations(fpath_d1641_fwss, df_wyt)
# df_reg_fwss['value'] = df_reg_fwss['value'] * 1000.  # Convert milli to micro
# df_stations_reg_fwss = df_stations[df_stations['ID'].isin(df_reg_fwss['location'].unique())]
# df_stations_reg_fwss

# %%
# options = {'yaxis_name': 'EC Monthly Mean of Daily Average of High-Tide (mmhos/cm)', 'title': 'D1641 FWS Suisun'}
# pdmn.plot_step_w_regulation(df_dht, df_reg_fws_tss, df_stations_reg_fwss, options)

# %%
# options = {'yaxis_name': 'Diff in EC scenario-standard (mmhos/cm)', 'title': 'EC Monthly Mean of Daily Average of High-Tide'}
# pdmn.plot_exceedance_w_regulation(df_dht, df_reg_fws_tss, df_stations_reg_fwss, options)

# %% [markdown]
# ## D1641 Municipal & Industrial standards

# %% [markdown]
# ### D1641_MI Contra Costa: daily mean Chloride 250 mg/L

# %%
fpath_d1641_mi = "./info/D1641_MI_250.csv"
df_reg_mi = pdmu.read_regulations(fpath_d1641_mi, df_wyt2020)
reg_mi_loc = df_reg_mi.location.unique()
df_stations_reg_mi = df_stations[df_stations["ID"].isin(reg_mi_loc)]
# df_stations_reg_mi

# %%
reg_mi_loc

# %%
df_davg.station.unique()

# %%
df_davg_mi = df_davg[df_davg["station"].isin(reg_mi_loc)]

# %%
df_davg_cl = df_davg_mi
df_davg_cl["value"] = df_davg_cl.apply(
    lambda x: max(x["value"] * 0.15 - 12.0, x["value"] * 0.285 - 50), axis=1
)
df_davg_cl["variable"] = "Chloride-MEAN"
# df_davg_cl

# %%
# Get the time range from the data set
df_reg_mi_ts = pdmu.generate_regulation_timeseries(df_reg_mi, df_davg_mi, freq="D")
df_reg_mi_ts["variable"] = "Chloride-MEAN"
df_reg_mi_ts["scenario_name"] = "D1641 MI 250"
# df_reg_mi_ts

# %%
options = {
    "yaxis_name": "Chloride Daily (mg/L)",
    "title": "Chloride Daily for D1641 MI 250 Timelines",
}
pdmn.plot_step_w_regulation(df_davg_cl, df_reg_mi_ts, df_stations_reg_mi, options)

# %%
options = {
    "yaxis_name": "Chloride Daily -standard (mg/L)",
    "title": "Chloride Daily for D1641 MI 250 Exceedances",
}
pdmn.plot_exceedance_w_regulation(df_davg_cl, df_reg_mi_ts, df_stations_reg_mi, options)

# %% [markdown]
# ### D1641_MI Contra Costa: daily mean Chloride 150 mg/L

# %%
fpath_d1641_mi2 = "./info/D1641_MI_150.csv"
df_reg_mi2 = pdmu.read_regulations(fpath_d1641_mi2, df_wyt2020)
reg_mi_loc2 = df_reg_mi2.location.unique()
df_stations_reg_mi2 = df_stations[df_stations["ID"].isin(reg_mi_loc2)]
# df_stations_reg_mi2

# %%
df_davg_mi2 = df_davg[df_davg["station"].isin(reg_mi_loc2)]

# %%
# Get the time range from the data set
df_reg_mi_ts2 = pdmu.generate_regulation_timeseries(df_reg_mi2, df_davg_mi2, freq="D")
df_reg_mi_ts2["variable"] = "Chloride-MEAN"
df_reg_mi_ts2["scenario_name"] = "D1641 MI 150"
# df_reg_mi_ts2

# %%
df_davg_cl2 = df_davg_mi2
df_davg_cl2["value"] = df_davg_cl2.apply(
    lambda x: max(x["value"] * 0.15 - 12.0, x["value"] * 0.285 - 50), axis=1
)
df_davg_cl2["cl_minus_reg"] = df_davg_cl2.apply(lambda x: x["value"] - 150, axis=1)
df_davg_cl2["cl_meet"] = df_davg_cl2["cl_minus_reg"].map(lambda x: x <= 0)
# df_davg_cl2


# %%
# Define an aggregation function to count days when the regulation is met.
# According to D1641:
# Maximum mean daily 150 mg/l Cl−for at least the number of days shown
# during the Calendar Year.
# Must be provided in intervals of not less than two weeks duration.
def sum_only_more_than_14days(series):
    total = 0
    cumsum = 0
    for x in series:
        if x:
            cumsum += 1
        else:
            if cumsum >= 14:
                total += cumsum
            cumsum = 0
    if cumsum >= 14:
        total += cumsum
    return total


# %%
df_davg_cl2pl = (
    df_davg_cl2.groupby(["scenario_name", "year"])["cl_meet"]
    .agg(sum_only_more_than_14days)
    .to_frame()
)
df_davg_cl2pl["n_records"] = df_davg_cl2.groupby(["scenario_name", "year"])[
    "year"
].count()
df_davg_cl2pl.reset_index(inplace=True)
import calendar

df_davg_cl2pl["days_in_year"] = df_davg_cl2pl["year"].map(
    lambda x: 366 if calendar.isleap(x) else 365
)
df_davg_cl2pl = df_davg_cl2pl[
    df_davg_cl2pl["n_records"] == df_davg_cl2pl["days_in_year"]
]
df_davg_cl2pl["time"] = df_davg_cl2pl["year"]
df_davg_cl2pl.time = pd.to_datetime(df_davg_cl2pl.time, format="%Y")
df_davg_cl2pl["value"] = df_davg_cl2pl["cl_meet"]
df_davg_cl2pl["station"] = "ROLD024"
df_davg_cl2pl["variable"] = "Chloride-MEAN"
df_davg_cl2pl = df_davg_cl2pl.merge(
    df_davg_cl2[["time", "scenario_name", "sac_yrtype"]],
    on=["time", "scenario_name"],
    how="left",
)
# df_davg_cl2pl

# %% [markdown]
# Calendar year 1923-2014, only 92years applicable

# %%
options = {
    "yaxis_name": "Number of days in year under regulation (day)",
    "title": "Yearly number of days for D1641 MI 150 Timelines",
}
pdmn.plot_step_w_regulation(df_davg_cl2pl, df_reg_mi_ts2, df_stations_reg_mi2, options)

# %%
options = {
    "yaxis_name": "Number of days under regulation - standard (day)",
    "title": "Yearly number of days for D1641 MI 150 Exceedances",
}
pdmn.plot_exceedance_w_regulation(
    df_davg_cl2pl, df_reg_mi_ts2, df_stations_reg_mi2, options
)

# %%
