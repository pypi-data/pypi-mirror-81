# Copyright 2019 Toyota Research Institute. All rights reserved.
"""
Module and scripts for training and predicting with models,
given a matching descriptor set.

Usage:
    run_model [INPUT_JSON] [--fit]

Options:
    -h --help        Show this screen
    --fit            <true_or_false>  [default: False] Fit model
    --version        Show version


The `run_model` script will generate a model and create predictions
based on the features previously generated by the featurize module.
It stores its outputs in `/data-share/predictions/`

The input json must contain the following fields
* `file_list` - list of files corresponding to model features

The output json will contain the following fields
* `file_list` - list of files corresponding to model predictions

Example:
$ run_model '{"file_list": ["/data-share/features/FastCharge_2_CH29_full_model_features.json"]}'
{
    "file_list": ["/data-share/predictions/FastCharge_2_CH29_full_model_predictions.json"]
}
"""
from __future__ import division
import os
import json
import pandas as pd
import numpy as np
import datetime
from docopt import docopt
from monty.json import MSONable
from monty.serialization import loadfn, dumpfn
from beep.collate import scrub_underscore_suffix, add_suffix_to_filename
from sklearn.linear_model import (
    Lasso,
    LassoCV,
    RidgeCV,
    Ridge,
    ElasticNetCV,
    ElasticNet,
    MultiTaskElasticNet,
    MultiTaskElasticNetCV,
)
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from beep.utils import KinesisEvents
from beep import MODEL_DIR, logger, __version__

s = {"service": "DataAnalyzer"}
# Projects that have cycling profiles compatible with the FastCharge model should be included in the list below
DEFAULT_MODEL_PROJECTS = [
    "FastCharge",
    "ClosedLoopOED",
    "2017-05-12",
    "2017-06-30",
    "2018-04-12",
]
assert all("_" not in name for name in DEFAULT_MODEL_PROJECTS)


