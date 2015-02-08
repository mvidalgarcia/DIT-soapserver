__author__ = 'Marco Vidal Garcia'
from sqlalchemy import MetaData
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from spyne.model.complex import ComplexModelBase
from spyne.model.complex import ComplexModelMeta
from spyne.model.primitive import UnsignedInteger32
from spyne.model.primitive import Unicode
from spyne.model.primitive import Decimal

db = create_engine('sqlite:////tmp/test.db')
Session = sessionmaker(bind=db)

# This is what calling TTableModel does. This is here for academic purposes.
class TableModel(ComplexModelBase):
    __metaclass__ = ComplexModelMeta
    __metadata__ = MetaData(bind=db)

class Place(TableModel):
    __tablename__ = 'place'
    __namespace__ = 'server_places'
    __table_args__ = {"sqlite_autoincrement": True}

    id = UnsignedInteger32(pk=True)
    name = Unicode()
    description = Unicode()
    lat = Decimal()
    lng = Decimal()
    address = Unicode()
    image = Unicode()
    category_id = UnsignedInteger32(fk='category.id')