#!/usr/bin/env python3

from os.path import basename, splitext
import tkinter as tk
from tkinter import filedialog
import pylab as pl
from scipy.interpolate import (
    CubicSpline,
    PchipInterpolator,
    Akima1DInterpolator,
    UnivariateSpline,
)

# from tkinter import ttk


class MyEntry(tk.Entry):
    def __init__(self, master=None, cnf={}, **kw):
        super().__init__(master, cnf, **kw)

        if not "textvariable" in kw:
            self.variable = tk.StringVar()
            self.config(textvariable=self.variable)
        else:
            self.variable = kw["textvariable"]

    @property
    def value(self):
        return self.variable.get()

    @value.setter
    def value(self, new: str):
        self.variable.set(new)


class Application(tk.Tk):
    name = basename(splitext(basename(__file__.capitalize()))[0])
    name = "Foo"
    colors = (
        "black",
        "red",
        "yellow",
        "cyan",
        "magenta",
        "green",
        "blue",
        "orange",
        "coral",
        "darkblue",
    )
    ifunction = {}
    for f in CubicSpline, PchipInterpolator, Akima1DInterpolator, UnivariateSpline:
        ifunction[f.__name__] = f
    ifunction = {
        f.__name__: f
        for f in (CubicSpline, PchipInterpolator, Akima1DInterpolator, UnivariateSpline)
    }

    def __init__(self):
        super().__init__(className=self.name)
        self.title(self.name)
        self.bind("<Escape>", self.quit)
        self.lbl = tk.Label(self, text="Hello tkGraf")
        self.lbl.pack()

        self.fileFrame = tk.LabelFrame(self, text="Soubor")
        self.fileFrame.pack(padx=5, pady=5, fill="x")
        self.fileEntry = MyEntry(self.fileFrame)
        self.fileEntry.pack(fill="x")
        self.fileBtn = tk.Button(self.fileFrame, text="...", command=self.chooseFile)
        self.fileBtn.pack(anchor="e")

        self.dataVar = tk.StringVar(value="ROW")
        self.rowRadio = tk.Radiobutton(
            self.fileFrame,
            text="Data jsou v řádcích",
            variable=self.dataVar,
            value="ROW",
        )
        self.rowRadio.pack(anchor="w")
        self.columnRadio = tk.Radiobutton(
            self.fileFrame,
            text="Data jsou ve sloupcích",
            variable=self.dataVar,
            value="COLUMN",
        )
        self.columnRadio.pack(anchor="w")

        self.grafFrame = tk.LabelFrame(self, text="Graf")
        self.grafFrame.pack(padx=5, pady=5, fill="x")

        tk.Label(self.grafFrame, text="Titulek").grid(row=0, column=0)
        self.titleEntry = MyEntry(self.grafFrame)
        self.titleEntry.grid(row=0, column=1, sticky=tk.NSEW, columnspan=2)

        tk.Label(self.grafFrame, text="osa X").grid(row=1, column=0)
        self.xlabelEntry = MyEntry(self.grafFrame)
        self.xlabelEntry.grid(row=1, column=1, sticky=tk.NSEW, columnspan=2)

        tk.Label(self.grafFrame, text="osa Y").grid(row=2, column=0)
        self.ylabelEntry = MyEntry(self.grafFrame)
        self.ylabelEntry.grid(row=2, column=1, sticky=tk.NSEW, columnspan=2)

        tk.Label(self.grafFrame, text="styl čáry").grid(row=3, column=0)
        self.lineVar = tk.StringVar(value="None")
        tk.OptionMenu(self.grafFrame, self.lineVar, "none", ":", "-.", "--", "-").grid(
            row=3, column=1, sticky="w"
        )
        self.colorVar = tk.StringVar(value=self.colors[0])
        tk.OptionMenu(self.grafFrame, self.colorVar, *self.colors).grid(
            row=3, column=2, sticky="w"
        )

        tk.Label(self.grafFrame, text="marker").grid(row=4, column=0)
        self.markerVar = tk.StringVar(value="None")
        tk.OptionMenu(
            self.grafFrame, self.markerVar, "none", *tuple(" .,o+PxX*1234<>v^")
        ).grid(row=4, column=1, sticky="w")
        self.mcolorVar = tk.StringVar(value=self.colors[0])
        tk.OptionMenu(self.grafFrame, self.mcolorVar, *self.colors).grid(
            row=4, column=2, sticky="w"
        )

        self.gridVar = tk.BooleanVar(value=True)
        tk.Label(self.grafFrame, text="mřížka").grid(row=5, column=0)
        tk.Checkbutton(self.grafFrame, variable=self.gridVar).grid(
            row=5, column=1, sticky="w"
        )

        tk.Label(self.grafFrame, text="interpolace").grid(row=6, column=0)
        self.interpolationVar = tk.StringVar(value="None")
        tk.OptionMenu(
            self.grafFrame, self.interpolationVar, "None", *self.ifunction.keys()
        ).grid(row=6, column=1)
        self.icolorVar = tk.StringVar(value=self.colors[0])
        tk.OptionMenu(self.grafFrame, self.icolorVar, *self.colors).grid(
            row=6, column=2, sticky="w"
        )

        tk.Button(self, text="Kresli", command=self.plot).pack(fill="x")
        tk.Button(self, text="Quit", command=self.quit).pack()

    def chooseFile(self):
        path = filedialog.askopenfilename()
        self.fileEntry.value = path
        self.fileEntry.xview_moveto(1)

    def plot(self):
        with open(self.fileEntry.value) as f:
            if self.dataVar.get() == "ROW":
                line = f.readline()
                x = line.split(";")
                line = f.readline()
                y = line.split(";")
                x = [float(i.replace(",", ".")) for i in x]
                y = [float(i.replace(",", ".")) for i in y]
            elif self.dataVar.get() == "COLUMN":
                x = []
                y = []
                while True:
                    line = f.readline()
                    if line == "":
                        break
                    if ";" not in line:
                        continue
                    x1, y1 = line.split(";")
                    x.append(float(x1.replace(",", ".")))
                    y.append(float(y1.replace(",", ".")))

        kwargs = {}
        kwargs["linestyle"] = self.lineVar.get()
        kwargs["marker"] = self.markerVar.get()
        kwargs["color"] = self.colorVar.get()
        kwargs["markerfacecolor"] = self.mcolorVar.get()
        kwargs["markeredgecolor"] = self.mcolorVar.get()
        pl.plot(x, y, **kwargs)
        # pl.plot(x, y, linestyle=self.lineVar.get(), marker=self.markerVar.get())

        if self.interpolationVar.get() in self.ifunction:
            x_min = min(x)
            x_max = max(x)
            xx = pl.linspace(x_min, x_max)
            funkce = self.ifunction[self.interpolationVar.get()](x, y)
            yy = funkce(xx)
            pl.plot(xx, yy, color=self.icolorVar.get())

        pl.grid(self.gridVar.get())
        pl.title(self.titleEntry.value)
        pl.xlabel(self.xlabelEntry.value)
        pl.ylabel(self.ylabelEntry.value)
        pl.show()

    def quit(self, event=None):
        super().quit()


app = Application()
app.mainloop()