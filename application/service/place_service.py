import logging
logging.basicConfig(level=logging.DEBUG)
logging.getLogger('spyne.protocol.xml').setLevel(logging.DEBUG)
logging.getLogger('sqlalchemy.engine.base.Engine').setLevel(logging.DEBUG)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound

from spyne.application import Application
from spyne.decorator import rpc
from spyne.error import ResourceNotFoundError
from spyne.protocol.soap import Soap11
from spyne.model.primitive import Mandatory
from spyne.model.primitive import Unicode
from spyne.error import InternalError
from spyne.model.fault import Fault
from spyne.model.complex import Array
from spyne.model.complex import Iterable
from spyne.model.primitive import UnsignedInteger32
from spyne.server.wsgi import WsgiApplication
from spyne.service import ServiceBase


db = create_engine('sqlite:////tmp/test.db')
Session = sessionmaker(bind=db)

from application.model.place import Place, TableModel

class PlaceManagerService(ServiceBase):
    @rpc(_returns=Iterable(Place))
    def get_all_place(ctx):
        return ctx.udc.session.query(Place)