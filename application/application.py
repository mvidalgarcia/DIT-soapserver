from spyne.application import Application
from spyne.error import InternalError
from spyne.model.fault import Fault
from spyne.error import ResourceNotFoundError
from sqlalchemy.orm.exc import NoResultFound

from category_service import Session

# Context
class DefinedContext(object):
    def __init__(self):
        self.session = Session()

# Application
def _on_method_call(ctx):
    ctx.udc = DefinedContext()


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