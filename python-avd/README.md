# pyavd

## Copy files from ansible-avd and patch as needed

`make dep`

## Test eos_cli_config_gen with molecule data

`make test-0`

## Test eos_designs_facts with molecule data

`make test-1`

## Test eos_designs structured_config with molecule data + facts from test-1

`make test-2`

## Test eos_cli_config_gen with structured_configs from test-2

`make test-3`
