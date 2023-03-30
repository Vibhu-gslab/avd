from pathlib import Path

from jinja2 import Environment, FileSystemBytecodeCache, FileSystemLoader, StrictUndefined

from .vendor.j2.filter.convert_dicts import convert_dicts
from .vendor.j2.filter.default import default
from .vendor.j2.filter.list_compress import list_compress
from .vendor.j2.filter.natural_sort import natural_sort
from .vendor.j2.filter.password import decrypt, encrypt
from .vendor.j2.filter.range_expand import range_expand
from .vendor.j2.test.contains import contains
from .vendor.j2.test.defined import defined

JINJA2_EXTENSIONS = ["jinja2.ext.loopcontrols", "jinja2.ext.do", "jinja2.ext.i18n"]
JINJA2_CUSTOM_FILTERS = {
    "arista.avd.default": default,
    "arista.avd.convert_dicts": convert_dicts,
    "arista.avd.decrypt": decrypt,
    "arista.avd.encrypt": encrypt,
    "arista.avd.list_compress": list_compress,
    "arista.avd.natural_sort": natural_sort,
    "arista.avd.range_expand": range_expand,
}
JINJA2_CUSTOM_TESTS = {
    "arista.avd.defined": defined,
    "arista.avd.contains": contains,
}
JINJA2_CACHE_PATH = Path(__file__).parent.joinpath("j2cache")


class Undefined(StrictUndefined):
    """
    Allow nested checks for undefined instead of having to check on every level.
    Example "{% if var.key.subkey is arista.avd.undefined %}" is ok.

    Without this it we would have to test every level, like
    "{% if var is arista.avd.undefined or var.key is arista.avd.undefined or var.key.subkey is arista.avd.undefined %}"

    Inspired from Ansible's AnsibleUndefined class.
    """

    def __getattr__(self, name):
        # Return original Undefined object to preserve the first failure context
        return self

    def __getitem__(self, key):
        # Return original Undefined object to preserve the first failure context
        return self

    def __repr__(self):
        return f"Undefined(hint={self._undefined_hint}, obj={self._undefined_obj}, name={self._undefined_name})"

    def __contains__(self, item):
        # Return original Undefined object to preserve the first failure context
        return self


class Templar:
    def __init__(self, searchpaths: list[str], cache=True):
        self.loader = FileSystemLoader(searchpaths)
        if cache:
            self.bytecode_cache = FileSystemBytecodeCache(JINJA2_CACHE_PATH)
        else:
            self.bytecode_cache = None

        self.environment = Environment(
            extensions=JINJA2_EXTENSIONS,
            loader=self.loader,
            undefined=Undefined,
            trim_blocks=True,
            bytecode_cache=self.bytecode_cache,
        )
        self.environment.filters.update(JINJA2_CUSTOM_FILTERS)
        self.environment.tests.update(JINJA2_CUSTOM_TESTS)

    def render_template_from_file(self, template_file: str, template_vars: dict):
        return self.environment.get_template(template_file).render(template_vars)
