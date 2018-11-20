# coding=utf-8

"""Hello world demo module"""
import six


def run_demo(console, text):
    """Show message"""

    six.print_(text)

    if not console:
        from tkinter import Tk, Label

        root = Tk()

        label = Label(root, text=text)
        label.pack()

        #uncomment root.mainloop() to enter tk main loop.
        #Delete any unit tests covering this section first
        #though as they will not complete.

        #root.mainloop()

    return True