class DegradationModel(MSONable):
    """
    Object corresponding to prediction model.

    Attributes:
        name (str): instance name.
        model (dict): model specific parameters.
    """

    def __init__(self, name, model):
        """

        Args:
            name (str):
            model (dict):
        """
        self.name = name
        self.model = model

    @classmethod
    def from_name(cls, model_name="full_model"):
        """
        Args:
            model_name (str): name of method for featurization.
        """
        if model_name == "full_model":
            return cls.init_full_model()
        else:
            raise NotImplementedError

    @classmethod
    def from_serialized_model(
        cls, model_dir="data-share/model/", serialized_model=None
    ):
        """
        Class method to invoke from serialized model

        Args:
            model_dir (str): path to model directory
            serialized_model (str): name of model

        Returns:
            (DegradationModel): model object from stored model

        """
        if serialized_model is None:
            raise ValueError("Please specify model name stored in {}".format(model_dir))
        elif not os.path.exists(os.path.join(model_dir, serialized_model)):
            raise ValueError("Path invalid")
        else:
            trained_model = loadfn(os.path.join(model_dir, serialized_model))

        return cls(name=serialized_model.split(".")[0], model=trained_model)

    @classmethod
    def init_full_model(cls):
        """
        Predict using model coefficients generated by fitting to
        D3Batt early prediction manuscript data using BEEP codebase.

        Returns:
            DegradationModel
        """
        coefs = np.array(
            [
                77.64331966,
                -3.38357566,
                0.0,
                0.0,
                9.48943144,
                -0.0,
                -0.0,
                -0.0,
                -0.0,
                0.0,
                -172.1890952,
                -61.6947121,
                5.22729452,
                0.0,
                0.0,
                0.0,
                0.0,
                -31.84889315,
                -0.0,
                -0.0,
            ]
        )

        mu = np.array(
            [
                1.06823975e00,
                7.73847312e-01,
                1.07329200e00,
                1.13981637e06,
                6.34888946e02,
                -1.36155073e00,
                -1.72133649e00,
                -3.47084255e00,
                -1.22713574e00,
                2.63323211e-01,
                -1.47651181e00,
                3.73629665e01,
                2.95566653e01,
                -1.36504373e-05,
                1.07594232e00,
                -6.87024033e-05,
                1.08010237e00,
                1.67499372e-02,
                1.73228530e-02,
                -3.04463017e-04,
            ]
        )

        sigma = np.array(
            [
                1.41520865e-02,
                1.95217699e-01,
                1.59416725e-02,
                7.23228725e06,
                5.65537087e01,
                2.58001513e-01,
                2.70289386e-01,
                4.51079117e-01,
                6.71019154e-01,
                2.05683149e-01,
                2.25143929e-01,
                1.71008400e00,
                5.69541083e-01,
                5.98941337e-05,
                1.44721412e-02,
                6.14265444e-05,
                1.48826794e-02,
                6.54248192e-04,
                7.19974520e-04,
                5.86172005e-04,
            ]
        )

        model = {"coef_": coefs}
        name = "full_model"

        date_string = datetime.datetime.now()

        trained_model = {
            "model_type": "linear",
            "model": model,
            "confidence_bounds": 0.1,
            "regularization_type": "elasticnet",
            "timestamp": date_string.isoformat(),
            "dataset_id": None,
            "hyperparameters": {},
            "featureset_name": "full_model",
            "predicted_quantity": "cycle",
            "mu": np.array(mu),
            "sigma": np.array(sigma),
        }

        return cls(name, trained_model)

    def serialize(self, processed_dir="data-share/model"):
        """

        Args:
            processed_dir (dict): target directory.

        Returns:

        """
        if not os.path.exists(processed_dir):
            os.makedirs(processed_dir)
        dumpfn(self.model, os.path.join(processed_dir, self.name + ".model"))

    def as_dict(self):
        """
        Method for dictionary serialization.

        Returns:
            dict: corresponding to dictionary for serialization.

        """

        return {
            "@module": self.__class__.__module__,
            "@class": self.__class__.__name__,
            "name": self.name,
            "model": self.model,
        }

    @classmethod
    def from_dict(cls, d):
        """
        MSONable deserialization method.

        Args:
            d (dict):

        Returns:
            beep.run_model.DegradationModel:
        """
        return cls(**d)

    @classmethod
    def train(
        cls,
        list_of_featurized_jsons,
        dataset_id=None,
        model_type="linear",
        regularization_type="elasticnet",
        model_name="custom_model",
        hyperparameters=None,
    ):
        """
        Class method to accept a json string of featurized cycler run files
        and output model coefficients.  Trained models are serialized as
        a dictionary and pushed into a local file.

        Model coefficients are initialized after training.

        Args:
            list_of_featurized_jsons (str): json string of featurized cycler run files.
            dataset_id (str): unique_id corresponding to a list of run_ids that are used
                for model training.
            model_type (str): linear or random_forest.
            regularization_type (str): lasso or ridge or elasticnet
                (cv estimator chosen by default).
            model_name (str): custom name for the model.
            hyperparameters (dict): dictionary with the following attributes:
                random_state, test_size, k_fold, tol, l1_ratio.

        """
        if hyperparameters is None:
            hyperparameters = {
                "random_state": 2,
                "test_size": 0.3,
                "k_fold": 5,
                "tol": 0.0001,
                "l1_ratio": [0.1, 0.5, 0.7, 0.9, 0.95, 1],
                "max_iter": 1000000,
            }

        X, y, featureset_name, predicted_quantity = assemble_predictors(
            list_of_featurized_jsons
        )
        if model_type.lower() == "random_forest":
            (
                model,
                mu,
                s,
                relative_prediction_error,
                Rsquare,
                hyperparameters_optimized,
            ) = train_linear_model(X, y, **hyperparameters)
        elif model_type.lower() == "linear":
            (
                model,
                mu,
                s,
                relative_prediction_error,
                Rsquare,
                hyperparameters_optimized,
            ) = train_linear_model(X, y, **hyperparameters)
        else:
            raise NotImplementedError

        # Book-keeping
        date_string = datetime.datetime.now()
        trained_model = {
            "model_type": model_type.lower(),
            "model": model.__dict__,
            "confidence_bounds": relative_prediction_error,
            "Rsquare": Rsquare,
            "regularization_type": regularization_type,
            "timestamp": date_string.isoformat(),
            "dataset_id": dataset_id,
            "hyperparameters": hyperparameters_optimized,
            "featureset_name": featureset_name,
            "predicted_quantity": predicted_quantity,
        }
        if model_type.lower() == "linear":
            trained_model["mu"] = np.array(mu)
            trained_model["sigma"] = np.array(s)

        return cls(name=model_name, model=trained_model)

    def predict(self, features):
        """
        Args:
            features (beep.featurize.DegradationPredictor): features in
                DegradationPredictor format.

        Returns:
            prediction (float): float corresponding to predicted value.
        """
        if self.model["model_type"].lower() == "linear":
            X = (features.X - self.model["mu"]) / self.model["sigma"]
        else:
            X = features.X
        coefs = self.model["model"]["coef_"]
        prediction = (
            np.nansum((np.array(X) * coefs), axis=1) + self.model["model"]["intercept_"]
        )
        if prediction.ndim == 2:
            prediction = prediction.reshape((prediction.shape[1],))
        return prediction

    def prediction_to_dict(self, prediction, nominal_capacity=1.1):
        """
        Args:
            prediction (float or [float]): float or list of floats
                corresponding to predictions.
            nominal_capacity (float): Nominal capacity of the cell.

        Returns:
            dict: dictionary with predictions, error bars and model name.

        """
        output_dict = {}
        if len(prediction) == 1:
            output_dict["discharge_capacity"] = nominal_capacity * 0.8
            output_dict["fractional_error"] = self.model["confidence_bounds"]
        else:
            output_dict["discharge_capacity"] = (
                np.around(np.arange(0.98, 0.78, -0.03), 2) * nominal_capacity
            )

            # For now the API is only serving up a single value as the confidence interval
            # the model is producing MSE values for each of the prediction points, so the correct value over
            # the full set of prediction point should be the average of the MSE for each of the points
            # In the future the fractional errors can be an array, once the API and UI are ready for that
            # Taking the average is equivalent to
            output_dict["fractional_error"] = np.asarray(
                [np.average(self.model["confidence_bounds"])]
            )

        output_dict["cycle_number"] = prediction
        output_dict["model_type"] = self.model["model_type"]
        output_dict["predicted_quantity"] = self.model["predicted_quantity"]

        # Ideally, we will have a model_id, but using model_name for now.
        output_dict["model_name"] = self.name
        return output_dict


