# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Functions to write the model at the end of training."""

import os
import pickle
import shutil
import json

from ...common.constants import ArtifactsLiterals
from ....common.exceptions import AutoMLVisionValidationException
from ...inference import InferenceModelWrapper


def _write_model(model_wrapper, labels=None, output_score_script_name=None,
                 output_featurize_script_name=None, output_dir=None, device=None, enable_onnx_norm=False):
    """Write artifacts.

    :param model_wrapper: model wrapper to output
    :type model_wrapper: azureml.contrib.automl.dnn.vision
    :param labels: list of classes
    :type labels: list
    :param output_score_script_name: path to output score script file
    :type output_score_script_name: str
    :param output_featurize_script_name: path to output featurize script file
    :type output_featurize_script_name: str
    :param output_dir: path to output directory
    :type output_dir: str
    :param device: device where model should be run (usually 'cpu' or 'cuda:0' if it is the first gpu)
    :type device: str
    :param enable_onnx_norm: enable normalization when exporting onnx
    :type enable_onnx_norm: bool
    """
    os.makedirs(output_dir, exist_ok=True)

    # Export and save the torch onnx model.
    onnx_file_path = os.path.join(output_dir, ArtifactsLiterals.ONNX_MODEL_FILE_NAME)
    model_wrapper.export_onnx_model(file_path=onnx_file_path, device=device, enable_norm=enable_onnx_norm)

    # Explicitly Save the labels to a json file.
    if labels is None:
        raise AutoMLVisionValidationException('No labels is found in dataset wrapper', has_pii=False)
    label_file_path = os.path.join(output_dir, ArtifactsLiterals.LABEL_FILE_NAME)
    with open(label_file_path, 'w') as f:
        json.dump(labels, f)

    if model_wrapper.distributed:
        model_wrapper.model = model_wrapper.model.module
        model_wrapper.distributed = False

    inference_model_wrapper = InferenceModelWrapper(model_wrapper, labels=labels)
    # Remove device info
    inference_model_wrapper._device = None
    with open(os.path.join(output_dir, ArtifactsLiterals.MODEL_WRAPPER_PKL), 'wb') as fp:
        pickle.dump(inference_model_wrapper, fp)

    # Save score and featurize script
    dirname = os.path.dirname(os.path.abspath(__file__))
    if output_score_script_name is None:
        output_score_script_name = ArtifactsLiterals.SCORE_SCRIPT

    if output_featurize_script_name is None:
        output_featurize_script_name = ArtifactsLiterals.FEATURIZE_SCRIPT

    shutil.copy(os.path.join(dirname, ArtifactsLiterals.SCORE_SCRIPT),
                os.path.join(output_dir, output_score_script_name))
    shutil.copy(os.path.join(dirname, ArtifactsLiterals.FEATURIZE_SCRIPT),
                os.path.join(output_dir, output_featurize_script_name))
