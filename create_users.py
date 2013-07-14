from django.db import connection
from django.contrib.auth.models import User,Group
from django.db import transaction

cursor = connection.cursor()

@transaction.commit_on_success
def create_users():
    query = "SELECT * FROM ibo2013_countries"

    cursor.execute(query)
    countries = dictfetchall(cursor)

    #query = "SELECT * FROM ibo2013_delegation_categories"
    #cursor.execute(query)
    #delegations = cursor.fetchall()

    query = "SELECT * FROM ibo2013_participants p JOIN ibo2013_countries c ON c.id = p.country_id JOIN ibo2013_delegation_categories d ON d.id = p.delegation_category_id"
    cursor.execute(query)
    users = dictfetchall(cursor)


    print countries[:10]
    #print delegations[:10]
    print users[:10]


    roles = ['Student','Jury']

    for c in countries:
        g, created = Group.objects.get_or_create(name=c['en'])
        g.save()

    for r in roles:
        g,created = Group.objects.get_or_create(name=r)
        g.save()

    for u in users:
        if u['class'] in ['Student','Jury']:
            new_user,created = User.objects.get_or_create(
            username=u['username'],
            first_name=u['first_name'],
            last_name=u['last_name'],
            )
        
            if created:
               new_user.set_password(u['password'])
               cgroup = Group.objects.get(name=u['en'])
               rolegroup = Group.objects.get(name=u['class'])
               new_user.groups.add(cgroup)
               new_user.groups.add(rolegroup)
            else:
                new_user.is_active = True           
                new_user.email = u['email']
 
            new_user.save()

            print "user " + u['username'] + " created" 

        else:
            pass
        
def dictfetchall(cursor):
    "Returns all rows from a cursor as a dict"
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]
