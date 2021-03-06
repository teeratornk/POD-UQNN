"""Metrics functions to output results."""
import numpy as np
import tensorflow as tf
from numpy.linalg import norm


def mse(v, v_pred):
    return tf.reduce_mean(tf.square(v - v_pred))


def re(U, U_pred):
    """Return relative error, inputs should be (n_h,)."""
    return norm(U - U_pred) / norm(U)


def re_max(U, U_pred):
    """Return relative error, inputs should be (n_h,)."""
    return norm(U - U_pred) / max(norm(U), norm(U_pred))


def re_s(U, U_pred, div_max=False):
    """Return relative error, inputs should be (n_h,)."""
    n_s = U.shape[1]
    err = 0.
    for i in range(n_s):
        if div_max:
            err += re_max(U[:, i], U_pred[:, i])
        else:
            err += re(U[:, i], U_pred[:, i])
    return err / n_s


def re_mean_std(U_s, U_pred_s):
    """Define the relative error metric."""
    U_pred_mean, U_mean = np.mean(U_pred_s, axis=-1), np.mean(U_s, axis=-1)
    U_pred_std, U_std = np.std(U_pred_s, axis=-1), np.std(U_s, axis=-1)
    err_mean = re(U_mean, U_pred_mean)
    err_std = re(U_std, U_pred_std)
    return err_mean, err_std


def rel_error_mean(U, U_pred):
    per_element_error = np.abs(U - U_pred) / np.maximum(np.abs(U), np.abs(U_pred))
    return np.nanmean(per_element_error)
