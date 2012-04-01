#!/usr/bin/python
#/etc/postfix/master.cf
#mailjail unix - n n - - pipe
#  flags=FDRq user=_user_ argv=/home/_user_/mailjail/mailjail2.py $sender $recipient
#

import sys,os
import time


def jail_file (sender,receipient):

    DIR=os.path.abspath(os.path.dirname(__file__))+"/mail1"
    if False == os.path.isdir(DIR):
        os.mkdir(DIR)
    filename = "%s-%s-%s.eml" % (sender, receipient,time.strftime('%Y%m%dT%H%M%S',time.localtime()) )
    return os.path.join(  DIR , filename ) 

def main():
  print __file__ 
  (sender,receipient)=('from','to')
  if len(sys.argv) > 1:
    sender=sys.argv[1]
    if len(sys.argv)> 2:
       receipient = sys.argv[2]

  if sys.stdin.isatty():
    print "*** NO STDIN ***"
    return

  f=open( jail_file(sender,receipient) , 'w')
  if None != f:
    f.writelines(sys.stdin.readlines())
    f.close()


if __name__ == '__main__':
  main()
