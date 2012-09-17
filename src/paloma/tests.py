from django.test import TestCase
#
from django.conf import settings
from django.core import mail
#
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
