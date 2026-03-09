import sys
import pathlib
import click
import panel as pn
from dsm2_calsim_analysis._version import __version__
from dsm2_calsim_analysis.nbplot.setup import (
    _DEFAULT_SCENARIOS,
    _DEFAULT_EC_SCENARIOS,
    _DEFAULT_CALSIM_FILE,
    parse_scenario,
    write_yaml,
    build_flow_config,
    build_ec_config,
    build_ec_vernalis_config,
    build_ec_ag_west_config,
    copy_info_files,
)
pn.extension()
CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(
    __version__, "-v", "--version", message="%(prog)s, version %(version)s"
)
def main():
    """DSM2 Calsim Analysis Tool."""
    pass


@click.command()
@click.argument(
    "config_file",
    type=click.Path(dir_okay=False, exists=True, readable=True),
)
def analyze(config_file):
    """
    Run DSM2 analysis based on the configuration file

    Keyword Arguments:
        config_file -- Configuration file for defining scenarios (default: {"config.yaml"})
    """
    from dsm2_calsim_analysis.nbplot import calsim_dsm2_analysis

    calsim_dsm2_analysis.main(config_file)


@click.command()
@click.option(
    "--scenario", "scenarios", multiple=True, metavar="NAME:PATH",
    default=_DEFAULT_SCENARIOS, show_default=True,
    help="Flow/Vernalis scenario in NAME:PATH format. Repeat for multiple scenarios.",
)
@click.option(
    "--ec-scenario", "ec_scenarios", multiple=True, metavar="NAME:PATH",
    default=_DEFAULT_EC_SCENARIOS, show_default=True,
    help="EC scenario in NAME:PATH format. Repeat for multiple scenarios. "
         "Defaults to --scenario values if omitted.",
)
@click.option(
    "--calsim-file", default=_DEFAULT_CALSIM_FILE, show_default=True, metavar="PATH",
    help="Path to the CalSim DSS file.",
)
@click.option(
    "--period-start", default="1921-01-01", show_default=True, metavar="YYYY-MM-DD",
    help="Start date of the analysis period.",
)
@click.option(
    "--period-end", default="2020-09-30", show_default=True, metavar="YYYY-MM-DD",
    help="End date of the analysis period.",
)
@click.option(
    "--output-dir", default=".", show_default=True,
    type=click.Path(file_okay=False),
    help="Directory where config YAML files will be written.",
)
def setup(scenarios, ec_scenarios, calsim_file, period_start, period_end, output_dir):
    """
    Generate config YAML files for DSM2/CalSim analysis.

    Creates four config files in OUTPUT_DIR:

    \b
      config_flow.yaml       — Monthly flow timelines, barcharts, exceedances, box plots
      config_ec.yaml         — EC vs all D1641 delta standards + general EC plots
      config_ec_vernalis.yaml — Vernalis EC (SALINITY-EC) plots
      config_ec_ag_west.yaml  — EC vs D1641 AG West & Interior Delta only

    An info/ subdirectory with the required station and regulation CSV files
    is also created in OUTPUT_DIR.

    \b
    Example (custom scenarios):
      dsm2-calsim-analysis setup \\
        --scenario "baseline:scenarios/baseline.dss" \\
        --scenario "alt1:scenarios/alt1.dss" \\
        --ec-scenario "baseline:scenarios/baseline_EC_p.dss" \\
        --ec-scenario "alt1:scenarios/alt1_EC_p.dss" \\
        --calsim-file "scenarios/calsim.dss" \\
        --period-start "1921-01-01" \\
        --period-end "2020-09-30" \\
        --output-dir my_analysis

    Running without arguments uses the bundled example scenarios and writes
    config files into the current directory.
    """
    out = pathlib.Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    # Copy bundled info CSVs to output_dir/info/
    info_dst = copy_info_files(out)
    click.echo(f"Copied info files to {info_dst}/")

    period = [period_start, period_end]
    flow_scenarios = [parse_scenario(s) for s in scenarios]
    ec_scen_list = [parse_scenario(s) for s in ec_scenarios]

    configs = {
        "config_flow.yaml":        build_flow_config(flow_scenarios, calsim_file, period),
        "config_ec.yaml":          build_ec_config(ec_scen_list, calsim_file, period),
        "config_ec_vernalis.yaml": build_ec_vernalis_config(flow_scenarios, calsim_file, period),
        "config_ec_ag_west.yaml":  build_ec_ag_west_config(ec_scen_list, calsim_file, period),
    }

    for filename, config in configs.items():
        fpath = out / filename
        write_yaml(fpath, config)
        click.echo(f"Written {fpath}")

    click.echo("\nSetup complete. Run analysis with:")
    for filename in configs:
        click.echo(f"  dsm2-calsim-analysis analyze {out / filename}")


main.add_command(analyze)
main.add_command(setup)

if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
