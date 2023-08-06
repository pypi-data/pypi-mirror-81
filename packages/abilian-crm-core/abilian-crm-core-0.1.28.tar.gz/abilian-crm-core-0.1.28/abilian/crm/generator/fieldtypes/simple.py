""""""

import hashlib

import sqlalchemy as sa
import sqlalchemy.orm

from abilian.core.models.blob import Blob
from abilian.core.sqlalchemy import JSON
from abilian.core.sqlalchemy import JSONDict as _JSONDict
from abilian.core.sqlalchemy import JSONList as _JSONList

from ..definitions import MAX_IDENTIFIER_LENGTH
from .base import Field
from .registry import model_field


@model_field
class Integer(Field):
    """4 bytes: -2147483648 to +2147483647."""

    sa_type = sa.types.Integer
    default_ff_type = "IntegerField"


@model_field
class SmallInteger(Integer):
    """2 bytes: -32768 to +32767."""

    sa_type = sa.types.SmallInteger


@model_field
class BigInteger(Integer):
    """8 bytes: -9223372036854775808 to 9223372036854775807."""

    sa_type = sa.types.BigInteger


@model_field
class PositiveInteger(Integer):
    """
    :class:`Integer` restricted to positive value: 0 to +2147483647
    """

    def get_table_args(self, *args, **kwargs):
        col_name = self.name[:MAX_IDENTIFIER_LENGTH]
        name = f"check_{col_name}_positive"
        if len(name) > MAX_IDENTIFIER_LENGTH:
            digest = hashlib.md5(self.name).digest()
            exceed = len(name) - MAX_IDENTIFIER_LENGTH
            name = self.name[: MAX_IDENTIFIER_LENGTH - exceed - 7]
            name = f"check_{name}_{digest[:6]}_positive"

        yield sa.schema.CheckConstraint(sa.sql.text(col_name + " >= 0"), name=name)


@model_field
class UnicodeText(Field):
    sa_type = sa.types.UnicodeText


@model_field
class LargeBinary(Field):
    sa_type = sa.types.LargeBinary


@model_field
class Date(Field):
    sa_type = sa.types.Date
    default_ff_type = "DateField"


@model_field
class DateTime(Field):
    sa_type = sa.types.DateTime
    default_ff_type = "DateTimeField"


@model_field
class Text(Field):
    sa_type = sa.types.Text


@model_field
class Float(Field):
    sa_type = sa.types.Float
    default_ff_type = "DecimalField"


@model_field
class Boolean(Field):
    sa_type = sa.types.Boolean
    default_ff_type = "BooleanField"


@model_field
class File(Field):
    sa_type = sa.types.Integer
    default_ff_type = "FileField"
    allow_multiple = False

    def get_model_attributes(self, *args, **kwargs):
        col_name = self.name[: (MAX_IDENTIFIER_LENGTH - 3)] + "_id"
        extra_args = {"nullable": not self.required}
        extra_args["info"] = info = {}
        info["label"] = self.label

        attr = sa.schema.Column(
            col_name,
            self.sa_type(**self.sa_type_options),
            sa.ForeignKey(Blob.id),
            **extra_args,
        )

        yield col_name, attr

        relationship = sa.orm.relationship(
            Blob, primaryjoin=f"{self.model.lower()}.c.{col_name} == Blob.id",
        )
        yield self.name, relationship


@model_field
class Image(File):
    default_ff_type = "ImageField"


@model_field
class JSONField(Field):
    __fieldname__ = "JSON"
    sa_type = JSON


@model_field
class JSONListField(Field):
    __fieldname__ = "JSONList"
    sa_type = staticmethod(_JSONList)


@model_field
class JSONDict(Field):
    __fieldname__ = "JSONDict"
    sa_type = staticmethod(_JSONDict)


@model_field
class EmailAddress(UnicodeText):
    default_ff_type = "EmailField"


@model_field
class URL(UnicodeText):
    default_ff_type = "URLField"
