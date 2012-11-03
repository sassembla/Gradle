import os
import sublime
import sublime_plugin

import threading 


class Build(sublime_plugin.TextCommand):
  def run (self, edit) :
    #generate other-thead and run build.
    thread = Some(self.view)
    thread.start()

    # self.handle_threads(threads)
    # this can run everything with other-process.
    # import os, subprocess, sys
    # CMD = "gradle test"#"gradle build"

    # try:
    #   print "Executing command is : " , CMD #, self.view.file_name()
    #   retcode = subprocess.call(CMD, shell=True)
     

    #   if retcode < 0:
    #     print >>sys.stderr, "Aborted : ", -retcode
    #   else:
    #     print >>sys.stderr, "Return code : ", retcode

    # except OSError, e:
    #   print >>sys.stderr, "OSError cptured : ", e


class Some(threading.Thread):
  def __init__(self, view):
    print "init!"
    self.view = view
    threading.Thread.__init__(self)

  def run(self):
    print "run!"
    self.view.window().run_command('exec', {'cmd': ['/usr/local/bin/gradle', 'build'], 'quiet': True})  