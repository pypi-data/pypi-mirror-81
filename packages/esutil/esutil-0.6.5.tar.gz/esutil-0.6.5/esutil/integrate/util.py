"""
Module:
    integrate


See docs for individual classes and functions for more detail.

Classes:
    QGauss:
        A class to perform gauss-legendre integration.

Functions:
    gauleg:
        Calculate the weights and abscissa for Gauss-Legendre integration.
"""
from __future__ import print_function

from sys import stdout
import numpy
from .. import stat
from .. import numpy_util

# for checking function type, method type
from types import *

try:
    from . import _cgauleg
    have_cgauleg=True
except:
    have_cgauleg=False

def qgauss(x,y,npts):
    qg=QGauss(npts)
    return qg.integrate(x,y)

class QGauss(object):
    """
    Module:
        integrate

    Class Name:
        QGauss
    
    Purpose:
        Perform gauss-legendre integration of points or functions.

    Methods:
        integrate: Perform the integration.
    Examples:
        from esutil.integrate import QGauss
        npoints = 30
        qg = QGauss(npoints)

        # integrate x-y point data
        result = qg.integrate(x, y)

        # integrate a function or method over the range xmin,xmax
        result = qg.integrate([xmin,xmax], some_function)

    """
    def __init__(self, npts=None):

        self.npts = None
        self.xxi = None
        self.wii = None
        self.f2 = None

        self.setup(npts=npts)

    def setup(self, npts=None):
        if npts is not None:
            if self.npts != npts:
                self.npts=npts
                self.xxi, self.wii = gauleg(-1.0, 1.0, self.npts)


    def integrate(self, xvals, yvals_or_func, npts=None):
        """
        Integrate a function or points
        """

        if isinstance(yvals_or_func,(FunctionType,MethodType)):
            return self.integrate_func(xvals,yvals_or_func,npts)
        else:
            return self.integrate_data(xvals,yvals_or_func,npts)

    def integrate_func(self, xvals, func, npts=None):
        """
        Integrate a function
        """
        self.setup(npts=npts)
        if self.npts is None:
            raise ValueError("Set npts on construction or in this call")

        if len(xvals) != 2:
            raise ValueError("When integrating a function, send the "
                             "x range [xmin,xmax] ")
        x1 = xvals[0]
        x2 = xvals[1]

        f1 = (x2-x1)/2.
        f2 = (x2+x1)/2.

        xi = self.xxi*f1 + f2

        yvals = func(xi)

        integrand = yvals*self.wii
        isum = integrand.sum()
        return f1*isum

    def integrate_data(self, xvals, yvals, npts=None):
        """
        Integrate over data, using linear interpolation
        """
        self.setup(npts=npts)
        if self.npts is None:
            raise ValueError("Set npts on construction or in this call")

        x1 = xvals.min()
        x2 = xvals.max()

        f1 = (x2-x1)/2.
        f2 = (x2+x1)/2.

        xi = self.xxi*f1 + f2

        # interpolate the yvalues to the right x values for gauss legendre
        # integration
        yi = stat.interplin(yvals, xvals, xi)

        integrand = yi*self.wii
        isum = integrand.sum()
        return f1*isum

    def test_gauss_data(self, npts=None):
        mean = 0.0
        sigma = 1.0

        num = 100
        xvals = numpy.arange(100)
        xvals = numpy_util.arrscl(xvals,mean-4.0*sigma,mean+4.0*sigma)

        norm = 1.0/numpy.sqrt(2.0*numpy.pi*sigma**2)
        gauss = norm*numpy.exp(-0.5*(xvals - mean)**2/sigma**2 )

        expected = 1.0

        ival = self.integrate_data(xvals, gauss, npts=npts)

        stdout.write("Expected value: %s\n" % expected)
        stdout.write("Got value: %s\n" % ival)

        pdiff = (ival - expected)/expected
        stdout.write("%% diff: %s\n" % pdiff)

    def test_gauss_func(self, npts=None):
        xrange = [-4.0,4.0]


        expected = 1.0

        ival = self.integrate_func(xrange, self.gaussfunc, npts=npts)

        stdout.write("Expected value: %s\n" % expected)
        stdout.write("Got value: %s\n" % ival)

        pdiff = (ival - expected)/expected
        stdout.write("%% diff: %s\n" % pdiff)


    def gaussfunc(self,xvals):
        mean=0.0
        sigma=1.0

        norm = 1.0/numpy.sqrt(2.0*numpy.pi*sigma**2)
        gauss = norm*numpy.exp(-0.5*(xvals - mean)**2/sigma**2 )

        return gauss

