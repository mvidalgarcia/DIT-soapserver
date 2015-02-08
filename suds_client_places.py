from suds import TypeNotFound
from suds.client import Client

has_permissions = True
c = Client('http://localhost:8000?wsdl')
'''
category1 = c.factory.create("Category")
category1.name = 'Eating'
category2 = c.factory.create("Category")
category2.name = 'Hangouts'
category3 = c.factory.create("Category")
category3.name = 'Leisure'
category4 = c.factory.create("Category")
category4.name = 'Personal care'
category5 = c.factory.create("Category")
category5.name = 'Religion'
category6 = c.factory.create("Category")
category6.name = 'Shopping'


retval = c.service.put_category(category1)
retval = c.service.put_category(category2)
retval = c.service.put_category(category3)
retval = c.service.put_category(category4)
retval = c.service.put_category(category5)
retval = c.service.put_category(category6)
print(retval)
'''
#print(c.service.get_category(1))

print(c.service.get_all_category())