# Copyright Contributors to the Pyro project.
# SPDX-License-Identifier: Apache-2.0

from jax import lax, random
import jax.numpy as jnp
from jax.scipy.special import betaln, gammaln

from numpyro.distributions import constraints
from numpyro.distributions.continuous import Beta, Gamma
from numpyro.distributions.discrete import Binomial, Poisson
from numpyro.distributions.distribution import Distribution
from numpyro.distributions.util import promote_shapes, validate_sample
from numpyro.util import not_jax_tracer


class BetaBinomial(Distribution):
    r"""
    Compound distribution comprising of a beta-binomial pair. The probability of
    success (``probs`` for the :class:`~numpyro.distributions.Binomial` distribution)
    is unknown and randomly drawn from a :class:`~numpyro.distributions.Beta` distribution
    prior to a certain number of Bernoulli trials given by ``total_count``.

    :param numpy.ndarray concentration1: 1st concentration parameter (alpha) for the
        Beta distribution.
    :param numpy.ndarray concentration0: 2nd concentration parameter (beta) for the
        Beta distribution.
    :param numpy.ndarray total_count: number of Bernoulli trials.
    """
    arg_constraints = {'concentration1': constraints.positive, 'concentration0': constraints.positive,
                       'total_count': constraints.nonnegative_integer}
    has_enumerate_support = True
    is_discrete = True

    def __init__(self, concentration1, concentration0, total_count=1, validate_args=None):
        batch_shape = lax.broadcast_shapes(jnp.shape(concentration1), jnp.shape(concentration0),
                                           jnp.shape(total_count))
        self.concentration1 = jnp.broadcast_to(concentration1, batch_shape)
        self.concentration0 = jnp.broadcast_to(concentration0, batch_shape)
        self.total_count, = promote_shapes(total_count, shape=batch_shape)
        self._beta = Beta(self.concentration1, self.concentration0)
        super(BetaBinomial, self).__init__(batch_shape, validate_args=validate_args)

    def sample(self, key, sample_shape=()):
        key_beta, key_binom = random.split(key)
        probs = self._beta.sample(key_beta, sample_shape)
        return Binomial(self.total_count, probs).sample(key_binom)

    @validate_sample
    def log_prob(self, value):
        log_factorial_n = gammaln(self.total_count + 1)
        log_factorial_k = gammaln(value + 1)
        log_factorial_nmk = gammaln(self.total_count - value + 1)
        return (log_factorial_n - log_factorial_k - log_factorial_nmk +
                betaln(value + self.concentration1, self.total_count - value + self.concentration0) -
                betaln(self.concentration0, self.concentration1))

    @property
    def mean(self):
        return self._beta.mean * self.total_count

    @property
    def variance(self):
        return self._beta.variance * self.total_count * (self.concentration0 + self.concentration1 + self.total_count)

    @property
    def support(self):
        return constraints.integer_interval(0, self.total_count)

    def enumerate_support(self, expand=True):
        total_count = jnp.amax(self.total_count)
        if not_jax_tracer(total_count):
            # NB: the error can't be raised if inhomogeneous issue happens when tracing
            if jnp.amin(self.total_count) != total_count:
                raise NotImplementedError("Inhomogeneous total count not supported"
                                          " by `enumerate_support`.")
        values = jnp.arange(total_count + 1).reshape((-1,) + (1,) * len(self.batch_shape))
        if expand:
            values = jnp.broadcast_to(values, values.shape[:1] + self.batch_shape)
        return values


class GammaPoisson(Distribution):
    r"""
    Compound distribution comprising of a gamma-poisson pair, also referred to as
    a gamma-poisson mixture. The ``rate`` parameter for the
    :class:`~numpyro.distributions.Poisson` distribution is unknown and randomly
    drawn from a :class:`~numpyro.distributions.Gamma` distribution.

    :param numpy.ndarray concentration: shape parameter (alpha) of the Gamma distribution.
    :param numpy.ndarray rate: rate parameter (beta) for the Gamma distribution.
    """
    arg_constraints = {'concentration': constraints.positive, 'rate': constraints.positive}
    support = constraints.nonnegative_integer
    is_discrete = True

    def __init__(self, concentration, rate=1., validate_args=None):
        self._gamma = Gamma(concentration, rate)
        self.concentration = self._gamma.concentration
        self.rate = self._gamma.rate
        super(GammaPoisson, self).__init__(self._gamma.batch_shape, validate_args=validate_args)

    def sample(self, key, sample_shape=()):
        key_gamma, key_poisson = random.split(key)
        rate = self._gamma.sample(key_gamma, sample_shape)
        return Poisson(rate).sample(key_poisson)

    @validate_sample
    def log_prob(self, value):
        post_value = self.concentration + value
        return -betaln(self.concentration, value + 1) - jnp.log(post_value) + \
            self.concentration * jnp.log(self.rate) - post_value * jnp.log1p(self.rate)

    @property
    def mean(self):
        return self.concentration / self.rate

    @property
    def variance(self):
        return self.concentration / jnp.square(self.rate) * (1 + self.rate)
