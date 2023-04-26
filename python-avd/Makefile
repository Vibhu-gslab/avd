CURRENT_DIR = $(shell pwd)
PACKAGE_DIR = pyavd
ANSIBLE_AVD_DIR ?= ..
VENDOR = vendor
VENDOR_DIR = $(PACKAGE_DIR)/$(VENDOR)
VENDOR_IMPORT = $(PACKAGE_DIR).$(VENDOR)
J2_DIR = $(VENDOR_DIR)/j2
TESTS_ARTIFACTS = $(VENDOR_DIR)/tests
TOOLS_DIR = $(PACKAGE_DIR)/tools
EOS_CLI_CONFIG_GEN_TEMPLATE_DIR = $(VENDOR_DIR)/templates
SCHEMAS_DIR = $(VENDOR_DIR)/schemas
EOS_DESIGNS_MODULES_DIR = $(VENDOR_DIR)/eos_designs

.PHONY: help
help: ## Display help message
	@grep -E '^[0-9a-zA-Z_-]+\.*[0-9a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: dep
dep: copy-libs fix-libs copy-test-data ## Copy and Fix Ansible AVD python files

.PHONY: clean
	rm -rf $(VENDOR_DIR)
	rm -rf $(SCHEMAS_DIR)

.PHONY: copy-libs
copy-libs: ## Copy files from Ansible AVD collection
	rm -rf $(VENDOR_DIR)
	mkdir -p $(VENDOR_DIR)
	mkdir -p $(J2_DIR)
	mkdir -p $(SCHEMAS_DIR)
	mkdir -p $(EOS_CLI_CONFIG_GEN_TEMPLATE_DIR)
	mkdir -p $(EOS_DESIGNS_MODULES_DIR)

	cp -r $(ANSIBLE_AVD_DIR)/ansible_collections/arista/avd/plugins/plugin_utils/* $(VENDOR_DIR)
	cp -r $(ANSIBLE_AVD_DIR)/ansible_collections/arista/avd/plugins/module_utils/* $(VENDOR_DIR)
	cp -r $(ANSIBLE_AVD_DIR)/ansible_collections/arista/avd/plugins/filter $(J2_DIR)
	cp -r $(ANSIBLE_AVD_DIR)/ansible_collections/arista/avd/plugins/test $(J2_DIR)
	cp -r $(ANSIBLE_AVD_DIR)/ansible_collections/arista/avd/roles/eos_cli_config_gen/templates/* $(EOS_CLI_CONFIG_GEN_TEMPLATE_DIR)
	cp $(ANSIBLE_AVD_DIR)/ansible_collections/arista/avd/roles/eos_cli_config_gen/schemas/eos_cli_config_gen.schema.yml $(SCHEMAS_DIR)/
	rm -f $(EOS_CLI_CONFIG_GEN_TEMPLATE_DIR)/avd_schema_documentation.j2

	cp -r $(ANSIBLE_AVD_DIR)/ansible_collections/arista/avd/roles/eos_designs/python_modules/* $(EOS_DESIGNS_MODULES_DIR)/
	mv $(VENDOR_DIR)/eos_designs_* $(EOS_DESIGNS_MODULES_DIR)/
	cp -r $(ANSIBLE_AVD_DIR)/ansible_collections/arista/avd/roles/eos_designs/schemas/eos_designs.schema.yml $(SCHEMAS_DIR)/

.PHONY: fix-libs
fix-libs: ## Fix/remove various Ansible specifics things from python files
	rm -f $(VENDOR_DIR)/schema/avdschematools.py
	find $(PACKAGE_DIR) -name '__pycache__' -exec rm -rf {} +
	find $(PACKAGE_DIR) -name '*.py' -exec sed -i 's/^from __future__ import.*/from __future__ import annotations/g' {} +
	find $(PACKAGE_DIR) -name '*.py' -exec sed -i '/^__metaclass__ = type/d' {} +
	find $(PACKAGE_DIR) -name '*.py' -exec sed -i 's/from ansible.errors import /from $(VENDOR_IMPORT).errors import /g' {} +
	find $(PACKAGE_DIR) -name '*.py' -exec sed -i 's/AnsibleFilterError/AristaAvdError/g' {} +
	find $(PACKAGE_DIR) -name '*.py' -exec sed -i 's/AnsibleError/AristaAvdError/g' {} +
	find $(PACKAGE_DIR) -name '*.py' -exec sed -i 's/AnsibleActionFail/AristaAvdError/g' {} +
	find $(PACKAGE_DIR) -name '*.py' -exec sed -i 's/ansible_collections\.arista\.avd\.plugins\.plugin_utils\.eos_designs_shared_utils/$(VENDOR_IMPORT)\.eos_designs\.eos_designs_shared_utils/g' {} +
	find $(PACKAGE_DIR) -name '*.py' -exec sed -i 's/ansible_collections\.arista\.avd\.plugins\.plugin_utils/$(VENDOR_IMPORT)/g' {} +
	find $(PACKAGE_DIR) -name '*.py' -exec sed -i 's/ansible_collections\.arista\.avd\.plugins\.module_utils/$(VENDOR_IMPORT)/g' {} +
	find $(PACKAGE_DIR) -name '*.py' -exec sed -i 's/ansible_collections\.arista\.avd\.plugins\.filter/$(VENDOR_IMPORT)\.j2\.filter/g' {} +
	find $(PACKAGE_DIR) -name '*.py' -exec sed -i 's/ansible_collections\.arista\.avd\.roles\.eos_designs\.python_modules/$(VENDOR_IMPORT)\.eos_designs/g' {} +
	find $(PACKAGE_DIR) -name '*.py' -exec sed -i 's/from ansible\.utils\.display/from $(VENDOR_IMPORT)\.utils\.display/g' {} +
	grep 'version:' $(ANSIBLE_AVD_DIR)/ansible_collections/arista/avd/galaxy.yml | sed -e 's/version: \(.\+\)/VERSION = "\1"/' > $(PACKAGE_DIR)/version.py

	cp -r $(CURRENT_DIR)/vendor_overrides/* $(VENDOR_DIR)/

	$(CURRENT_DIR)/compile_templates.py

.PHONY: copy-test-data
copy-test-data: ## Copy inventory files from AVD collection Molecule scenario.
	rm -rf $(TESTS_ARTIFACTS)

	mkdir -p $(TESTS_ARTIFACTS)/eos_cli_config_gen/vars
	mkdir -p $(TESTS_ARTIFACTS)/eos_cli_config_gen/expected_configs
	mkdir -p $(TESTS_ARTIFACTS)/eos_cli_config_gen/configs
	mkdir -p $(TESTS_ARTIFACTS)/eos_designs/vars
	mkdir -p $(TESTS_ARTIFACTS)/eos_designs/facts
	mkdir -p $(TESTS_ARTIFACTS)/eos_designs/expected_structured_configs
	mkdir -p $(TESTS_ARTIFACTS)/eos_designs/structured_configs
	mkdir -p $(TESTS_ARTIFACTS)/eos_designs/expected_configs
	mkdir -p $(TESTS_ARTIFACTS)/eos_designs/configs


## eos_cli_config_gen
	cp $(ANSIBLE_AVD_DIR)/ansible_collections/arista/avd/molecule/eos_cli_config_gen/inventory/group_vars/all.yml $(TESTS_ARTIFACTS)/eos_cli_config_gen/
	cp $(ANSIBLE_AVD_DIR)/ansible_collections/arista/avd/molecule/eos_cli_config_gen/inventory/host_vars/* $(TESTS_ARTIFACTS)/eos_cli_config_gen/vars/
	cp $(ANSIBLE_AVD_DIR)/ansible_collections/arista/avd/molecule/eos_cli_config_gen/intended/configs/* $(TESTS_ARTIFACTS)/eos_cli_config_gen/expected_configs/
## Remove tests with inline jinja or custom templates
	rm $(TESTS_ARTIFACTS)/eos_cli_config_gen/vars/custom-templates.yml
	rm $(TESTS_ARTIFACTS)/eos_cli_config_gen/expected_configs/custom-templates.cfg
	rm $(TESTS_ARTIFACTS)/eos_cli_config_gen/vars/tcam-profile.yml
	rm $(TESTS_ARTIFACTS)/eos_cli_config_gen/expected_configs/tcam-profile.cfg
## Remove blank line in empty template result (some weird ansible behavior)
	echo -n '' > $(TESTS_ARTIFACTS)/eos_cli_config_gen/expected_configs/generate-default-config.cfg
	find $(TESTS_ARTIFACTS)/eos_cli_config_gen/ -name '*.yml' -exec sed -i 's/!unsafe //g' {} +

## eos_designs
	cp $(ANSIBLE_AVD_DIR)/ansible_collections/arista/avd/roles/eos_designs/defaults/main/*.yml $(TESTS_ARTIFACTS)/eos_designs/
	cp $(ANSIBLE_AVD_DIR)/ansible_collections/arista/avd/molecule/eos_designs_unit_tests/intended/structured_configs/*.yml $(TESTS_ARTIFACTS)/eos_designs/expected_structured_configs/
	cp $(ANSIBLE_AVD_DIR)/ansible_collections/arista/avd/molecule/eos_designs_unit_tests/intended/configs/*.cfg $(TESTS_ARTIFACTS)/eos_designs/expected_configs/

## Remove tests with custom templates
	rm $(TESTS_ARTIFACTS)/eos_designs/expected_structured_configs/CUSTOM-TEMPLATES*.yml
	rm $(TESTS_ARTIFACTS)/eos_designs/expected_configs/CUSTOM-TEMPLATES*.cfg
	rm $(TESTS_ARTIFACTS)/eos_designs/expected_structured_configs/CUSTOM-PYTHON_MODULES*.yml
	rm $(TESTS_ARTIFACTS)/eos_designs/expected_configs/CUSTOM-PYTHON_MODULES*.cfg

## Vendor Overrides
	cp -r $(CURRENT_DIR)/vendor_overrides/tests/* $(VENDOR_DIR)/tests/

## Run ansible-inventory to get all group-vars and inherited variables per host
	for FILE in `ls -1 $(TESTS_ARTIFACTS)/eos_designs/expected_structured_configs/*.yml` ; \
	do \
	basename $${FILE}; \
	ansible-inventory -i $(ANSIBLE_AVD_DIR)/ansible_collections/arista/avd/molecule/eos_designs_unit_tests/inventory/hosts.yml \
	--host "`basename $${FILE%.yml}`" > $(TESTS_ARTIFACTS)/eos_designs/vars/`basename $${FILE%.yml}.json`; \
	done

## Update test vars for default vars.
#	sed -i -e 's/{{ inventory_dir }}/$(PACKAGE_DIR)\/tests\/eos_designs/g' $(TESTS_ARTIFACTS)/eos_designs/main.yml

#	$(CURRENT_DIR)/runner.py --template_vars \
#	    --device_varfiles '$(TESTS_ARTIFACTS)/eos_designs/*.yml' \
#	    --common_varfile $(TESTS_ARTIFACTS)/eos_designs/main.yml \
#	    --common_varfile $(TESTS_ARTIFACTS)/eos_designs/default-templates.yml \
#		--common_varfile $(TESTS_ARTIFACTS)/eos_designs/pyavd_test_vars.yml

#	sed -i -e "s/\"\(\[.*\]\)\"/\1/g" $(TESTS_ARTIFACTS)/eos_designs/main.yml
#	sed -i -e "s/\"\({.*}\)\"/\1/g" $(TESTS_ARTIFACTS)/eos_designs/main.yml
#	sed -i 's/ansible_collections\.arista\.avd\.roles\.eos_designs\.python_modules/$(VENDOR_IMPORT)\.eos_designs/g' $(TESTS_ARTIFACTS)/eos_designs/main.yml

## Template var files since we do not support templating of vars at runtime.
	$(CURRENT_DIR)/runner.py --template_vars \
	    --device_varfiles '$(TESTS_ARTIFACTS)/eos_designs/vars/*' \
		--common_varfile $(TESTS_ARTIFACTS)/eos_designs/pyavd_test_vars.yml

## Remove quotes from templated lists or dicts: "[...]" -> [...] and "{...}" -> {...}
	find $(TESTS_ARTIFACTS)/eos_designs/vars -name '*.json' -exec sed -i -e 's/"\(\[.*\]\)"/\1/g' {} +
	find $(TESTS_ARTIFACTS)/eos_designs/vars -name '*.json' -exec sed -i -e 's/"\({.*}\)"/\1/g' {} +

## Template var files since we do not support templating of vars at runtime. (not sure why this second round is needed, but it is.)
	$(CURRENT_DIR)/runner.py --template_vars \
	    --device_varfiles '$(TESTS_ARTIFACTS)/eos_designs/vars/*' \
		--common_varfile $(TESTS_ARTIFACTS)/eos_designs/pyavd_test_vars.yml

.PHONY: test-0
test-0: ## Run tests by parsing test inputs and comparing with expected configs
	$(CURRENT_DIR)/runner.py --eos_cli_config_gen \
	    -t $(TESTS_ARTIFACTS)/eos_cli_config_gen/all.yml \
	    -s '$(TESTS_ARTIFACTS)/eos_cli_config_gen/vars/*' \
	    -c $(TESTS_ARTIFACTS)/eos_cli_config_gen/configs/
	diff -q $(TESTS_ARTIFACTS)/eos_cli_config_gen/expected_configs/ $(TESTS_ARTIFACTS)/eos_cli_config_gen/configs/

.PHONY: test-3
test-3: ## Run tests by parsing test inputs and comparing with expected configs
	$(CURRENT_DIR)/runner.py --eos_cli_config_gen \
	    --struct_cfgfiles '$(TESTS_ARTIFACTS)/eos_designs/structured_configs/*' \
	    --cfgfiles $(TESTS_ARTIFACTS)/eos_designs/configs
	diff -q $(TESTS_ARTIFACTS)/eos_designs/expected_configs/ $(TESTS_ARTIFACTS)/eos_designs/configs/

.PHONY: test-2
test-2: ## Run tests by parsing test inputs and comparing with expected structured configs
	$(CURRENT_DIR)/runner.py --eos_designs_structured_configs \
	    --factsfile '$(TESTS_ARTIFACTS)/eos_designs/facts/eos_designs_facts.yml' \
	    --device_varfiles '$(TESTS_ARTIFACTS)/eos_designs/vars/*' \
		--common_varfile $(TESTS_ARTIFACTS)/eos_designs/pyavd_test_vars.yml \
		--struct_cfgfiles $(TESTS_ARTIFACTS)/eos_designs/structured_configs
	diff -q $(TESTS_ARTIFACTS)/eos_designs/expected_structured_configs/ $(TESTS_ARTIFACTS)/eos_designs/structured_configs/

.PHONY: test-1
test-1: ## Run tests by parsing test inputs and comparing with expected configs
	$(CURRENT_DIR)/runner.py --eos_designs_facts \
	    --factsfile '$(TESTS_ARTIFACTS)/eos_designs/facts/eos_designs_facts.yml' \
	    --device_varfiles '$(TESTS_ARTIFACTS)/eos_designs/vars/*' \
		--common_varfile $(TESTS_ARTIFACTS)/eos_designs/pyavd_test_vars.yml

.PHONE: test
test: test-1 test-3
