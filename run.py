__author__ = 'Marco Vidal Garcia'

import logging
logging.basicConfig(level=logging.DEBUG)
logging.getLogger('spyne.protocol.xml').setLevel(logging.DEBUG)
logging.getLogger('sqlalchemy.engine.base.Engine').setLevel(logging.DEBUG)
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication

from application.service.category_service import CategoryManagerService
from application.service.place_service import PlaceManagerService

from application.model.db import TableModel
from application.app import MyApplication


if __name__ == '__main__':
    from wsgiref.simple_server import make_server

    application = MyApplication([CategoryManagerService, PlaceManagerService],
                'server_places',
                in_protocol=Soap11(validator='lxml'),
                out_protocol=Soap11(),
            )

    wsgi_app = WsgiApplication(application)
    server = make_server('0.0.0.0', 8888, wsgi_app)

    TableModel.Attributes.sqla_metadata.create_all()
    logging.info("listening to http://156.35.95.75:8888")
    logging.info("wsdl is at: http://156.35.95.75:8888/?wsdl")

    server.serve_forever()
