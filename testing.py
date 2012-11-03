
# coding=UTF-8

import os
import sublime
import sublime_plugin
import subprocess
import threading 

# 色んな実験を行う。
class Testing(sublime_plugin.TextCommand):
  def run (self, edit) :
    print "os is ", os
    gradle = sublime.load_settings("Gradle.sublime-settings").get("command").get('gradle')
    build = sublime.load_settings("Gradle.sublime-settings").get("command").get('build')

    #単純に実行、ただしロックしない。
    # self.view.window().run_command('exec', {'cmd': [gradle, 'build'], 'quiet': True})

    # メインスレッドでサブプロセスとして実行すると、あっという間にロックする。
    # subprocess.call(gradle + " " + 'build', shell=True)

    # スレッドを作成してスレッド内から実行したところ、問題ない！
    thread = BuildThread(self.view, gradle + " " + build)
    thread.start()

    
class BuildThread(threading.Thread):
  def __init__(self, view, command):
    self.view = view
    self.command = command
    threading.Thread.__init__(self)

  def run(self):
    print "run started ",self.command
    subprocess.call(self.command, shell=True)
    print "run end ",self.command
    