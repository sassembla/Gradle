# coding=UTF-8

import os
import sublime
import sublime_plugin
import subprocess
import threading 

class Gtest(sublime_plugin.TextCommand):
  def run (self, edit) :

    gradle = sublime.load_settings("Gradle.sublime-settings").get("command").get('gradle')
    test = sublime.load_settings("Gradle.sublime-settings").get("command").get('test')
    
    command = gradle + " " + test

    # 別スレッドから実行
    thread = BuildThread(self.view, command)
    thread.start()
    # self.view.set_status('gradle', 'build start')
    sublime.status_message('start:gradle '+test)

class BuildThread(threading.Thread):
  def __init__(self, view, command):
    self.view = view
    self.command = command
    threading.Thread.__init__(self)

  def run(self):
    print "run started ",self.command

    # この結果をハンドルしたい、、
    subprocess.call(self.command, shell=True)
    
    print "run end ",self.command
    

