__author__ = 'Marco Vidal Garcia'

from application.service.category_service import *
#from application.service.place_service import *

from application.application import *


if __name__=='__main__':
    from wsgiref.simple_server import make_server

    application = MyApplication([CategoryManagerService],
                'server_places',
                in_protocol=Soap11(validator='lxml'),
                out_protocol=Soap11(),
            )

    wsgi_app = WsgiApplication(application)
    server = make_server('127.0.0.1', 8000, wsgi_app)

    TableModel.Attributes.sqla_metadata.create_all()
    logging.info("listening to http://127.0.0.1:8000")
    logging.info("wsdl is at: http://localhost:8000/?wsdl")

    server.serve_forever()