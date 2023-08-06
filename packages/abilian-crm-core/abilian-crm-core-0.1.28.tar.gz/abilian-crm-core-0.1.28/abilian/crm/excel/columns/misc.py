""""""

from openpyxl.cell.cell import NUMERIC_TYPES, STRING_TYPES
from six import text_type

from .base import Column

__all__ = ("EmptyColumn", "TextIntegerColumn")


class EmptyColumn(Column):
    """Useful when an export needs a blank column."""

    importable = False

    def __init__(self, label=""):
        super().__init__("", label=label, type_=None)

    def data(self, item):
        yield None, None


class TextIntegerColumn(Column):
    """Column for text that may be entered as integer, like a zipcode."""

    expected_cell_types = STRING_TYPES
    adapt_cell_types = NUMERIC_TYPES

    def _adapt_from_cell(self, value, cell_type, workbook):
        if isinstance(value, float):
            value = str(int(value))
        return value, value
