""""""

from flask import current_app
from openpyxl.cell.cell import STRING_TYPES
from six import text_type

from .base import Column

__all__ = ("TagsColumn",)


class TagsColumn(Column):
    """Columns for :class:`abilian.core.models.tags.Tag` items."""

    expected_cell_types = STRING_TYPES

    def data(self, item):
        ext = current_app.extensions.get("tags")
        if not ext or not ext.is_support_tagging(item):
            yield None, None

        value = sorted(ext.entity_tags(item))
        import_value = "; ".join(str(t) for t in value) if value else ""
        yield import_value, value

    def deserialize(self, value):
        # type_ has already 'deserialized' value
        return value
