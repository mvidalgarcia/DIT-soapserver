__author__ = 'Marco Vidal Garcia'

from suds.client import Client

has_permissions = True
c = Client('http://156.35.95.75:8888?wsdl')

#----------------------- #
# ----- CATEGORIES ----- #
#----------------------- #

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
#all_categories = c.service.get_all_category()
#print(all_categories[0][0].name)


#----------------------- #
# ------- PLACES ------- #
#----------------------- #

'''
place1 = c.factory.create("Place")
place1.name = 'McDonalds Restaurant'
place1.description = 'Fast food restaurant especialised in burgers, fries and resfreshments.'
place1.lat = 43.37105
place1.lng = -5.831441
place1.address = 'Centro Comercial Los Prados, Calle Fernandez Ladreda, s/n 33011 Oviedo, Asturias'
place1.image = 'http://www.centrocomerciallosprados.com/web/img/locales/26.JPG'
place1.category_id = 1
place1.id = 2

retval = c.service.put_place(place1)
print(retval)
'''
#c.service.del_place(1)
print(c.service.get_all_place())
#print(c.service.get_place_by_category('Eating'))
