"""Default hyperparameters for 2D inviscid Shallow Water Equations."""

from poduqnn.varneuralnetwork import NORM_MEANSTD, NORM_CENTER, NORM_NONE


HP = {}
HP["mesh_idx"] = ["eta"]
HP["mu_idx"] = [1]
# Dimension of u(x, t, mu)
HP["n_v"] = len(HP["mesh_idx"])
# Time
HP["n_t"] = 101
HP["d_t"] = 0.3
HP["t_min"] = 0.
HP["t_max"] = 100.
# Snapshots count
HP["n_s"] = 98
HP["n_s_tst"] = 2
# POD stopping param
HP["eps"] = 1e-6
HP["eps_init"] = 1e-6
HP["n_L"] = 0
# Train/val split
HP["train_val"] = (.8, .2)
# Deep NN hidden layers topology
HP["h_layers"] = [128, 128, 128]
# Setting up TF SGD-based optimizer
HP["n_M"] = 3
HP["epochs"] = 200000
HP["lr"] = 0.001
HP["lambda"] = 0.001
HP["adv_eps"] = 0.001
HP["soft_0"] = 0.01
HP["norm"] = NORM_MEANSTD
# Frequency of the logger
HP["log_frequency"] = 1000
