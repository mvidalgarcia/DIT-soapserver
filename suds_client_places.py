from suds import TypeNotFound
from suds.client import Client

has_permissions = True
c = Client('http://localhost:8000?wsdl')
'''
category1 = c.factory.create("Category")
category1.name = 'Hangouts'
category2 = c.factory.create("Category")
category2.name = 'Leisure'
category3 = c.factory.create("Category")
category3.name = 'Personal care'
category4 = c.factory.create("Category")
category4.name = 'Religion'
category5 = c.factory.create("Category")
category5.name = 'Shopping'

print(category1)

retval = c.service.put_category(category1)
retval = c.service.put_category(category2)
retval = c.service.put_category(category3)
retval = c.service.put_category(category4)
retval = c.service.put_category(category5)
print(retval)
'''
#print(c.service.get_category(retval))
print(c.service.get_all_category())
#print(c.service.del_user(2))