import logging

import click

from graviteeio_cli.lint.gio_linter import Gio_linter
from graviteeio_cli.lint.formats import document
# from graviteeio_cli.graviteeio.utils import filter_api_values
from graviteeio_cli.resolvers.api_conf_resolver import ApiConfigResolver
from graviteeio_cli.lint.types.enums import DiagLevel
from graviteeio_cli.core.output import OutputFormatType

# from graviteeio_cli.http_client.apim.api import ApiClient


logger = logging.getLogger("command-apim-def-lint")


@click.command(short_help="examine api definition configuration generated for possible issues.")
@click.option(
    '--def-path', 'config_path', default=".",
    type=click.Path(exists=False),
    required=False,
    help="Path where api definition is generated. The default value is the current directory"
)
@click.option(
    '--file', '-f',
    type=click.Path(exists=True), required=False,
    help="Value file"
)
@click.option(
    '--set', '-s', multiple=True,
    help="Overload the value(s) of value file eg: `--set proxy.groups[0].name=mynewtest`"
)
@click.pass_obj
def lint(obj, config_path, file, set):
    """This command allow to run a serie of tests to verify thaht api definition configuration is correctly formed."""

    api_resolver = ApiConfigResolver(config_path, file)
    api_def_config = api_resolver.get_api_data(debug=False, set_values=set)

    linter = Gio_linter()
    diagResults = linter.run(api_def_config)

    display_diag_level = {
        DiagLevel.Error: click.style('error', fg='red'),
        DiagLevel.Warn: click.style('warning', fg='yellow'),
        DiagLevel.Info: click.style('info', fg='blue'),
        DiagLevel.Hint: click.style('hint', fg='magenta')
    }

    results = []
    nb_errors = 0
    nb_warning = 0
    nb_infos = 0
    for error in diagResults:
        line_result = []
        line_result.append(display_diag_level.get(error.level))
        line_result.append(error.path)
        line_result.append(error.message)

        results.append(line_result)

        if error.level == DiagLevel.Error:
            nb_errors = nb_errors + 1
        elif error.level == DiagLevel.Warn:
            nb_warning = nb_warning + 1
        elif error.level == DiagLevel.Info:
            nb_infos = nb_infos + 1

        # click.echo()
        # print('%s %s %s' % (error.level, error.path, error.message))

    OutputFormatType.TABLE.echo(results, inner_heading_row_border=False)

    click.echo(click.style("\nSummary: errors({}), warnings({}), infos({})".format(nb_errors, nb_warning, nb_infos), fg="yellow"))
