import filecmp
from pyavd.tools.multiprocess_runners import run_eos_cli_config_gen

common_struct_cfgfile = ["./vendor/tests/eos_cli_config_gen/all.yml"]
struct_cfgfiles = "./vendor/tests/eos_cli_config_gen/vars/*"
cfgfiles = "./vendor/tests/eos_cli_config_gen/configs"
docfiles = None

def test_eos_cli_config_gen():
    run_eos_cli_config_gen(common_struct_cfgfile, struct_cfgfiles, cfgfiles, docfiles)
    generated_config = "./vendor/tests/eos_cli_config_gen/configs"
    expected_config = "./vendor/tests/eos_cli_config_gen/expected_configs"
    result = filecmp.dircmp(generated_config, expected_config)
    assert not result.diff_files