def train_linear_model(
    X,
    y,
    random_state=1,
    test_size=0.2,
    regularization_type="elasticnet",
    k_fold=5,
    max_iter=1000000,
    tol=0.0001,
    l1_ratio=None,
):
    """
    Function to train linear model with regularization and cross-validation.

    Args:
        X (pandas.DataFrame): dataframe of descriptors.
        y (pandas.DataFrame): dataframe of cycle lifetimes.
        random_state (int): seed for train/test split.
        test_size (float): proportion of the dataset reserved for model evaluation.
        regularization_type (str): lasso or ridge or elastic-net (with cv).
        k_fold (int): k in k-fold cross-validation.
        max_iter (int): maximum number of iterations for model fitting.
        tol (float): tolerance for optimization.
        l1_ratio ([float]): list of lasso to ridge ratios for elasticnet.

    Returns:
        sklearn.linear_model.LinearModel: fitted model.
        mu (float): Mean value of descriptors used in training.
        s (float): Std dev of descriptors used in training.

    """
    if l1_ratio is None:
        l1_ratio = [0.1, 0.5, 0.7, 0.9, 0.95, 1]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )

    # Standardize (training) data after train/test split
    mu = np.mean(X_train, axis=0)
    s = np.std(X_train, axis=0)
    X_scaled = (X_train - mu) / s
    hyperparameters = {
        "random_state": random_state,
        "test_size": test_size,
        "k_fold": k_fold,
        "tol": tol,
        "max_iter": max_iter,
    }
    if regularization_type == "lasso" and y.shape[1] == 1:
        lassocv = LassoCV(
            fit_intercept=True, alphas=None, tol=tol, cv=k_fold, max_iter=max_iter
        )
        lassocv.fit(X_scaled, y_train.values.ravel())
        # Set optimal alpha and refit model
        alpha_opt = lassocv.alpha_
        linear_model = Lasso(fit_intercept=True, alpha=alpha_opt, max_iter=max_iter)
        linear_model.fit(X_scaled, y_train.values)
        hyperparameters["l1_ratio"] = 1

    elif regularization_type == "ridge" and y.shape[1] == 1:
        ridgecv = RidgeCV(fit_intercept=True, alphas=None, cv=k_fold)
        ridgecv.fit(X_scaled, y_train.values.ravel())
        # Set optimal alpha and refit model
        alpha_opt = ridgecv.alpha_
        linear_model = Ridge(fit_intercept=True, alpha=alpha_opt)
        linear_model.fit(X_scaled, y_train)
        hyperparameters["l1_ratio"] = 0

    elif regularization_type == "elasticnet" and y.shape[1] == 1:
        elasticnetcv = ElasticNetCV(
            fit_intercept=True,
            normalize=False,
            alphas=None,
            cv=k_fold,
            l1_ratio=l1_ratio,
            max_iter=max_iter,
        )
        elasticnetcv.fit(X_scaled, y_train.values.ravel())

        # Set optimal alpha and l1_ratio. Refit model
        alpha_opt = elasticnetcv.alpha_
        l1_ratio_opt = elasticnetcv.l1_ratio_
        linear_model = ElasticNet(
            fit_intercept=True,
            normalize=False,
            l1_ratio=l1_ratio_opt,
            alpha=alpha_opt,
            max_iter=max_iter,
        )
        linear_model.fit(X_scaled, y_train)
        hyperparameters["l1_ratio"] = l1_ratio_opt

    # If more than 1 outcome present, perform multitask regression
    elif regularization_type == "elasticnet" and y.shape[1] > 1:
        multi_elasticnet_CV = MultiTaskElasticNetCV(
            fit_intercept=True,
            cv=k_fold,
            normalize=False,
            l1_ratio=l1_ratio,
            max_iter=max_iter,
        )
        multi_elasticnet_CV.fit(X_scaled, y_train)
        # Set optimal alpha and l1_ratio. Refit model
        alpha_opt = multi_elasticnet_CV.alpha_
        l1_ratio_opt = multi_elasticnet_CV.l1_ratio_
        linear_model = MultiTaskElasticNet(
            fit_intercept=True, normalize=False, max_iter=max_iter
        )
        linear_model.set_params(alpha=alpha_opt, l1_ratio=l1_ratio_opt)
        linear_model.fit(X_scaled, y_train)
        hyperparameters["l1_ratio"] = l1_ratio_opt
    else:
        raise NotImplementedError

    y_pred = linear_model.predict((X_test - mu) / s)
    Rsq = linear_model.score((X_test - mu) / s, y_test)
    # Compute 95% confidence interval
    # Multioutput = 'raw_values' provides prediction error per output
    pred_actual_ratio = [x / y for x, y in zip(y_pred, np.array(y_test))]
    relative_prediction_error = 1.96 * np.sqrt(
        mean_squared_error(
            np.ones(y_pred.shape), pred_actual_ratio, multioutput="raw_values"
        )
        / y_pred.shape[0]
    )
    hyperparameters["alpha"] = alpha_opt
    return linear_model, mu, s, relative_prediction_error, Rsq, hyperparameters


