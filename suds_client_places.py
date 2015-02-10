__author__ = 'Marco Vidal Garcia'

from suds.client import Client

has_permissions = True
c = Client('http://156.35.95.75:8888?wsdl')

#----------------------- #
# ----- CATEGORIES ----- #
#----------------------- #


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
#print(retval)

#print(c.service.get_category(1))

print(c.service.get_all_category())
#all_categories = c.service.get_all_category()
#print(all_categories[0][0].name)


#----------------------- #
# ------- PLACES ------- #
#----------------------- #
'''
# Eating

place0 = c.factory.create("Place")
place0.name = 'McDonalds Restaurant'
place0.description = 'Fast food restaurant especialised in burgers, fries and resfreshments.'
place0.lat = 43.37105
place0.lng = -5.831441
place0.address = 'Centro Comercial Los Prados, Calle Fernandez Ladreda, s/n 33011 Oviedo, Asturias'
place0.image = 'http://www.centrocomerciallosprados.com/web/img/locales/26.JPG'
place0.category_id = 1

place1 = c.factory.create("Place")
place1.name = 'Pizza Móvil'
place1.description = ''
place1.lat = 43.370604
place1.lng = -5.840382
place1.address = 'Calle Turina, 2, Oviedo, Asturias, Spain'
place1.image = 'http://www.civisglobal.com/images%5Carticulos%5Cactividades%5Cobras%5Creformas%5CPizzaMov%5CPizzaMov04.jpg'
place1.category_id = 1


# Hangouts

place2 = c.factory.create("Place")
place2.name = 'cafe y mas'
place2.description = 'Your favourite coffee here!'
place2.lat = 43.370706
place2.lng = -5.838598
place2.address = 'Av Aureliano San Román, 41, 33010 Oviedo, Asturias, Spain'
place2.image = 'https://lh6.googleusercontent.com/-kCdzVKR7_2E/VNnTpzDWyyI/AAAAAAAAAAg/HCl8Bgn1x8I/s180-no/photo.jpg'
place2.category_id = 2

place3 = c.factory.create("Place")
place3.name = 'Café Gil de Jaz'
place3.description = 'Lots of coffees in the Oviedo city centre'
place3.lat = 43.363965
place3.lng = -5.852354
place3.address = 'Calle Gil de Jaz, 4, 33004 Oviedo, Asturias, Spain'
place3.image = 'http://www.cafegildejaz.es/img/img08.png'
place3.category_id = 2

# Leisure

place4 = c.factory.create("Place")
place4.name = 'Centro de Recepción e Interpretación del Prerrománico Asturiano'
place4.description = 'Asturian preromance, its origin, tradition, culture, etc.'
place4.lat = 43.378652
place4.lng = -5.867332
place4.address = 'Antiguas Escuelas del Naranco, s/n, 33012 Oviedo, Spain'
place4.image = 'http://www.prerromanicoasturiano.es/uploads/fotos/9KDiu8rgTBa74UkPrt2Q5jEPNPEzD4Ki.jpg'
place4.category_id = 3

# Personal care

place5 = c.factory.create("Place")
place5.name = 'OXYFIT Oviedo. Gimnasio. Centro deportivo. Oviedo'
place5.description = 'Undoubtebly the best gym in the capital of Asturias'
place5.lat = 43.36256
place5.lng = -5.856597
place5.address = 'Calle Matemático Pedrayes, 9, 33005 Oviedo, Asturias, Spain'
place5.image = 'http://www.oxyfitoviedo.es/wp-content/uploads/2014/10/DSC_0340.jpg'
place5.category_id = 4

#retval = c.service.put_place(place4)
#print(retval)

#c.service.del_place(1)
#print(c.service.get_all_place())
print(c.service.get_place_by_category('hangouts'))
'''