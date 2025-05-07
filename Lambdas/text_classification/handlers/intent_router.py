import importlib


def get_handler_class(intent_name):
    try:
        module = importlib.import_module(f"handlers.{intent_name.lower()}")
        handler_class = getattr(module, f"{intent_name.capitalize()}Handler")
        return handler_class
    except (ModuleNotFoundError, AttributeError):
        from handlers.default import DefaultHandler
        return DefaultHandler
