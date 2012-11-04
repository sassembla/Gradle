
# coding=UTF-8

import os
import sys
import sublime
import sublime_plugin
import subprocess
import shlex
import threading



# 色んな実験を行う。
class Testing(sublime_plugin.TextCommand):
  def run (self, edit) :
    print "os is ", os

    gradle = sublime.load_settings("Gradle.sublime-settings").get("path").get('gradle')
    build = sublime.load_settings("Gradle.sublime-settings").get("command").get('build')

   
    # 別スレッドで実行
    thread = BuildThread(gradle + " " + build)
    thread.start()

    #statusBarに経過表示
    ThreadProgress(thread, 'gradle '+build+" running...", 'gradle '+build+" Done.")

    
class BuildThread(threading.Thread):
  def __init__(self, command):
    self.command = command
    
    
    threading.Thread.__init__(self)

  def run(self):

    # run command
    # a = subprocess.call(self.command, shell=True) これは値しか返さない。
    # a = subprocess.call(self.command, shell=True, stdout=subprocess.PIPE)コレも一緒。

    # a = subprocess.check_call(self.command, shell=True, stdout=subprocess.PIPE)
    
    a = subprocess.Popen(shlex.split(self.command.encode('utf8')))
    print "a is ",a

    output = a.communicate()[0]
    print "output is ", output
    
    # もし遠い将来、Python2.7系がデフォルトで入ったら、callの代わりにcheck_outputを使って
    # コンソールの内容とパラメータをtail的に返してあげたいところ。

    # while True:
    #   out = child.stderr.read(1)
    #   if out == '' and child.poll() != None:
    #     print "break!"
    #     break
    #   if out != '':
    #     sys.stdout.write(out)
    #     sys.stdout.flush()
    #     print "!?"


class ThreadProgress():
  def __init__(self, thread, message, success_message):
    self.thread = thread

    self.message = message
    self.success_message = success_message
    
    self.addend = 1
    self.size = 8
    sublime.set_timeout(lambda: self.run(0), 100)

  def run(self, i):
    if not self.thread.is_alive():
        if hasattr(self.thread, 'result'):
            print self.thread.result
        sublime.status_message(self.success_message)
        return

    before = i % self.size
    after = (self.size - 1) - before
    sublime.status_message('%s [%s=%s]' % \
        (self.message, ' ' * before, ' ' * after))

    # カーソルをふらふらさせる
    if not after:
        self.addend = -1
    if not before:
        self.addend = 1
    i += self.addend

    # 100後に再度実行
    sublime.set_timeout(lambda: self.run(i), 100)
