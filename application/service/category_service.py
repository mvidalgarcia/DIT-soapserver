from spyne.decorator import rpc
from spyne.error import ResourceNotFoundError
from spyne.model.primitive import Mandatory
from spyne.model.complex import Iterable
from spyne.model.primitive import UnsignedInteger32
from spyne.service import ServiceBase

from application.model.db import Category


class CategoryManagerService(ServiceBase):
    @rpc(Mandatory.UnsignedInteger32, _returns=Category)
    def get_category(ctx, category_id):
        return ctx.udc.session.query(Category).filter_by(id=category_id).one()

    @rpc(Category, _returns=UnsignedInteger32)
    def put_category(ctx, category):
        if category.id is None:
            ctx.udc.session.add(category)
            ctx.udc.session.flush() # so that we get the category.id value

        else:
            if ctx.udc.session.query(Category).get(category.id) is None:
                # this is to prevent the client from setting the primary key
                # of a new object instead of the database's own primary-key
                # generator.
                # Instead of raising an exception, you can also choose to
                # ignore the primary key set by the client by silently doing
                # category.id = None
                raise ResourceNotFoundError('category.id=%d' % category.id)

            else:
                ctx.udc.session.merge(category)

        return category.id

    @rpc(Mandatory.UnsignedInteger32)
    def del_category(ctx, category_id):
        count = ctx.udc.session.query(Category).filter_by(id=category_id).count()
        if count == 0:
            raise ResourceNotFoundError(category_id)

        ctx.udc.session.query(Category).filter_by(id=category_id).delete()


    @rpc(Mandatory.UnsignedInteger32)
    def del_category_by_name(ctx, category_name):
        count = ctx.udc.session.query(Category).filter_by(name=category_name).count()
        if count == 0:
            raise ResourceNotFoundError(category_name)

        ctx.udc.session.query(Category).filter_by(name=category_name).delete()


    @rpc(_returns=Iterable(Category))
    def get_all_categories(ctx):
        return ctx.udc.session.query(Category)