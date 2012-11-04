# coding=UTF-8

import os
import sublime
import sublime_plugin
import subprocess
import threading

class Gbuild(sublime_plugin.TextCommand):
  def run (self, edit) :

    gradle = sublime.load_settings("Gradle.sublime-settings").get("path").get('gradle')
    build = sublime.load_settings("Gradle.sublime-settings").get("command").get('build')
    
    command = gradle + " " + build

    # 別スレッドから実行
    thread = BuildThread(self, command)
    thread.start()
    
    sublime.status_message('gradle '+build+" running...")


class BuildThread(threading.Thread):
  def __init__(self, master, command):
    self.master = master
    self.command = command

    threading.Thread.__init__(self)

  def run(self):
    print "run started ",self.command

    # この結果をハンドルしたい、、
    p = subprocess.call(self.command, shell=True)
    print "run end ",self.command, p
    

