# -*- coding: utf-8 -*-
r"""
    This module contains the implementation of the
    `inverse Mellin transformation <https://en.wikipedia.org/wiki/Mellin_inversion_theorem>`_.

    It contains the actual transformations itself, as well as the necessary tools
    such as the definition of paths.

    The integral routine is provided by :func:`scipy.integrate.quad`.

    Integration Paths
    -----------------

    Although this module provides four different path implementations in practice
    only the Talbot path :cite:`Abate`

    .. math::
        p_{\text{Talbot}}(t) =  o + r \cdot ( \theta \cot(\theta) + i\theta)\quad
            \text{with}~\theta = \pi(2t-1)

    is used, as it results in the most efficient convergence. The default values
    for the parameters :math:`r,o` are given by :math:`r = 1/2, o = 0` for
    the non-singlet integrals and by :math:`r = \frac{2}{5} \frac{16}{1 - \ln(x)}, o = 1`
    for the singlet sector. Note that the non-singlet kernels evolve poles only up to
    :math:`N=0` whereas the singlet kernels have poles up to :math:`N=1`.

"""  # pylint:disable=line-too-long

import numpy as np
import numba as nb


@nb.njit("c16(f8,f8,f8)", cache=True)
def Talbot_path(t, r, o):
    """
    Talbot path.

    .. math::
        p_{\\text{Talbot}}(t) =  o + r \\cdot ( \\theta \\cot(\\theta) + i\\theta ),
        \\theta = \\pi(2t-1)

    Parameters
    ----------
        r : float
            scaling parameter - effectivly corresponds to the intersection of the path with the
            real axis
        o : float
            offset on real axis

    Returns
    -------
        path : complex
            Talbot path
    """
    theta = np.pi * (2.0 * t - 1.0)
    re = 0.0
    if t == 0.5:  # treat singular point seperately
        re = 1.0
    else:
        re = theta / np.tan(theta)
    im = theta
    return o + r * np.complex(re, im)


@nb.njit("c16(f8,f8,f8)", cache=True)
def Talbot_jac(t, r, o):  # pylint: disable=unused-argument
    """
    Derivative of Talbot path.

    .. math::
        p_{\\text{Talbot}}(t) =  o + r \\cdot ( \\theta \\cot(\\theta) + i\\theta ),
        \\theta = \\pi(2t-1)

    Parameters
    ----------
        r : float
            scaling parameter - effectivly corresponds to the intersection of the path with the
            real axis
        o : float
            offset on real axis

    Returns
    -------
        jac : complex
            derivative of Talbot path
    """
    theta = np.pi * (2.0 * t - 1.0)
    re = 0.0
    if t == 0.5:  # treat singular point seperately
        re = 0.0
    else:
        re = 1.0 / np.tan(theta)
        re -= theta / (np.sin(theta)) ** 2
    im = 1.0
    return r * np.pi * 2.0 * np.complex(re, im)


def get_path_line():
    """
    Textbook path, i.e. a straight line parallel to the imaginary axis.

    .. math::
        p_{\\text{line}}(t) = c + m \\cdot (2t - 1)

    Returns the path and its derivative which then have to be called with the arguments
    listed under `Other Parameters`.

    Other Parameters
    ----------------
        m : float
            half length of the path
        c : float
            intersection of path with real axis

    Returns
    -------
        path : function
            textbook path
        jac : function
            derivative of textbook path
    """

    @nb.njit
    def path(t, m, c):
        return np.complex(c, m * (2 * t - 1))

    @nb.njit
    def jac(_t, m, _c):
        return np.complex(0, m * 2)

    return path, jac


def get_path_edge():
    """
    Edged path with a given angle.

    .. math::
        p_{\\text{edge}}(t) = c + m\\left|t - \\frac 1 2\\right|\\exp(i\\phi)

    Returns the path and its derivative which then have to be called with the arguments
    listed under `Other Parameters`.

    Other Parameters
    ----------------
        m : float
            length of the path
        c : float, optional
            intersection of path with real axis - defaults to 1
        phi : complex, optional
            bended angle - defaults to +135° with respect to positive x axis
    Returns
    -------
        path : function
            Edged path
        jac : function
            derivative of edged path
    """

    @nb.njit
    def path(t, m, c, phi):
        if t < 0.5:  # turning point: path is not differentiable in this point
            return c + (0.5 - t) * m * np.exp(np.complex(0, -phi))
        else:
            return c + (t - 0.5) * m * np.exp(np.complex(0, +phi))

    @nb.njit
    def jac(t, m, _c, phi):
        if t < 0.5:  # turning point: jacobian is not continuous here
            return -m * np.exp(np.complex(0, -phi))
        else:
            return +m * np.exp(np.complex(0, phi))

    return path, jac
