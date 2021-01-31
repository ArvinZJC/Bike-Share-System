'''
Description: the definition of a user widget Tooltip
Version: 1.0.0.20210131
Author: Arvin Zhao
Date: 2021-01-30 20:51:12
Last Editors: Arvin Zhao
LastEditTime: 2021-01-30 20:53:00
'''

from tkinter import Toplevel, ttk

from bss.ui.conf import attrs, styles


class Tooltip:
    '''
    The class for using Tooltip.
    '''

    def __init__(self, parent, text) -> None:
        '''
        The constructor of the class for using Tooltip. Please note that the parent widget's `enter` and `leave` event may be affected.

        Parameters
        ----------
        parent : the parent widget using Tooltip
        '''
        self.parent = parent
        self.tooltip_window = None
        self.label_tooltip = None
        self.text = None
        self.set_text(text)

    # noinspection PyUnusedLocal
    def __show(self, event) -> None:
        '''
        Show the tooltip when the mouse enters the parent widget.

        Parameters
        ----------
        event : the event bound to the widget calling this function
        '''

        if self.tooltip_window is not None or self.text is None:
            return

        x, y, _, parent_height = self.parent.bbox('insert')
        x = x + self.parent.winfo_rootx() + attrs.TOOLTIP_OFFSET
        y = y + parent_height + self.parent.winfo_rooty() + attrs.TOOLTIP_OFFSET
        self.tooltip_window = Toplevel(self.parent)
        self.tooltip_window.wm_overrideredirect(1)
        self.tooltip_window.wm_geometry('+%d+%d' % (x, y))

        styles.apply_style()

        self.label_tooltip = ttk.Label(self.tooltip_window, style = styles.EXPLANATION_LABEL, text = self.text)
        self.label_tooltip.pack(ipadx = 1)

    # noinspection PyUnusedLocal
    def __hide(self, event) -> None:
        '''
        Hide the tooltip when the mouse leaves the parent widget.

        Parameters
        ----------
        event : the event bound to the widget calling this function
        '''

        if self.tooltip_window is not None:
            self.tooltip_window.destroy()
            self.tooltip_window = None

    def set_text(self, text = None) -> None:
        '''
        Set the tooltip text. Please note that the parent widget's `enter` and `leave` event may be affected.

        Parameters
        ----------
        text : the tooltip text
        '''

        if self.tooltip_window is not None and self.text is None:
            self.tooltip_window.destroy()
            self.tooltip_window = None
        else:
            self.parent.bind('<Enter>', self.__show)
            self.parent.bind('<Leave>', self.__hide)

        self.text = text


# Test purposes only.
if __name__ == '__main__':
    from tkinter import Button, Tk

    TOOLTIP_TEXT = 'Tooltip here!'


    def show_tooltip() -> None:
        '''
        Show the tooltip when the specified button is clicked.
        '''

        if tooltip_button.text is None:
            tooltip_button.set_text(TOOLTIP_TEXT)
        else:
            tooltip_button.set_text()


    test_window = Tk()
    test_window.geometry('200x200')
    test_window.title('Tooltip Test')
    test_button = Button(test_window, command = show_tooltip, text = 'Hover on me!')
    test_button.pack()
    tooltip_button = Tooltip(test_button, TOOLTIP_TEXT)
    test_window.mainloop()
