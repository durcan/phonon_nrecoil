import numpy as np
import scipy.optimize as op
import matplotlib.pyplot as pl
from matplotlib.ticker import MaxNLocator
import triangle


class pmodel(object):

    def mu_model(self, *args):
        # linear model for mean
        m, b, x = args
        return m * x + b

    def sig_model(self, *args):
        c, d, e, x = args
        return np.true_divide(c, x) + d*x + e

    def ln_sig_model(self, *args):
        # sigma has a c/x + d model
        lnc, d, lne, x = args
        return np.true_divide(np.exp(lnc), x) + d*x + np.exp(lne)

    def lnlike(self, theta, x, y):
        m, b, lnc, lnd = theta
        mu = self.mu_model(m, b, x)
        inv_sig_sq = 1.0/self.ln_sig_model(lnc, lnd, x)**2
        return -0.5*(np.sum(inv_sig_sq*(y-mu)**2 - np.log(2*np.pi*inv_sig_sq)))

    def fit_max_like(self, m_guess, b_guess, c_guess, d_guess, e_guess, x, y):
        nll = lambda *args: -self.lnlike(*args)
        result = op.minimize(
            nll,
            [m_guess, b_guess, np.log(c_guess), d_guess],
            args=(x, y))
        return result

    def lnprior(self, theta):
        m, b, lnc, lnd = theta
        if (
                -1.0 < m < 1.0 and
                -1.0 < b < 1.0 and
                -10.0 < lnc < 10.0 and
                -10.0 < lnd < 10.0
                ):
            return 0.0
        else:
            return -np.inf

    def lnprob(self, theta, x, y):
        lp = self.lnprior(theta)
        if not np.isfinite(lp):
            return -np.inf
        else:
            return lp + self.lnlike(theta, x, y)

    def runner_graph(self, sampler):
        pl.clf()
        fig, axes = pl.subplots(4, 1, sharex=True, figsize=(8, 9))
        axes[0].plot(sampler.chain[:, :, 0].T, color="k", alpha=0.4)
        axes[0].yaxis.set_major_locator(MaxNLocator(5))
        axes[0].set_ylabel("$m$")

        axes[1].plot(sampler.chain[:, :, 1].T, color="k", alpha=0.4)
        axes[1].yaxis.set_major_locator(MaxNLocator(5))
        axes[1].set_ylabel("$b$")

        axes[2].plot(np.exp(sampler.chain[:, :, 2]).T, color="k", alpha=0.4)
        axes[2].yaxis.set_major_locator(MaxNLocator(5))
        axes[2].set_ylabel("$lnc$")

        axes[3].plot(np.exp(sampler.chain[:, :, 3]).T, color="k", alpha=0.4)
        axes[3].yaxis.set_major_locator(MaxNLocator(5))
        axes[3].set_ylabel("$lnd$")

        axes[3].set_xlabel("step number")

        pl.show()

    def corner_graph(self, sampler, burnin):

        samples = sampler.chain[:, burnin:, :].reshape((-1, 4))

        fig = triangle.corner(
            samples,
            labels=["$m$", "$b$", "$\ln\,c$", "$\ln\,d$"])
        pl.show()


class pmodel2(pmodel):

    def sig_model(self, *args):
        # model is e*exp(-x/c) + d
        c, d, e, x = args
        return e*np.exp(-np.true_divide(x, c)) + d

    def ln_sig_model(self, *args):
        # sigma has e*exp(-x/c) + d model
        lnc, lnd, lne, x = args
        return np.exp(lne)*np.exp(-np.true_divide(x, np.exp(lnc))) + np.exp(lnd)