__author__ = 'Marco Vidal Garcia'

from spyne.model.primitive import UnsignedInteger32
from spyne.model.primitive import Unicode
from spyne.model.complex import TTableModel
from spyne.model.primitive import Decimal

from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy.orm import sessionmaker

db = create_engine('sqlite:////tmp/test.db')
Session = sessionmaker(bind=db)

TableModel = TTableModel(MetaData(bind=db))


# Model Category
class Category(TableModel):
    __tablename__ = 'category'
    __namespace__ = 'server_places'
    __table_args__ = {"sqlite_autoincrement": True}

    id = UnsignedInteger32(pk=True)
    name = Unicode()


# Model Place
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