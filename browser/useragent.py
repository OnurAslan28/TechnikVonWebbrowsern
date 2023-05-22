import sys
import tkinter
import tkinter.font

from browser.layout.layout import Layout, VSTEP
from util.HTMLParser import HTMLParser
from util.request import request

SCROLL_STEP = 100


class Browser:
    def __init__(self, width, height):
        self.nodes = None
        self.height = height
        self.width = width
        self.window = tkinter.Tk()
        self.canvas = tkinter.Canvas(
            self.window,
            width=self.width,
            height=self.height
        )
        self.canvas.pack(expand=True, fill="both")
        self.display_list = []
        self.scroll = 0
        self.window.bind("<Down>", self.scrolldown)
        self.window.bind("<Up>", self.scrollup)
        self.window.bind("<Configure>", self.resize)

    def load(self, url):
        headers, body = request(url)
        self.nodes = HTMLParser(body).parse()
        self.display_list = Layout(self.nodes, self.width).display_list
        self.draw()

    def draw(self):
        self.canvas.delete("all")
        for x, y, c, f in self.display_list:
            if y > self.scroll + self.height:
                continue
            if y + VSTEP < self.scroll:
                continue
            self.canvas.create_text(x, y - self.scroll, text=c, font=f, anchor='nw')

    def scrolldown(self, e):
        self.scroll += SCROLL_STEP
        self.draw()

    def scrollup(self, e):
        if self.scroll - SCROLL_STEP < 0:
            self.scroll = 0
        else:
            self.scroll -= SCROLL_STEP
        self.draw()

    def resize(self, e):
        self.height = self.canvas.winfo_height()
        self.width = self.canvas.winfo_width()
        self.display_list = Layout(self.nodes, self.width).display_list
        self.draw()


if __name__ == "__main__":
    WIDTH, HEIGHT = 800, 600
    Browser(WIDTH, HEIGHT).load(sys.argv[1])
    tkinter.mainloop()
