"""
Unit tests for optimizers.
"""
import numpy as np
import pytest
from numpy.linalg import norm
from sklearn.base import BaseEstimator
from sklearn.exceptions import ConvergenceWarning
from sklearn.exceptions import NotFittedError
from sklearn.linear_model import ElasticNet
from sklearn.linear_model import Lasso
from sklearn.utils.validation import check_is_fitted

from pysindy.optimizers import SINDyOptimizer
from pysindy.optimizers import SR3
from pysindy.optimizers import STLSQ
from pysindy.utils import supports_multiple_targets


class DummyLinearModel(BaseEstimator):
    # Does not natively support multiple targets
    def fit(self, x, y):
        self.coef_ = np.ones(x.shape[1])
        self.intercept_ = 0
        return self

    def predict(self, x):
        return x


class DummyEmptyModel(BaseEstimator):
    # Does not have fit or predict methods
    def __init__(self):
        self.fit_intercept = False
        self.normalize = False


class DummyModelNoCoef(BaseEstimator):
    # Does not set the coef_ attribute
    def fit(self, x, y):
        self.intercept_ = 0
        return self

    def predict(self, x):
        return x


@pytest.mark.parametrize(
    "cls, support",
    [(Lasso, True), (STLSQ, True), (SR3, True), (DummyLinearModel, False)],
)
def test_supports_multiple_targets(cls, support):
    assert supports_multiple_targets(cls()) == support


@pytest.fixture(params=["data_derivative_1d", "data_derivative_2d"])
def data(request):
    return request.getfixturevalue(request.param)


@pytest.mark.parametrize(
    "optimizer",
    [
        STLSQ(),
        SR3(),
        Lasso(fit_intercept=False),
        ElasticNet(fit_intercept=False),
        DummyLinearModel(),
    ],
)
def test_fit(data, optimizer):
    x, x_dot = data
    if len(x.shape) == 1:
        x = x.reshape(-1, 1)
    opt = SINDyOptimizer(optimizer, unbias=False)
    opt.fit(x, x_dot)

    check_is_fitted(opt)
    assert opt.complexity >= 0
    if len(x_dot.shape) > 1:
        assert opt.coef_.shape == (x.shape[1], x_dot.shape[1])
    else:
        assert opt.coef_.shape == (1, x.shape[1])


@pytest.mark.parametrize(
    "optimizer",
    [STLSQ(), SR3()],
)
def test_not_fitted(optimizer):
    with pytest.raises(NotFittedError):
        optimizer.predict(np.ones((1, 3)))


@pytest.mark.parametrize("optimizer", [STLSQ(), SR3()])
def test_complexity_not_fitted(optimizer, data_derivative_2d):
    with pytest.raises(NotFittedError):
        optimizer.complexity

    x, _ = data_derivative_2d
    optimizer.fit(x, x)
    assert optimizer.complexity > 0


@pytest.mark.parametrize(
    "kwargs", [{"normalize": True}, {"fit_intercept": True}, {"copy_X": False}]
)
def test_alternate_parameters(data_derivative_1d, kwargs):
    x, x_dot = data_derivative_1d
    x = x.reshape(-1, 1)

    model = STLSQ(**kwargs)
    model.fit(x, x_dot)
    model.fit(x, x_dot, sample_weight=x[:, 0])

    check_is_fitted(model)


def test_bad_parameters():
    with pytest.raises(ValueError):
        STLSQ(threshold=-1)

    with pytest.raises(ValueError):
        STLSQ(alpha=-1)

    with pytest.raises(ValueError):
        STLSQ(max_iter=0)

    with pytest.raises(ValueError):
        SR3(threshold=-1)

    with pytest.raises(ValueError):
        SR3(nu=0)

    with pytest.raises(ValueError):
        SR3(tol=0)

    with pytest.raises(NotImplementedError):
        SR3(thresholder="l2")

    with pytest.raises(ValueError):
        SR3(max_iter=0)

    with pytest.raises(ValueError):
        SR3(trimming_fraction=-1)

    with pytest.raises(ValueError):
        SR3(trimming_fraction=2)


