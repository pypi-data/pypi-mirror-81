""""""

import sqlalchemy as sa
import sqlalchemy.ext
import sqlalchemy.orm

import abilian.web.forms.fields as awbff
import abilian.web.forms.widgets as aw_widgets

from ...forms import PostalAddressField, PostalAddressForm
from ...models import PostalAddress
from .base import Field, FormField
from .registry import form_field, model_field


@model_field
class _PostalAddressField(Field):
    __fieldname__ = "PostalAddress"
    sa_type = sa.Integer
    default_ff_type = "PostalAddressFormField"
    allow_multiple = True

    def get_model_attributes(self, *args, **kwargs):
        # column declared_attr
        col_name = self.name + "_id"

        if self.multiple:
            yield self.gen_m2m(*args, **kwargs)
            raise StopIteration

        def gen_column(cls):
            fk_kw = dict(
                name=f"{cls.__name__.lower()}_{col_name}_fkey",
                use_alter=True,
                ondelete="SET NULL",
            )
            target_col = str(PostalAddress.id.parent.c.id)
            fk = sa.ForeignKey(target_col, **fk_kw)
            return sa.Column(col_name, sa.types.Integer(), fk)

        gen_column.func_name = col_name
        yield col_name, sa.ext.declarative.declared_attr(gen_column)

        # relationship declared_attr
        def gen_relationship(cls):
            kw = dict(uselist=False)
            local = cls.__name__ + "." + col_name
            remote = str(PostalAddress.id)
            kw["primaryjoin"] = f"{local} == {remote}"
            return sa.orm.relationship(PostalAddress, **kw)

        gen_relationship.func_name = self.name
        yield self.name, sa.ext.declarative.declared_attr(gen_relationship)

    def gen_m2m(self, *args, **kwargs):
        model_name = self.model

        def gen_relationship(cls):
            src_name = cls.__tablename__
            local_src_col = model_name.lower() + "_id"
            local_target_col = "postaladdress_id"
            tbl_name = src_name + "_" + self.name
            secondary_table = sa.Table(
                tbl_name,
                cls.metadata,
                sa.Column(local_src_col, sa.ForeignKey(cls.id)),
                sa.Column(local_target_col, sa.ForeignKey(PostalAddress.id)),
                sa.schema.UniqueConstraint(local_src_col, local_target_col),
            )

            rel_kw = dict(secondary=secondary_table)
            return sa.orm.relationship(PostalAddress, **rel_kw)

        gen_relationship.func_name = self.name
        return self.name, sa.ext.declarative.declared_attr(gen_relationship)


@form_field
class PostalAddressFormField(FormField):
    ff_type = PostalAddressField

    def get_type(self, *args, **kwargs):
        return awbff.ModelFieldList if self.multiple else self.ff_type

    def get_extra_args(self, *args, **kwargs):
        extra_args = super().get_extra_args(*args, **kwargs)
        if self.multiple:
            extra_args["unbound_field"] = awbff.ModelFormField(PostalAddressForm)
            extra_args["min_entries"] = 1
            extra_args["population_strategy"] = "update"
            extra_args["widget"] = aw_widgets.TabularFieldListWidget(
                template="widgets/model_fieldlist.html"
            )

        return extra_args
