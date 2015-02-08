from sqlalchemy import MetaData
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from spyne.model.complex import ComplexModelBase
from spyne.model.complex import ComplexModelMeta
from spyne.model.primitive import UnsignedInteger32
from spyne.model.primitive import Unicode


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