class QGauss2(object):
    """
    Perform gauss-legendre integration

    parameters
    ----------
    nx: int
        Number of points in x to use for integration
    ny: int
        Number of points in y to use for integration

    examples
    --------
    from esutil.integrate import QGauss2
    n1,n2 = 30,30
    qg = QGauss2(n1,n2)

    # integrate a function or method over the range xmin,xmax
    result = qg.integrate([xmin,xmax], [ymin,ymax], some_function)

    """
    def __init__(self, nx, ny):

        self.nx = nx
        self.ny = ny

        self._setup()

    def _setup(self):
        from numpy import ones, newaxis, meshgrid
        nx,ny = self.nx,self.ny

        x, wx = gauleg(-1.0, 1.0, nx)
        y, wy = gauleg(-1.0, 1.0, ny)

        self.xgrid, self.ygrid = meshgrid(x,y)

        wxgrid = ones( (nx,ny) )*wx[newaxis,:]
        wygrid = ones( (nx,ny) )*wy[:,newaxis]

        self.wgrid = wxgrid*wygrid

    def integrate_func(self, xrng, yrng, func):
        """
        Integrate a function
        """

        if len(xrng) != 2 or len(yrng) != 2:
            raise ValueError("xrng and yrng should be 2-element")

        x1 = xrng[0]
        x2 = xrng[1]
        y1 = yrng[0]
        y2 = yrng[1]

        xf1 = (x2-x1)/2.
        xf2 = (x2+x1)/2.
        yf1 = (y2-y1)/2.
        yf2 = (y2+y1)/2.

        xgrid = self.xgrid*xf1 + xf2
        ygrid = self.ygrid*yf1 + yf2

        zvals = func(xgrid, ygrid)

        integrand = zvals*self.wgrid

        isum = integrand.sum()
        return xf1*yf1*isum

    def test_gauss_func(self, npts=None):
        xrange = [-8.0,8.0]
        yrange = [-8.0,8.0]

        expected = 1.0

        ival = self.integrate_func(xrange, yrange, self.gaussfunc)

        stdout.write("Expected value: %s\n" % expected)
        stdout.write("Got value: %s\n" % ival)

        fracdiff = (ival - expected)/expected
        stdout.write("fracdiff: %s\n" % fracdiff)


    def gaussfunc(self, xvals, yvals):
        norm = 1.0/(2.0*numpy.pi)
        gauss = norm*numpy.exp( -0.5 * (xvals**2 + yvals**2) )

        return gauss


def gauleg(x1, x2, npts):
    """
    NAME:
      gauleg()
      
    PURPOSE:
      Calculate the weights and abscissa for Gauss-Legendre integration.
    
    CALLING SEQUENCE:
      x,w = gauleg(x1,x2,npts)

    INPUTS:
      x1,x2: The range for the integration.
      npts: Number of points to use in the integration.

    REVISION HISTORY:
      Created: 2010-04-18. Use the new C++ extension and only 
      drop back to python only version if necessary.
    """

    if have_cgauleg:

        if npts <= 0:
            raise ValueError("npts should be > 0, got %s" % npts)

        x,w = _cgauleg.cgauleg(x1,x2,npts)
    else:
        raise ValueError("gauleg C++ extension not found")

    return x,w


