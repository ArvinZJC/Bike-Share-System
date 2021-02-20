'''
Description: the definition of customised Tkinter simple dialogues
Version: 1.0.1.20210220
Author: Arvin Zhao
Date: 2021-02-19 10:20:30
Last Editors: Arvin Zhao
LastEditTime: 2021-02-20 10:57:50
'''

from tkinter import simpledialog

from bss.conf import attrs
from bss.ui.utils import img_path as img


# noinspection PyProtectedMember
class FloatDialogue(simpledialog._QueryFloat):
    '''
    The class for creating a customised Tkinter simple float dialogue.
    '''

    def body(self, master):
        super().body(master)
        self.iconbitmap(img.get_img_path(attrs.APP_ICON_FILENAME))

    @staticmethod
    def askfloat(title: str, prompt: str, **kw) -> float:
        '''
        Show a customised Tkinter simple float dialogue.

        Parameters
        ----------
        title : the dialogue's title
        prompt : the prompt on the dialogue
        kw : some properties controlling the dialogue's behaviours

        Returns
        -------
        result : a floating point value or `None`
        '''

        d = FloatDialogue(title, prompt, **kw)
        return d.result


# noinspection PyProtectedMember
class IntegerDialogue(simpledialog._QueryInteger):
    '''
    The class for creating a customised Tkinter simple integer dialogue.
    '''

    def body(self, master):
        super().body(master)
        self.iconbitmap(img.get_img_path(attrs.APP_ICON_FILENAME))

    @staticmethod
    def askinteger(title: str, prompt: str, **kw) -> int:
        '''
        Show a customised Tkinter simple integer dialogue.

        Parameters
        ----------
        title : the dialogue's title
        prompt : the prompt on the dialogue
        kw : some properties controlling the dialogue's behaviours

        Returns
        -------
        result : an integer or `None`
        '''

        d = IntegerDialogue(title, prompt, **kw)
        return d.result


# noinspection PyProtectedMember
class StringDialogue(simpledialog._QueryString):  # TODO: remove this if it is not used
    '''
    The class for creating a customised Tkinter simple string dialogue.
    '''

    def body(self, master):
        super().body(master)
        self.iconbitmap(img.get_img_path(attrs.APP_ICON_FILENAME))

    @staticmethod
    def askstring(title: str, prompt: str, **kw) -> str:
        '''
        Show a customised Tkinter simple string dialogue.

        Parameters
        ----------
        title : the dialogue's title
        prompt : the prompt on the dialogue
        kw : some properties controlling the dialogue's behaviours

        Returns
        -------
        result : a string value or `None`
        '''

        d = StringDialogue(title, prompt, **kw)
        return d.result


# Test purposes only.
if __name__ == '__main__':
    from tkinter import Tk

    test_window = Tk()
    screen_width = test_window.winfo_screenwidth()
    screen_height = test_window.winfo_screenheight()
    parent_length = 500
    test_window.geometry('%dx%d+%d+%d' % (parent_length, parent_length, (screen_width - parent_length) / 2, (screen_height - parent_length) / 2))  # Centre the parent window.
    test_window.title('Test')
    test_window.iconbitmap(img.get_img_path(attrs.APP_ICON_FILENAME))
    print(FloatDialogue.askfloat('Float dialogue test', 'Enter anything for testing:'))
    print(IntegerDialogue.askinteger('Integer dialogue test', 'Enter anything for testing:'))
    print(StringDialogue.askstring('String dialogue test', 'Enter anything for testing:'))
    test_window.mainloop()