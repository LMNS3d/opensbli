import numpy as np


def spline(x, y, n, y_start, y_end):
    """ Function to perform the CubicSpline, adapted from the version in
    'Numerical Recipes 3rd Edition: The Art of Scientific Computing' (2007).
    arg: ndarray: x: Array of values for the independent variable of the function to spline.
    arg: ndarray: y: Array of values y(x) for the independent variable of the function to spline.
    arg: int: n: Size of the x, y arrays.
    arg: float: y_start: Value of the first derivative to enforce at y'(0).
    arg: float: y_end: Value of the first derivative to enforce at y'(n-1).
    returns: ndarray: d2y: Array of values for the second derivative spline.
    """
    print type(x)
    exit()
    u, d2y = np.zeros_like(y), np.zeros_like(y)
    if (y_start > 0.99e30):  # Boundary condition set to natural
        d2y[0], u[0] = 0, 0
    else:  # Otherwise specify derivative at initial boundary
        d2y[0] = -0.5
        u[0] = (3.0/(x[1]-x[0]))*((y[1]-y[0])/(x[1]-x[0])-y_start)
    for i in range(1, n-1):  # Tridiagonal decomposition algorithm
        sig = (x[i]-x[i-1])/(x[i+1]-x[i-1])
        p = sig*d2y[i-1]+2.0
        d2y[i] = (sig-1.0)/p
        u[i] = (y[i+1]-y[i])/(x[i+1]-x[i]) - (y[i]-y[i-1])/(x[i]-x[i-1])
        u[i] = (6.0*u[i]/(x[i+1]-x[i-1]) - sig*u[i-1])/p
    if (y_end > 0.99e30):  # End boundary set to natural
        qn, un = 0, 0
    else:  # Otherwise end boundary first derivative is specified
        qn = 0.5
        un = (3.0/(x[n-1]-x[n-2]))*(y_end-(y[n-1]-y[n-2])/(x[n-1]-x[n-2]))
    d2y[n-1] = (un-qn*u[n-2])/(qn*d2y[n-2]+1.0)
    for k in range(n-2, -1, -1):  # Back substitution
        d2y[k] = d2y[k]*d2y[k+1]+u[k]
    return d2y


def splint(xa, ya, y2a, n, x):
    """ Function to perform the Splint, adapted from the version in
    'Numerical Recipes 3rd Edition: The Art of Scientific Computing' (2007). To be used
    with the CubicSpline generated by the spline routine.
    arg: ndarray: xa: Array of values for the independent variable used to create the spline.
    arg: ndarray: ya: Array of values y(x) for the independent variable used to create the spline.
    arg: ndarray: y2a: Array of values for the second derivative spline.
    arg: int: n: Size of the xa, ya, y2a arrays.
    arg: float: x: New value of the independent variable x to interpolate the function y onto.
    returns: float: y: The value of the function at the new x location.
    """
    klo, khi = 0, n-1
    while (khi - klo > 1):
        k = (khi+klo) // 2
        if (xa[k] > x):
            khi = k
        else:
            klo = k
    h = xa[khi] - xa[klo]
    if (h == 0):
        raise ValueError("Bad xa input, xa values must be distinct.")
    a = (xa[khi] - x)/h
    b = (x - xa[klo])/h
    y = a*ya[klo]+b*ya[khi]+((a**3 - a)*y2a[klo]+(b**3 - b)*y2a[khi])*(h**2)/6.0
    return y
