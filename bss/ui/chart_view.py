from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter.constants import BOTH
import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(BASE_DIR)

from bss.conf import attrs
from bss.ui.utils import img_path as img


class ChartView:
    '''
    The class for creating a chart view.
    '''

    def __init__(self, parent, title: str, fig) -> None:
        '''
        The constructor of the class for creating a chart view.

        Parameters
        ----------
        parent : the parent window for the manager view to display
        title : the parent window's title
        fig : figure
        '''

        parent.title(title)
        parent.iconbitmap(img.get_img_path(attrs.APP_ICON_FILENAME))
        parent.minsize(400, 300)

        canvas_chart = FigureCanvasTkAgg(fig, parent)
        canvas_chart.get_tk_widget().pack(expand = True, fill = BOTH)


# Test purposes only.
if __name__ == '__main__':
    from tkinter import Tk

    from bss.manager import Manager

    fig_test = Manager(3, 'xiaoran', '666666').plot_bike()
    chart_window = Tk()
    ChartView(chart_window, 'Test', fig_test)
    chart_window.mainloop()