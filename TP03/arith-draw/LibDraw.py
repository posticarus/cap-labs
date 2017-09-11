#!/usr/bin/python3
# -*- coding: utf-8 -*-

from tkinter import Tk, Frame, Canvas

# API for DrawPict language, CAP mini-project 2017
# Laure Gonnord, aug 2017

# A class for a Line


class Line:  # a line
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2

# Main class for a Frame


class LibDraw:
    def __init__(self, h, w, debug):
        self._bc = "lightgray"
        self._pixWidth = w+30
        self._pixHeight = h+30
        self._lines = []
        self._debug = debug

    def drawLine(self, line, g2):
        if self._debug:
            print('printing line from ('+str(line.x1)+','+str(line.y1) +
                  ' to ('+str(line.x2)+','+str(line.y2)+')')
        g2.create_line([line.x1, line.y1, line.x2, line.y2])

    def addLine(self, x1, y1, x2, y2):  # add a line
        self._lines.append(Line(x1, y1, x2, y2))

    def resize(self, nw, nh):
        self._pixWidth = nw
        self._pixHeight = nh

    # Main function:  show the Frame.
    def showPicture(self):
        root = Tk()
        app = Frame(master=root)
        app.master.title("DrawPict Interpret, 2017")
        w = Canvas(root, width=self._pixWidth, height=self._pixHeight)
        # now print all lines
        for line in self._lines:
            self.drawLine(line, w)
        w.pack()
        app.mainloop()
