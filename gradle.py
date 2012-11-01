import os

import sublime

class GradleInit(object):
    def some(self, directory):
        if os.path.exists(directory):
        	sublime.status_message("Directory does not exist.")
            #self.run_command(['git', 'init'], self.git_inited, working_dir=directory)
        #else:
         #   sublime.status_message("Directory does not exist.")

    def some2(self, result):
        sublime.status_message("result")
