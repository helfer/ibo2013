from django.contrib.auth.models import User, Group


def make_testuser(start,end):
    for i in xrange(start,end):
        new_user=User.objects.create_user('test{0}'.format(i),
                                  'test1@ibosuisse.ch',
                                  'test{0}'.format(i))
        new_user.first_name = "Test"
        new_user.last_name = str(i)
        new_user.save()
        print new_user
