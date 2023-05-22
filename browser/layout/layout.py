import tkinter.font

from browser.layout.text import Text


HSTEP, VSTEP = 13, 18
FONTS = {}


def get_font(size, weight, slant):
    key = (size, weight, slant)
    if key not in FONTS:
        font = tkinter.font.Font(size=size, weight=weight, slant=slant)
        FONTS[key] = font
    return FONTS[key]


class Layout:
    def __init__(self, tree, width):
        self.display_list = []
        self.line = []
        self.cursor_x = HSTEP
        self.cursor_y = VSTEP
        self.weight = "normal"
        self.style = "roman"
        self.size = 16
        self.width = width
        self.pre_tag = False
        self.recurse(tree)
        self.flush()

    def flush(self):
        if not self.line:
            return
        metrics = [font.metrics() for x, word, font in self.line]
        max_ascent = max([metric["ascent"] for metric in metrics])
        baseline = self.cursor_y + 1.25 * max_ascent
        for x, word, font in self.line:
            y = baseline - font.metrics("ascent")
            self.display_list.append((x, y, word, font))
        self.cursor_x = HSTEP
        self.line = []
        max_descent = max([metric["descent"] for metric in metrics])
        self.cursor_y = baseline + 1.25 * max_descent

    def text(self, tok):
        if self.pre_tag:
            print("Pre tag was found")
            for word in tok.text.split():
                font = get_font(self.size, self.weight, self.style)
                w = font.measure(word)
                if self.cursor_x + w > self.width - HSTEP:
                    self.flush()
                self.line.append((self.cursor_x, word, font))
                self.cursor_x += w + font.measure(" ")
        else:
            for word in tok.text.split():
                font = get_font(self.size, self.weight, self.style)
                w = font.measure(word)
                if self.cursor_x + w > self.width - HSTEP:
                    self.flush()
                self.line.append((self.cursor_x, word, font))
                self.cursor_x += w + font.measure(" ")

    def recurse(self, tree):
        if isinstance(tree, Text):
            self.text(tree)
        else:
            self.open_tag(tree.tag)
            for child in tree.children:
                self.recurse(child)
            self.close_tag(tree.tag)

    def open_tag(self, tag):
        if tag == "i":
            self.style = "italic"
        elif tag == "b":
            self.weight = "bold"
        elif tag == "small":
            self.size -= 2
        elif tag == "big":
            self.size += 4
        elif tag == "br":
            self.flush()
        elif tag == "pre":
            self.pre_tag = True

    def close_tag(self, tag):
        if tag == "i":
            self.style = "roman"
        elif tag == "b":
            self.weight = "normal"
        elif tag == "small":
            self.size += 2
        elif tag == "big":
            self.size -= 4
        elif tag == "/p":
            self.flush()
            self.cursor_y += VSTEP
        elif tag == "/pre":
            self.pre_tag = False


def print_tree(node, indent=0):
    print(" " * indent, node)
    for child in node.children:
        print_tree(child, indent + 2)
