'''
Description: a style sheet for Ttk to make it convenient to manage theme styles
Version: 1.0.2.20210209
Author: Arvin Zhao
Date: 2021-01-30 11:18:59
Last Editors: Arvin Zhao
LastEditTime: 2021-02-09 11:19:09
'''

from tkinter import ttk
from tkinter.constants import SOLID
from tkinter.font import BOLD

from bss.ui.conf import attrs, colours


CONTENT_LABEL = 'Content.TLabel'  # The style name of a content label.
EXPLANATION_LABEL = 'Explanation.TLabel'  # The style name of an explanation label.
IMG_BUTTON = 'Img.TButton'  # The style name of an image button.
LINK_LABEL = 'Link.TLabel'  # The style name of a link label.
PLACEHOLDER_LABEL = 'Placeholder.TLabel'  # The style name of a placeholder label.
PRIMARY_LABEL = 'Primary.TLabel'  # The style name of a primary content label.
TOOLTIP_LABEL = 'Tooltip.TLabel'  # The style name of a tooltip label.


def apply_style() -> dict:
    '''
    Apply customised styles to Ttk and get a dictionary of font configurations.

    Returns
    -------
    font_dict : a dictionary of some font configurations
    '''

    font_content = [attrs.FONT_FAMILY, attrs.CONTENT_FONT_SIZE]  # The content font.
    font_explanation = [attrs.FONT_FAMILY, attrs.EXPLANATION_FONT_SIZE]  # The explanation font.
    font_placeholder = [attrs.FONT_FAMILY, attrs.PADDING_Y]  # The placeholder font.
    font_primary = [attrs.FONT_FAMILY, attrs.PRIMARY_FONT_SIZE, BOLD]  # The primary content font.

    style = ttk.Style()

    style.configure('.', font = font_content)  # The style of every widget (it can be overridden by another style).
    style.configure('TButton', padding = attrs.PADDING_Y)
    style.configure(CONTENT_LABEL, padding = [0, attrs.PADDING_Y, 0, 0])  # The style of a content label.
    style.configure(EXPLANATION_LABEL, font = font_explanation, padding = [0, attrs.PADDING_Y, 0, 0])  # The style of an explanation label.
    style.configure(IMG_BUTTON, padding = attrs.IMG_BUTTON_PADDING)  # The style of an image button.
    style.configure(PLACEHOLDER_LABEL, font = font_placeholder)  # The style of a placeholder label.
    style.configure(PRIMARY_LABEL, font = font_primary)  # The style of a primary content label.
    style.configure(TOOLTIP_LABEL, background = colours.TOOLTIP_BACKGROUND, font = font_explanation, relief = SOLID)  # The style of a tooltip label.

    # The style of a link label.
    style.configure(LINK_LABEL, foreground = colours.HIGHLIGHT, padding = [0, attrs.PADDING_Y, 0, 0])
    style.map(LINK_LABEL,
              foreground = [('disabled', colours.DISABLED),
                            ('focus', colours.FOCUSED),
                            ('active', colours.ACTIVE)])

    return {'content_font': font_content, 'placeholder_font': font_placeholder}