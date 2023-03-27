from pathlib import Path

pyavd_dir = Path(__file__).parents[2]
DEFAULT_SCHEMAS = {
    "avd_meta_schema": pyavd_dir.joinpath("vendor", "schema", "avd_meta_schema.json"),
    "eos_cli_config_gen": pyavd_dir.joinpath("vendor", "schemas", "eos_cli_config_gen.schema.yml"),
    "eos_designs": pyavd_dir.joinpath("vendor", "schemas", "eos_designs.schema.yml"),
}
