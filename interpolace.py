import pylab as lab
import scipy.interpolate as inp


x= [0, 0.3, 0.5, 0.8, 1,  2,  3 ]
y= [0, 0.1, 0.5, 1,   3, 10, 30]

x= "0 0.3 0.5 0.8 1  2  3".split()
y= "0 0.1 0.5 1   3 10 30".split()

x= list(map(float,x))
y= list(map(float,y))

lab.plot(x,y, "ro", label="původní hodnoty")

newX = lab.linspace(0, 3, 99)
funkce = inp.CubicSpline(x,y)
newY = funkce(newX, nu=1)
lab.plot(newX, newY, label="CubicSpline")

lab.plot(newX, inp.Akima1DInterpolator(x,y) (newX), label="Akima1DInterpolator")
lab.plot(newX, inp.PchipInterpolator(x,y) (newX), label="PchipInterpolator")



lab.legend()
lab.grid(1)
lab.show()
