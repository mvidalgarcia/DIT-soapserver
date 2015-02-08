import logging
logging.basicConfig(level=logging.DEBUG)
logging.getLogger('spyne.protocol.xml').setLevel(logging.DEBUG)
logging.getLogger('sqlalchemy.engine.base.Engine').setLevel(logging.DEBUG)

from sqlalchemy import create_engine
from sqlalchemy import MetaData
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
from spyne.model.complex import ComplexModelBase
from spyne.model.complex import ComplexModelMeta
from spyne.model.primitive import UnsignedInteger32
from spyne.server.wsgi import WsgiApplication
from spyne.service import ServiceBase


db = create_engine('sqlite:////tmp/test.db')
Session = sessionmaker(bind=db)

# This is what calling TTableModel does. This is here for academic purposes.
class TableModel(ComplexModelBase):
    __metaclass__ = ComplexModelMeta
    __metadata__ = MetaData(bind=db)


class Category(TableModel):
    __tablename__ = 'category'
    __namespace__ = 'server_places.categories'
    __table_args__ = {"sqlite_autoincrement": True}

    id = UnsignedInteger32(pk=True)
    name = Unicode()

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

    @rpc(_returns=Iterable(Category))
    def get_all_category(ctx):
        return ctx.udc.session.query(Category)


class CategoryDefinedContext(object):
    def __init__(self):
        self.session = Session()


def _on_method_call(ctx):
    ctx.udc = CategoryDefinedContext()


def _on_method_context_closed(ctx):
    if ctx.udc is not None:
        ctx.udc.session.commit()
        ctx.udc.session.close()


class MyApplication(Application):
    def __init__(self, services, tns, name=None,
                                         in_protocol=None, out_protocol=None):
        super(MyApplication, self).__init__(services, tns, name, in_protocol,
                                                                 out_protocol)

        self.event_manager.add_listener('method_call', _on_method_call)
        self.event_manager.add_listener("method_context_closed",
                                                    _on_method_context_closed)

    def call_wrapper(self, ctx):
        try:
            return ctx.service_class.call_wrapper(ctx)

        except NoResultFound:
            raise ResourceNotFoundError(ctx.in_object)

        except Fault, e:
            logging.error(e)
            raise

        except Exception, e:
            logging.exception(e)
            raise InternalError(e)


if __name__=='__main__':
    from wsgiref.simple_server import make_server

    application = MyApplication([CategoryManagerService],
                'server_places.categories',
                in_protocol=Soap11(validator='lxml'),
                out_protocol=Soap11(),
            )

    wsgi_app = WsgiApplication(application)
    server = make_server('127.0.0.1', 8000, wsgi_app)

    TableModel.Attributes.sqla_metadata.create_all()
    logging.info("listening to http://127.0.0.1:8000")
    logging.info("wsdl is at: http://localhost:8000/?wsdl")

    server.serve_forever()