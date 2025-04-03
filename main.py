from data import db_session, users


db_session.global_init('db/mars.db')
session = db_session.create_session()


user = users.User()
user.surname = 'Scott'
user.name = 'Ridley'
user.age = 21
user.position = 'captain'
user.speciality = 'research_engineer'
user.address = 'module_1'
user.email = 'scott_chief@mars.org'
session.add(user)
session.commit()

user = users.User()
user.surname = 'Wir'
user.name = 'Andy'
user.age = 20
user.position = 'engineer'
user.speciality = 'engineer'
user.address = 'module_2'
user.email = 'wir_notchief@mars.org'
session.add(user)
session.commit()

user = users.User()
user.surname = 'Whitney'
user.name = 'Mark'
user.age = 23
user.position = 'co-captain'
user.speciality = 'research_engineer'
user.address = 'module_3'
user.email = 'whitney_almostchief@mars.org'
session.add(user)
session.commit()

user = users.User()
user.surname = 'Kapoor'
user.name = 'Venkata'
user.age = 22
user.position = 'pilot'
user.speciality = 'pilot'
user.address = 'module_4'
user.email = 'kappor_notchief@mars.org'
session.add(user)
session.commit()