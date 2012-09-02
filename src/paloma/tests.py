# -*- coding: utf-8 -*-

from django.test import TestCase
#
from django.conf import settings
from django.core import mail
#
class EnrollTest(TestCase):

    fixtures = ["enroll/auth.json","enroll/paloma.json",]

    def test_activate(self):
        ''' python ../manage.py test paloma.EnrollTest.test_activate
        '''
        from paloma.models import Enroll,Notice,Mailbox
        mailbox = Mailbox.objects.all()[0]
        group =mailbox.groups.all()[0]

        enroll = Enroll.objects.provide_activate(mailbox,group )

        notice = group.owner.notice_set.filter(name="activate")[0]
        ret = notice.render(enroll=enroll,group=group )
        print ret[0]
        print ret[1]

    def test_signin(self):
        ''' python ../manage.py test paloma.EnrollTest.test_signin
        '''
        from paloma.models import Enroll,Notice,Mailbox
        mailbox = Mailbox.objects.all()[0]
        group =mailbox.groups.all()[0]

        enroll = Enroll.objects.provide_signin(mailbox,group )

        notice = group.owner.notice_set.filter(name="signin")[0]
        ret = notice.render(enroll=enroll,group=group )
        print ret[0]
        print ret[1]

    def test_signup(self):
        ''' python ../manage.py test paloma.EnrollTest.test_signup
        '''
        from paloma.models import Enroll,Notice,Group
        group = Group.objects.all()[0]

        enroll = Enroll.objects.provide_signup(group )

        print enroll.signup_email()

    def test_invite(self):
        ''' python ../manage.py test paloma.EnrollTest.test_invite
        '''
        from paloma.models import Enroll,Notice,Mailbox,Group
        from django.contrib.auth.models import User
        group =Group.objects.all()[0]
        inviter=User.objects.all()[0]

        enroll = Enroll.objects.provide_invite(group,inviter )

        notice = group.owner.notice_set.filter(name="invite")[0]
        ret = notice.render(enroll=enroll,group=group )
        print ret[0]
        print ret[1]

class SerTest(TestCase):

    def test_pickle(self):
        ''' python ../manage.py test paloma.SerTest.test_pickle
        '''
        from email import message_from_string
        msg='''From: gmail@hoge.com
To: hdknr@foooooo.deb
Subject:Hello

My First mail'''
        e = message_from_string(msg)
        self.assertEqual(e['From'] , 'gmail@hoge.com')

        # - serialize
        import pickle
        from cStringIO import StringIO

        src = StringIO()
        p = pickle.Pickler(src)


        p.dump(e)
        datastream = src.getvalue()
        print repr(datastream),type(datastream)
        
        # - deserialize
        dst = StringIO(datastream)        

        up= pickle.Unpickler(dst)
        e2 = up.load()
        print type(e2)
        #        
        self.assertEqual(e['From'] , e2['From'] )

class BounceTest(TestCase):

    fixtures = ["enroll/auth.json","enroll/paloma.json",]

    def test_returnpath(self):
        ''' python ../manage.py test paloma.BounceTest.test_returnpath
        '''
        import exceptions
        from paloma.models import default_return_path ,return_path_from_address
        MSG_FMT="bcmsg-%(message_id)s@%(domain)s"

        param = {'message_id': 3, "domain":"hogehoge.com" }

        return_path = default_return_path(param)
        result = return_path_from_address(return_path)

        for (k,v) in result.items():
            self.assertEqual(str(param[k]), v )

        for mail in ['','admin@google.com', ]:
            with self.assertRaises(exceptions.AttributeError) as cm:
                print "return_path_from_address(%s)" % str(mail), "=> AttributeError"
                result = return_path_from_address(mail)

        for mail in [None] :
            with self.assertRaises(exceptions.TypeError) as cm:
                print "return_path_from_address(%s)" % str(mail), "=> TypeError"
                result = return_path_from_address(mail)
