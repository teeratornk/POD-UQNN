"""POD-NN modeling for the 1D time-dep Burgers Equation."""

import sys
import os
import yaml
import numpy as np

sys.path.append(os.path.join("..", ".."))
from podnn.podnnmodel import PodnnModel
from podnn.mesh import create_linear_mesh
from podnn.plotting import genresultdir

from genhifi import u, generate_test_dataset
from plot import plot_results


def main(resdir, hp, gen_test=False, use_cached_dataset=False,
         no_plot=False):
    """Full example to run POD-NN on 1dt_burger."""

    if gen_test:
        generate_test_dataset()

    if not use_cached_dataset:
        # Create linear space mesh
        x_mesh = create_linear_mesh(hp["x_min"], hp["x_max"], hp["n_x"])
        np.save(os.path.join(resdir, "x_mesh.npy"), x_mesh)
    else:
        x_mesh = np.load(os.path.join(resdir, "x_mesh.npy"))

    # Init the model
    model = PodnnModel(resdir, hp["n_v"], x_mesh, hp["n_t"])

    # Generate the dataset from the mesh and params
    X_v_train, v_train, U, \
        X_v_test, U_test = \
            model.generate_dataset(u, hp["mu_min"], hp["mu_max"],
                                   hp["n_s"],
                                   hp["train_val_test"],
                                   eps=hp["eps"], n_L=hp["n_L"],
                                   eps_init=hp["eps_init"],
                                   x_noise=hp["x_noise"],
                                   t_min=hp["t_min"], t_max=hp["t_max"],
                                   use_cache=use_cached_dataset)

    # Train
    model.initNN(hp["h_layers"], hp["h_layers_t"],
                 hp["lr"], hp["lambda"], hp["beta"],
                 hp["k1"], hp["k2"], hp["norm"])
    train_res = model.train(X_v_train, v_train, hp["epochs"],
                            hp["train_val_test"], freq=hp["log_frequency"])

    # Predict and restruct
    v_pred, v_pred_sig = model.predict_v(X_v_test)
    U_pred = model.V.dot(v_pred.T)
    U_pred = model.restruct(U_pred)
    U_test = model.restruct(U_test)

    # Sample the new model to generate a HiFi prediction
    n_s_hifi = hp["n_s_hifi"]
    print("Sampling {n_s_hifi} parameters")
    X_v_test_hifi = model.generate_hifi_inputs(n_s_hifi, hp["mu_min"], hp["mu_max"],
                                               hp["t_min"], hp["t_max"])
    print("Predicting the {n_s_hifi} corresponding solutions")
    U_pred_hifi, U_pred_hifi_sig = model.predict_var(X_v_test_hifi)
    U_pred_hifi = model.restruct(U_pred_hifi)
    U_pred_hifi_sig = model.restruct(U_pred_hifi_sig)
    U_pred_hifi_mean = (model.restruct(U_pred_hifi.mean(-1), no_s=True),
                        model.restruct(U_pred_hifi_sig.mean(-1), no_s=True))
    U_pred_hifi_std = (model.restruct(U_pred_hifi.std(-1), no_s=True),
                       model.restruct(U_pred_hifi_sig.std(-1), no_s=True))

    # Plot against test and save
    return plot_results(U_test, U_pred, U_pred_hifi_mean, U_pred_hifi_std,
                        resdir, train_res, hp, no_plot)

if __name__ == "__main__":
    # Custom hyperparameters as command-line arg
    if len(sys.argv) > 1:
        with open(sys.argv[1]) as HPFile:
            HP = yaml.load(HPFile)
    # Default ones
    else:
        from hyperparams import HP

    resdir = genresultdir()
    main(resdir, HP, gen_test=False, use_cached_dataset=False)