def assemble_predictors(file_list_json):
    """
    Method to assemble predictor dataframe from a json string of paths to feature vectors.

    Args:
        file_list_json (str): json string corresponding to a dictionary
            with a file_list attribute.

    Returns:
        pandas.DataFrame: Dataframe of size (n,m). n = number of cells, m = number of features.
        pandas.Series: Series of length n.
    """
    if file_list_json.endswith(".json"):
        file_list_data = loadfn(file_list_json)
    else:
        file_list_data = json.loads(file_list_json)

    X = pd.DataFrame()
    y = pd.DataFrame()

    for path in file_list_data["file_list"]:
        features = loadfn(path)
        X = X.append(features.X)
        if isinstance(features.y, (int, float)):
            y = y.append(pd.DataFrame([features.y]))
        else:
            y = y.append(pd.DataFrame(features.y))

    # Most NaNs should be handled at featurization, but if any crop-up during
    # model fitting, impute missing values with median of that feature.
    X = X.apply(lambda x: x.fillna(x.median()), axis=0)
    y = y.apply(lambda x: x.fillna(x.median()), axis=0)

    return X, y, features.name, features.predicted_quantity


def add_file_prefix_to_path(path, prefix):
    """
    Helper function to add file prefix to path

    Args:
        path (str): full path to file
        prefix (str): prefix for file

    Returns:
        str: path with prefix appended to filename

    """
    split_path = list(os.path.split(path))
    split_path[-1] = prefix + split_path[-1]
    return os.path.join(*split_path)


def get_project_name_from_list(file_list):
    """
    Helper function to get the project name from a list of file names

    Args:
        file_list (list): List of full file names (paths).
    Returns:
        str: Name of the project.
    """
    names_list = []
    for file in file_list:
        _, file_tail = os.path.split(file)
        names_list.append(file_tail.split("_")[0])
    project_name = max(set(names_list), key=names_list.count)

    return project_name


