import numpy as np
import scipy.optimize as op


class pmodel(object):

    def mu_model(self, *args):
        # linear model for mean
        m, b, x = args
        return m * x + b

    def sig_model(self, *args):
        c, d, x = args
        return np.true_divide(c, x) + d

    def ln_sig_model(self, *args):
        # sigma has a c/x + d model
        lnc, lnd, x = args
        return np.true_divide(np.exp(lnc), x) + np.exp(lnd)

    def lnlike(self, theta, x, y):
        m, b, lnc, lnd = theta
        mu = self.mu_model(m, b, x)
        inv_sig_sq = 1.0/self.ln_sig_model(lnc, lnd, x)**2
        return -0.5*(np.sum(inv_sig_sq*(y-mu)**2 - np.log(2*np.pi*inv_sig_sq)))

    def fit_max_like(self, m_guess, b_guess, c_guess, d_guess, x, y):
        nll = lambda *args: -self.lnlike(*args)
        result = op.minimize(
            nll,
            [m_guess, b_guess, np.log(c_guess), np.log(d_guess)],
            args=(x, y))
        return result

    def lnprior(theta):
        m, b, lnc, lnd = theta
        if -1.0 < m < 1.0 and -1.0 < b < 1.0 and -10.0 < lnc < 10.0 and -10.0 < lnd < 10.0:
            return 0.0
        else:
            return -np.inf

    def lnprob(self, theta, x, y):
        lp = self.lnprior(theta)
        if not np.isfinite(lp):
            return -np.inf
        else:
            return lp + self.lnlike(theta, x, y)
