from pathlib import Path

from .avd_schema_tools import AvdSchemaTools
from .templater import Templar

JINJA2_TEMPLATE_PATHS = [Path(__file__).parent.joinpath("vendor", "templates")]
JINJA2_CONFIG_TEMPLATE = "eos-intended-config.j2"
JINJA2_DOCUMENTAITON_TEMPLATE = "eos-device-documentation.j2"
SCHEMA_ID = "eos_cli_config_gen"


def update_templates():
    templar = Templar()
    templar.compile_templates_in_paths(JINJA2_TEMPLATE_PATHS)


def eos_cli_config_gen(
    hostname: str,
    template_vars: dict,
    render_configuration: bool = True,
    render_documentation: bool = False,
) -> tuple[str | None, str | None]:
    """
    Main function for eos_cli_config_gen to render configs and/or documentation for one device.

    Is used by run_eos_cli_config_gen_process worker function but can also be called by other frameworks.

    Parameters
    ----------
    hostname : str
        Hostname of device. Set as 'inventory_hostname' on the input vars, to keep compatability with Ansible focused code.
    template_vars : dict
        Dictionary of variables applied to template. Variables are converted and validated according to AVD Schema first.
    render_configuration: bool, default=True
        If true, the device configuration will be rendered and returned
    render_documentation: bool, default=False
        If true, the device documentation will be rendered and returned
    update_compiled_templates: bool, default=False
        Update Jinja2 compiled templates before running.

    Returns
    -------
    configuration : str
        Device configuration in EOS CLI format. None if render_configuration is not true.
    documentation : str
        Device documentation in markdown format. None if render_documentation is not true.
    """

    configuration = None
    documentation = None

    # All the AVD code looks for the hostname in this key.
    template_vars["inventory_hostname"] = hostname

    AvdSchemaTools(schema_id=SCHEMA_ID).convert_and_validate_data(template_vars)

    templar = Templar()

    if render_configuration:
        configuration = templar.render_template_from_file(JINJA2_CONFIG_TEMPLATE, template_vars)

    if render_documentation:
        documentation = templar.render_template_from_file(JINJA2_DOCUMENTAITON_TEMPLATE, template_vars)

    return configuration, documentation
