
# coding=UTF-8

import os
import sublime
import sublime_plugin
import subprocess
import threading

def main_thread(callback, *args, **kwargs):
#     # sublime.set_timeout gets used to send things onto the main thread
#     # most sublime.[something] calls need to be on the main thread
#     sublime.set_timeout(functools.partial(callback, *args, **kwargs), 0)
  print "callback!"

# 色んな実験を行う。
class Testing(sublime_plugin.TextCommand):
  def run (self, edit) :
    print "os is ", os
    gradle = sublime.load_settings("Gradle.sublime-settings").get("command").get('gradle')
    build = sublime.load_settings("Gradle.sublime-settings").get("command").get('build')

    sublime.status_message('gradle '+build+" running...")

    #単純に実行、ただしロックしない。
    # self.view.window().run_command('exec', {'cmd': [gradle, 'build'], 'quiet': True})

    # メインスレッドでサブプロセスとして実行すると、あっという間にロックする。
    # subprocess.call(gradle + " " + 'build', shell=True)

    # スレッドを作成してスレッド内から実行したところ、問題ない！
    thread = BuildThread(self, gradle + " " + build)
    thread.start()

# スレッドの監視は重い。
    # プールを監視
    # self.handle_threads(thread, "aaa")

  def masterC(self):
    print "here comes"
    # 呼べるけどメインに帰って来れない。やっぱりなー
    sublime.status_message('gradle '+"build"+" done.")

  # def handle_threads(self, thread, message="def"):
  #   print "haha?" ,message
  #   # if thread.is_alive():
  #   #   print "still alive"

  #   if thread.result == False:
  #     # t = threading.Timer(1.0, self.handle_threads(thread))
  #     # t.start()
  #     print "still running"
    
  #   print "handle over"
    
class BuildThread(threading.Thread):
  def __init__(self, master, command):
    self.master = master
    self.command = command
    
    threading.Thread.__init__(self)

  def run(self):
    print "run started ",self.command
    subprocess.call(self.command, shell=True)

    # def切っても駄目
    # 

    sublime.set_timeout(
                    lambda: main_thread(self.command, self.master.masterC()),
                    0)

    # self.master.masterC()
    print "run end ",self.command
