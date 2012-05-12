#!/usr/bin/env python
# -*- coding: utf-8 -*-


import sys, os, time, atexit
from datetime import datetime
from signal import SIGTERM
from django.utils.daemonize import become_daemon

class Daemon(object):
    """
    A generic daemon class.
    Usage: subclass the Daemon class and override the run() method
    """
    def __init__(self, pidfile='daemin.pid', std_out='/dev/null',
                 std_err='/dev/null', silent=False):
        self.pidfile = pidfile
        self.std_out = std_out
        self.std_err = std_err
        self.silent = silent

    def delpid(self):
        try:
            os.remove(self.pidfile)
        except Exception:
            self.log('OSERROR!!!!!')
        else:
            self.log('PID, deleted!')
    
    def daemonize(self):
        become_daemon(err_log=self.std_err, out_log=self.std_out)
        # write pidfile
        atexit.register(self.delpid)
        pid = str(os.getpid())
        file(self.pidfile,'w+').write("%s\n" % pid)
    
    def start(self):
        """
        Start the daemon
        """
        # Check for a pidfile to see if the daemon already runs
        try:
            pf = file(self.pidfile,'r')
            pid = int(pf.read().strip())
            pf.close()
        except IOError:
            pid = None
        
        if pid:
            message = 'pidfile %s already exist. Daemon already running?'
            self.log(message % self.pidfile)
            return
        
        # Start the daemon
        self.daemonize()
        self.run()
    
    def stop(self):
        """
        Stop the daemon
        """
        # Get the pid from the pidfile
        try:
            pf = file(self.pidfile,'r')
            pid = int(pf.read().strip())
            pf.close()
        except IOError:
            pid = None
        
        if not pid:
            message = 'pidfile %s does not exist. Daemon not running?'
            self.log(message % self.pidfile)
            return # not an error in a restart
        
        # Try killing the daemon process
        if os.getpid() != pid:
            try:
                while True:
                    os.kill(pid, SIGTERM)
                    time.sleep(0.1)
                self.delpid()
            except OSError as err:
                err = str(err)
                if err.find('No such process') > 0:
                    if os.path.exists(self.pidfile):
                        os.remove(self.pidfile)
                else:
                    self.log(str(err))
                    return False
        
        self.log('Stoped')
        return True
    
    def restart(self):
        """
        Restart the daemon
        """
        self.stop()
        self.start()
    
    def run(self):
        """
        You should override this method when you subclass Daemon. It will be
        called after the process has been
        daemonized by start() or restart().
        """
        raise NotImplemented()
    
    def log(self, text):
        if not self.silent:
            print '[%s] >>> DAEMON %s:' % (datetime.now(), self.pidfile), text
    
    def execute(self, command):
        commands = {
            'start': self.start,
            'stop': self.stop,
            'restart': self.restart
        }
        if command not in commands:
            self.log('Unknown command')
            sys.exit(2)
        else:
            commands[command]()
            sys.exit(0)

    def execute_from_cli(self, command_index=1):
        if len(sys.argv) >= command_index + 1:
            self.execute(sys.argv[command_index])
        else:
            invoke_line = ' '.join(sys.argv[:command_index])
            self.log('Ussage: %s start|stop|restart' % invoke_line)
            sys.exit(2)
    
    
    