def test_bad_optimizers(data_derivative_1d):
    x, x_dot = data_derivative_1d
    x = x.reshape(-1, 1)

    with pytest.raises(AttributeError):
        opt = SINDyOptimizer(DummyEmptyModel())

    with pytest.raises(AttributeError):
        opt = SINDyOptimizer(DummyModelNoCoef())
        opt.fit(x, x_dot)


# The different capitalizations are intentional;
# I want to make sure different versions are recognized
@pytest.mark.parametrize("thresholder", ["L0", "l1", "CAD"])
def test_sr3_prox_functions(data_derivative_1d, thresholder):
    x, x_dot = data_derivative_1d
    x = x.reshape(-1, 1)
    model = SR3(thresholder=thresholder)
    model.fit(x, x_dot)
    check_is_fitted(model)


def test_unbias(data_derivative_1d):
    x, x_dot = data_derivative_1d
    x = x.reshape(-1, 1)

    optimizer_biased = SINDyOptimizer(
        STLSQ(threshold=0.01, alpha=0.1, max_iter=1), unbias=False
    )
    optimizer_biased.fit(x, x_dot)

    optimizer_unbiased = SINDyOptimizer(
        STLSQ(threshold=0.01, alpha=0.1, max_iter=1), unbias=True
    )
    optimizer_unbiased.fit(x, x_dot)

    assert (
        norm(optimizer_biased.coef_ - optimizer_unbiased.coef_)
        / norm(optimizer_unbiased.coef_)
        > 1e-9
    )


def test_unbias_external(data_derivative_1d):
    x, x_dot = data_derivative_1d
    x = x.reshape(-1, 1)

    optimizer_biased = SINDyOptimizer(
        Lasso(alpha=0.1, fit_intercept=False, max_iter=1), unbias=False
    )
    optimizer_biased.fit(x, x_dot)

    optimizer_unbiased = SINDyOptimizer(
        Lasso(alpha=0.1, fit_intercept=False, max_iter=1), unbias=True
    )
    optimizer_unbiased.fit(x, x_dot)

    assert (
        norm(optimizer_biased.coef_ - optimizer_unbiased.coef_)
        / (norm(optimizer_unbiased.coef_) + 1e-5)
        > 1e-9
    )


def test_sr3_trimming(data_linear_oscillator_corrupted):
    X, X_dot, trimming_array = data_linear_oscillator_corrupted

    optimizer_without_trimming = SINDyOptimizer(SR3(), unbias=False)
    optimizer_without_trimming.fit(X, X_dot)

    optimizer_trimming = SINDyOptimizer(SR3(trimming_fraction=0.15), unbias=False)
    optimizer_trimming.fit(X, X_dot)

    # Check that trimming found the right samples to remove
    np.testing.assert_array_equal(
        optimizer_trimming.optimizer.trimming_array, trimming_array
    )

    # Check that the coefficients found by the optimizer with trimming are closer to
    # the true coefficients than the coefficients found by the optimizer without
    # trimming
    true_coef = np.array([[-2.0, 0.0], [0.0, 1.0]])
    assert norm(true_coef - optimizer_trimming.coef_) < norm(
        true_coef - optimizer_without_trimming.coef_
    )


def test_sr3_disable_trimming(data_linear_oscillator_corrupted):
    x, x_dot, _ = data_linear_oscillator_corrupted

    model_plain = SR3()
    model_plain.fit(x, x_dot)

    model_trimming = SR3(trimming_fraction=0.5)
    model_trimming.disable_trimming()
    model_trimming.fit(x, x_dot)

    np.testing.assert_allclose(model_plain.coef_, model_trimming.coef_)


def test_sr3_enable_trimming(data_linear_oscillator_corrupted):
    x, x_dot, _ = data_linear_oscillator_corrupted

    model_plain = SR3()
    model_plain.enable_trimming(trimming_fraction=0.5)
    model_plain.fit(x, x_dot)

    model_trimming = SR3(trimming_fraction=0.5)
    model_trimming.fit(x, x_dot)

    np.testing.assert_allclose(model_plain.coef_, model_trimming.coef_)


def test_sr3_warn(data_linear_oscillator_corrupted):
    x, x_dot, _ = data_linear_oscillator_corrupted
    model = SR3(max_iter=1, tol=1e-10)

    with pytest.warns(ConvergenceWarning):
        model.fit(x, x_dot)
