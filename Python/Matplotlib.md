# Matplotlib Cheatsheet

Matplotlib prepares 2D (and some 3D) graphics. 
 
- Main page: http://www.matplotlib.org
- Image gallery: http://matplotlib.org/gallery.html 
- pyplot command summary: http://matplotlib.org/api/pyplot_summary.html 
- Examples http://matplotlib.org/examples/index.html
- Tutorial: http://www.loria.fr/~rougier/teaching/matplotlib/
- See also: https://www.wakari.io/nb/url///wakari.io/static/notebooks/Lecture_4_Matplotlib.ipynb

## Matplotlib, pylab, and pyplot: how are they related?

- Matplotlib is the whole package. Pylab and matplotlib.pyplot (pyplot in the following) are modules in matplotlib.
- Pyplot makes matplotlib work like MATLAB. 
- Pyplot provides the state-machine interface to the underlying plotting library (the matplotlib API in the matplotlib module). 
- Each pyplot function makes some change to a figure: eg, create a figure, create a plotting area in a figure, plot some lines in a plotting area, decorate the plot with labels, etc.... 
- Pyplot is __stateful__, in that it keeps track of the current figure and plotting area, and the plotting functions are directed to the current axes.
- Pylab combines the pyplot functionality (for plotting) with the numpy functionality (mathematics / arrays) in a single namespace, making that namespace (or environment) even more MATLAB-like. 
- The pyplot interface is generally preferred for non-interactive plotting (i.e., scripting). 
- The pylab interface is convenient for interactive calculations and plotting, as it minimizes typing.

