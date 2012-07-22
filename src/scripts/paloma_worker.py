''' 
Paloma Start:

    - execute absolute path to paloma_start.py
    - give your django application path to the first argument

::

    $ /home/hdknr/ve/paloma/bin/paloma_start.py /home/hdknr/ve/paloma/src/paloma/app start

'''
if __name__ == '__main__':
    import sys,os
    if len(sys.argv) < 2:
        sys.stderr.write('you need path of your django application')
        sys.exit(1) 

    sys.path.append(os.path.dirname(sys.argv[1]))    #: Important
    sys.path.append(sys.argv[1])    #: Important

    from django.core.management import execute_manager
    import imp
    try:
        imp.find_module('settings') # Assumed to be in the same directory.
    except ImportError:
        import sys
        sys.stderr.write("Error: Can't find the file 'settings.py' in the directory containing %r. It appears you've customized things.\nYou'll have to run django-admin.py, passing it your settings module.\n" % __file__)
        sys.exit(1)
    
    import settings
    import run
    
    if __name__ == "__main__":
        sys.argv = run.configure(sys.argv) #
        print "palaoma workder ",sys.argv
        execute_manager(settings)
