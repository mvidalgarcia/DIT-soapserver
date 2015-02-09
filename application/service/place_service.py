from spyne.decorator import rpc
from spyne.error import ResourceNotFoundError
from spyne.model.primitive import Mandatory
from spyne.model.complex import Iterable
from spyne.model.primitive import UnsignedInteger32
from spyne.service import ServiceBase

from application.model.db import Place
from application.model.db import Category


class PlaceManagerService(ServiceBase):
    @rpc(Mandatory.UnsignedInteger32, _returns=Place)
    def get_place(ctx, place_id):
        return ctx.udc.session.query(Place).filter_by(id=place_id).one()

    @rpc(Place, _returns=UnsignedInteger32)
    def put_place(ctx, place):
        if place.id is None:
            ctx.udc.session.add(place)
            ctx.udc.session.flush() # so that we get the place.id value

        else:
            if ctx.udc.session.query(Place).get(place.id) is None:
                # this is to prevent the client from setting the primary key
                # of a new object instead of the database's own primary-key
                # generator.
                # Instead of raising an exception, you can also choose to
                # ignore the primary key set by the client by silently doing
                # place.id = None
                raise ResourceNotFoundError('place.id=%d' % place.id)

            else:
                ctx.udc.session.merge(place)

        return place.id

    @rpc(Mandatory.UnsignedInteger32)
    def del_place(ctx, place_id):
        count = ctx.udc.session.query(Place).filter_by(id=place_id).count()
        if count == 0:
            raise ResourceNotFoundError(place_id)

        ctx.udc.session.query(Place).filter_by(id=place_id).delete()

    @rpc(_returns=Iterable(Place))
    def get_all_place(ctx):
        return ctx.udc.session.query(Place)

    @rpc(Mandatory.Unicode, _returns=Iterable(Place))
    def get_place_by_category(ctx, category_name):
        id = ctx.udc.session.query(Category.id).filter_by(name=category_name).one()
        return ctx.udc.session.query(Place).filter_by(category_id=id[0])