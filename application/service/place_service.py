from spyne.decorator import rpc
from spyne.error import ResourceNotFoundError
from spyne.error import ValidationError
from spyne.model.primitive import Mandatory, Decimal, UnsignedInteger32, Boolean, Unicode
from spyne.model.complex import Iterable
from spyne.model.binary import File
from spyne.service import ServiceBase
from haversine import haversine

from application.model.db import Place
from sqlalchemy import asc
from sqlalchemy import and_

import datetime  # to get timestamp
import socket  # to get my own ip
import unicodedata
import os
import base64

import logging
logger = logging.getLogger(__name__)


class PlaceManagerService(ServiceBase):
    @rpc(Mandatory.UnsignedInteger32, _returns=Place)
    def get_place(ctx, place_id):
        return ctx.udc.session.query(Place).filter_by(id=place_id).one()

    @rpc(Place, _returns=UnsignedInteger32)
    def put_place(ctx, place):
        if place.id is None:
            ctx.udc.session.add(place)
            ctx.udc.session.flush()  # so that we get the place.id value

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
    def get_all_places(ctx):
        return ctx.udc.session.query(Place)

    @rpc(Mandatory.UnsignedInteger32, UnsignedInteger32, UnsignedInteger32, _returns=Iterable(Place))
    def get_places_by_category_id(ctx, category_id, from_id=0, elements=None):
        places = ctx.udc.session.query(Place).filter_by(category_id=category_id)
        if from_id is not None:
            places = [place for place in places if place.id >= from_id]
            for place in places:
               place.rating = -1.0 if place.rating == 0.0 else place.rating    
        return _partition_places(places, elements)

    @rpc(Mandatory.UnsignedInteger32, Decimal, Decimal, Decimal, UnsignedInteger32, UnsignedInteger32, _returns=Iterable(Place))
    def get_near_places_by_category_id(ctx, category_id, lat, lng, radius, from_id=0, elements=None):
        places = ctx.udc.session.query(Place).filter_by(category_id=category_id)
        places = places.order_by(asc(Place.id))
        if from_id is not None:
            places = [place for place in places if place.id >= from_id]
        # Filter just near places
        places = [place for place in places if _are_points_closed(place.lat, place.lng, lat, lng, radius)]
        # Just places id greater than from_id
        return _partition_places(places, elements)

    @rpc(Mandatory.Unicode, _returns=Boolean)
    def gplaces_id_exists_in_category(ctx, gplaces_id, category_id):
        return ctx.udc.session.query(Place).filter_by(category_id=category_id, gplaces_id=gplaces_id).count() > 0

    @rpc(Unicode, File(min_occurs=1, nullable=False), _returns=Unicode)
    def upload_image(ctx, image_name, image_file):
        image_name = image_name.replace(' ', '_')+'_'+datetime.datetime.now().strftime("%d-%m-%y_%H.%m")+'.jpg'
        path = os.path.join(os.path.abspath('/srv/images'), image_name)
        if not path.startswith(os.path.abspath('/srv/images')):
            raise ValidationError(image_file)
        f = open(path, 'wb')
        try:
            for data in image_file.data:
                f.write(base64.b64decode(data))
            logger.debug("File written: %r" % image_name)
            f.close()
        except:
            f.close()
            os.remove(image_name)
            logger.debug("File removed: %r" % image_name)
            raise # again, the client will see an internal error.
        # Watch out the port!
        url = 'http://'+socket.gethostbyname(socket.gethostname())+':8080/images/'+image_name
        return url


# Aux functions

def _partition_places(places, elements):
    return places if elements is None else [place for place in places[0:int(elements)]]


# Radius in KM
def _are_points_closed(lat1, lng1, lat2, lng2, radius):
    if lat1 is None or lng1 is None or lat2 is None or lng2 is None or radius is None:
        return True
    else:
        return haversine((float(lat1), float(lng1)), (float(lat2), float(lng2))) <= float(radius)


def strip_accents(s):
    return ''.join(char for char in unicodedata.normalize('NFD', s) if unicodedata.category(char) != 'Mn')
