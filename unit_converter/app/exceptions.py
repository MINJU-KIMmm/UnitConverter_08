"""User-facing validation errors (app layer)."""


class UnitConverterError(Exception):
    """Base for CLI-visible conversion errors."""


class InvalidInputError(UnitConverterError, ValueError):
    """FR-05: malformed unit:value input."""


class NegativeValueError(UnitConverterError, ValueError):
    """FR-04: negative numeric input."""


class UnknownUnitError(UnitConverterError, ValueError):
    """FR-03: unit not registered in registry."""
