from collections import ChainMap

from .avd_schema_tools import AvdSchemaTools
from .vendor.avdfacts import AvdFacts
from .vendor.eos_designs.base import AvdStructuredConfig as EosDesignsBase
from .vendor.eos_designs.connected_endpoints import AvdStructuredConfig as EosDesignsConnectedEndpoints
from .vendor.eos_designs.core_interfaces import AvdStructuredConfig as EosDesignsCoreInterfaces
from .vendor.eos_designs.custom_structured_configuration import AvdStructuredConfig as EosDesignsCustomStructuredConfiguration
from .vendor.eos_designs.inband_management import AvdStructuredConfig as EosDesignsInbandManagement
from .vendor.eos_designs.l3_edge import AvdStructuredConfig as EosDesignsL3Edge
from .vendor.eos_designs.mlag import AvdStructuredConfig as EosDesignsMlag
from .vendor.eos_designs.network_services import AvdStructuredConfig as EosDesignsNetworkServices
from .vendor.eos_designs.overlay import AvdStructuredConfig as EosDesignsOverlay
from .vendor.eos_designs.underlay import AvdStructuredConfig as EosDesignsUnderlay
from .vendor.merge import merge

EOS_DESIGNS_MODULES = {
    "base": EosDesignsBase,
    "mlag": EosDesignsMlag,
    "underlay": EosDesignsUnderlay,
    "overlay": EosDesignsOverlay,
    "core_interfaces": EosDesignsCoreInterfaces,
    "l3_edge": EosDesignsL3Edge,
    "network_services": EosDesignsNetworkServices,
    "connected_endpoints": EosDesignsConnectedEndpoints,
    "inband_management": EosDesignsInbandManagement,
    "custom_structured_configuration": EosDesignsCustomStructuredConfiguration,
}

DEFAULT_CUSTOM_STRUCTURED_CONFIGURATION_LIST_MERGE = "append_rp"


def eos_designs_structured_configs(hostname: str, vars: dict, modules: list[str] | None = None) -> dict:
    """
    Main function for eos_designs_structured_configs to render structured configs for one device.

    Is used by run_eos_designs_structured_configs_process worker function but can also be called by other frameworks.

    Parameters
    ----------
    hostname : str
        Hostname of device. Set as 'inventory_hostname' on the input vars, to keep compatability with Ansible focused code.
    vars : dict
        Dictionary of variables passed to modules. Variables are converted and validated according to AVD Schema first.
    modules : list[str] | None
        List of eos_designs python modules to run. Must be one of the supported modules set in constant EOS_DESIGNS_MODULES.
        If not set, the full list of modules will be run.
    verbosity: int
        Vebosity level for output. Passed along to other functions

    Returns
    -------
    dict
        Device structured configuration rendered by the given modules
    """

    if not modules:
        modules = list(EOS_DESIGNS_MODULES)

    output_schematools = AvdSchemaTools(schema_id="eos_cli_config_gen")

    structured_config = {}
    module_vars = ChainMap(
        {"inventory_hostname": hostname},
        structured_config,
        vars,
    )

    for module in modules:
        if module not in EOS_DESIGNS_MODULES:
            raise ValueError(f"Unknown eos_designs module '{module}' during render of eos_designs_structured_config for host '{hostname}'")

        eos_designs_module: AvdFacts = EOS_DESIGNS_MODULES[module](module_vars, None)
        results = eos_designs_module.render()

        # Modules can return a dict or a list of dicts
        if not isinstance(results, list):
            results = [results]

        for result in results:
            output_schematools.convert_data(result)

        if module == "custom_structured_configuration":
            list_merge = module_vars.get("custom_structured_configuration_list_merge", DEFAULT_CUSTOM_STRUCTURED_CONFIGURATION_LIST_MERGE)
        else:
            list_merge = "append"

        merge(structured_config, *results, list_merge=list_merge, schema=output_schematools.avdschema)

    return structured_config