def process_file_list_from_json(
    file_list_json,
    model_dir="/data-share/models/",
    processed_dir="data-share/predictions/",
    hyperparameters=None,
    model_name=None,
    predict_only=True,
):
    """
    Function to take a json file containing featurized json locations,
    train a new model if necessary, write files containing predictions into a
    predetermined directory, and return a jsonable dict of prediction file locations

    Args:
        file_list_json (str): json string or json filename corresponding
            to a dictionary with a file_list attribute,
            if this string ends with ".json", a json file is assumed
            and loaded, otherwise interpreted as a json string
        model_dir (str): location where models are serialized and stored
        processed_dir (str): location for processed cycler run output files
            to be placed
        hyperparameters (dict): dictionary of hyperparameters to optimize/use for training
        model_name (str): name of feature generation method
        predict_only (bool):

    Returns:
        str: json string of feature files (with key "feature_file_list").

    """
    # Get file list and validity from json, if ends with .json,
    # assume it's a file, if not assume it's a json string
    if file_list_json.endswith(".json"):
        file_list_data = loadfn(file_list_json)
    else:
        file_list_data = json.loads(file_list_json)

    # Setup Events
    events = KinesisEvents(service="DataAnalyzer", mode=file_list_data["mode"])

    # Add BEEP_PROCESSING_DIR to processed_dir
    processed_dir = os.path.join(
        os.environ.get("BEEP_PROCESSING_DIR", "/"), processed_dir
    )
    if not os.path.exists(processed_dir):
        os.makedirs(processed_dir)

    file_list = file_list_data["file_list"]
    run_ids = file_list_data["run_list"]
    processed_run_list = []
    processed_result_list = []
    processed_message_list = []
    processed_paths_list = []
    project_name = get_project_name_from_list(file_list)
    if predict_only:
        features = loadfn(file_list[0])
        if model_name is None and project_name in DEFAULT_MODEL_PROJECTS:

            if features.prediction_type == "multi":
                model = DegradationModel.from_serialized_model(
                    model_dir=model_dir, serialized_model="d3batt_multi_point.model"
                )
            else:
                model = DegradationModel.from_serialized_model(
                    model_dir=model_dir, serialized_model="d3batt_single_point.model"
                )

        elif model_name is None and project_name not in DEFAULT_MODEL_PROJECTS:
            output_data = {
                "file_list": [],
                "run_list": [],
                "result_list": [],
                "message_list": [],
            }

            events.put_analyzing_event(output_data, "predicting", "error")

            # Return jsonable file list
            return json.dumps(output_data)

        else:
            model = DegradationModel.from_serialized_model(
                model_dir=model_dir, serialized_model=model_name
            )

    else:
        if hyperparameters is None:
            hyperparameters = {
                "random_state": 1,
                "test_size": 0.3,
                "k_fold": 5,
                "tol": 0.001,
                "l1_ratio": [0.1, 0.5, 0.7, 0.9, 0.95, 0.99, 1],
            }

        dataset_id = file_list_data.get("dataset_id")
        model = DegradationModel.train(
            file_list_json,
            dataset_id=dataset_id,
            model_type="linear",
            regularization_type="elasticnet",
            model_name=model_name,
            hyperparameters=hyperparameters,
        )
        logger.warning("fitting=%s dataset=%s", model.name, str(dataset_id), extra=s)

    for path, run_id in zip(file_list, run_ids):
        logger.info(
            "model=%s run_id=%s predicting=%s", model.name, str(run_id), path, extra=s
        )
        features = loadfn(path)
        prediction = model.predict(features)
        prediction_dict = model.prediction_to_dict(
            prediction, features.nominal_capacity
        )
        new_filename = os.path.basename(path)
        new_filename = scrub_underscore_suffix(new_filename)
        new_filename = add_suffix_to_filename(new_filename, "_predictions")
        processed_path = os.path.join(processed_dir, new_filename)
        processed_path = os.path.abspath(processed_path)
        dumpfn(prediction_dict, processed_path)

        # Append file loc to list to be returned
        processed_paths_list.append(processed_path)
        processed_run_list.append(run_id)
        processed_result_list.append("success")
        processed_message_list.append({"comment": "", "error": ""})

    output_data = {
        "file_list": processed_paths_list,
        "run_list": processed_run_list,
        "result_list": processed_result_list,
        "message_list": processed_message_list,
    }

    events.put_analyzing_event(output_data, "predicting", "complete")

    # Return jsonable file list
    return json.dumps(output_data)


def main():
    """
    Main function of this module, takes in arguments of an input
    and output filename corresponding to featurized run data
    and creates a predictor object output for analysis/ML processing
    """
    # Parse args and construct initial cycler run
    logger.info("starting", extra=s)
    logger.info("Running version=%s", __version__, extra=s)
    try:
        args = docopt(__doc__)
        input_json = args["INPUT_JSON"]
        if args["--fit"]:
            print(
                process_file_list_from_json(
                    input_json, predict_only=False, model_dir=MODEL_DIR
                ),
                end="",
            )
        else:
            print(process_file_list_from_json(input_json, model_dir=MODEL_DIR), end="")
    except Exception as e:
        logger.error(str(e), extra=s)
        raise e
    logger.info("finish", extra=s)
    return None


if __name__ == "__main__":
    print(main())
