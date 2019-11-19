"""POD-NN modeling for 1D Shekel Equation."""

import sys
import json
import os
import numpy as np

sys.path.append(os.path.join("..", ".."))
from podnn.podnnmodel import PodnnModel
from podnn.metrics import error_podnn
from podnn.mesh import create_linear_mesh

from datagen import u, generate_test_dataset
from plots import plot_results


def main(hp, gen_test=False, use_cached_dataset=False,
         no_plot=False):
    """Full example to run POD-NN on 1d_shekel."""

    if gen_test:
        generate_test_dataset()

    if not use_cached_dataset:
        # Create linear space mesh
        x_mesh = create_linear_mesh(hp["x_min"], hp["x_max"], hp["n_x"])
        np.save(os.path.join("cache", "x_mesh.npy"), x_mesh)
    else:
        x_mesh = np.load(os.path.join("cache", "x_mesh.npy"))

    # Extend the class and init the model
    class Burgers2PodnnModel(PodnnModel):
        def u(self, X, t, mu):
            return u(X, t, mu)
    model = Burgers2PodnnModel("cache", hp["n_v"], x_mesh, hp["n_t"])

    # Generate the dataset from the mesh and params
    X_v_train, v_train, \
        X_v_val, v_val, \
        U_val = model.generate_dataset(hp["mu_min"], hp["mu_max"],
                                       hp["n_s"],
                                       hp["train_val_ratio"],
                                       hp["eps"],
                                       use_cache=use_cached_dataset)

    # Create the model and train
    def error_val():
        v_val_pred = model.predict_v(X_v_val)
        # return mse(v_val, v_val_pred)
        return error_podnn(v_val, v_val_pred)
    model.train(X_v_train, v_train, error_val, hp["h_layers"],
                hp["epochs"], hp["lr"], hp["lambda"]) 

    # Predict and restruct
    U_pred = model.predict(X_v_val)

    # Plot against test and save
    return plot_results(U_val, U_pred, hp, no_plot)


if __name__ == "__main__":
    # Custom hyperparameters as command-line arg
    if len(sys.argv) > 1:
        with open(sys.argv[1]) as HPFile:
            HP = json.load(HPFile)
    # Default ones
    else:
        from hyperparams import HP

    main(HP, gen_test=False, use_cached_dataset=False)
    # main(HP, gen_test=False, use_cached_dataset=True)
