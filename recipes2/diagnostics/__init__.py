import importlib
import pkgutil

# dynamically collect all modules in this package
modules = {}
for loader, module_name, is_pkg in pkgutil.iter_modules(__path__):
    module = importlib.import_module(f".{module_name}", package=__name__)
    modules[module_name] = module

def run_all():
    results = {}
    for module in modules.values():
        results.update(module.run())
    return results