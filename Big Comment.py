import sublime
import sublime_plugin
import time
import threading

class InsertBigCommentCommand(sublime_plugin.TextCommand):
    def run(self, args):
        thread = BigComment(self.view, args)
        thread.start()

class InsertBigCommentText(sublime_plugin.TextCommand):
  def run(self, edit, args):
    self.view.insert(edit, self.view.sel()[0].begin(), args['comment'])

class BigComment(threading.Thread):
    """docstring for BigComment"""
    def __init__(self, view, args):
        self.view = view
        self.args = args
        super(BigComment, self).__init__()

    def run(self):
        prompt_for_big_comment = PromptUser('Big Comment:', 'PERSON')
        prompt_for_big_comment.start()
        prompt_for_big_comment.join()

        comment_text = prompt_for_big_comment.value
        chars = len(comment_text)

        # add the length of space plus -- twice
        chars = chars + 6
        dashes = chars * '-'
        dashes_and_comment = '-- ' + comment_text.upper() + ' --'

        big_comment = dashes + '\n' + dashes_and_comment + '\n' + dashes
        self.view.run_command("insert_big_comment_text", {"args":{'comment':big_comment}})

class PromptUser(threading.Thread):
    def __init__(self, prompt, caption=''):
        self.finished = False
        self.prompt = prompt
        self.caption = caption
        self.value = None
        super(PromptUser, self).__init__()

    def run(self):
        PromptForUserInput(
            self.prompt, self.caption,
            self.set_input_value, self.user_canceled)

        while self.finished == False:
            time.sleep(0.01)

    def user_canceled(self):
        self.value = None
        self.finished = True

    def set_input_value(self, input_value):
        self.value = input_value
        self.finished = True


class PromptForUserInput(object):
    """ The PromptForUserInput class is never called individually. It is called
    through PromptUser.

    The PromptForUserInput will manage opening the sublime input panel, and
    prompting for whatever is passed into the PromptUser thread.

    """
    def __init__(self, prompt, caption, on_done, on_cancel):
        self.prompt = prompt
        self.caption = caption
        self.input_value = ''
        self.on_done = on_done
        self.on_cancel = on_cancel
        self.window = None
        sublime.set_timeout(self.show_input, 1)
        sublime.set_timeout(self.on_cancel, 30000)

    def password(self, input):
        # we need to disregard the input, because it's just all asterisks
        self.on_done(self.input_value)
        self.finished = True

    def show_input(self):

        self.window = sublime.active_window()
        self.window.show_input_panel(
            self.prompt, self.caption, self.on_done,
            None, self.on_cancel)
