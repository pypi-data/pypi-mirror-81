# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Constants for the package."""


class SystemSettings:
    """System settings."""
    NAMESPACE = 'azureml.contrib.automl.dnn.vision'
    LOG_FILENAME = 'azureml_automl_vision.log'
    LOG_FOLDER = 'logs'


class PretrainedModelNames:
    """Pre trained model names."""
    RESNET18 = 'resnet18'
    RESNET50 = 'resnet50'
    MOBILENET_V2 = 'mobilenet_v2'
    SE_RESNEXT50_32X4D = 'se_resnext50_32x4d'
    FASTERRCNN_RESNET50_FPN_COCO = 'fasterrcnn_resnet50_fpn_coco'
    MASKRCNN_RESNET50_FPN_COCO = 'maskrcnn_resnet50_fpn_coco'


class RunPropertyLiterals:
    """String keys important for finding the best run."""
    PIPELINE_SCORE = 'score'


class SettingsLiterals:
    """String names for automl settings"""
    DATA_FOLDER = 'data_folder'
    DATASET_ID = 'dataset_id'
    DEVICE = 'device'
    DETERMINISTIC = 'deterministic'
    ENABLE_ONNX_NORMALIZATION = 'enable_onnx_normalization'
    IGNORE_DATA_ERRORS = 'ignore_data_errors'
    IMAGE_FOLDER = 'images_folder'
    LABELS_FILE = 'labels_file'
    LABELS_FILE_ROOT = 'labels_file_root'
    MULTILABEL = 'multilabel'
    NUM_WORKERS = 'num_workers'
    OUTPUT_DIR = 'output_dir'
    RANDOM_SEED = 'seed'
    RESUME = 'resume'
    TASK_TYPE = 'task_type'
    VALIDATION_DATASET_ID = 'validation_dataset_id'
    VALIDATION_LABELS_FILE = 'validation_labels_file'
    MODEL_NAME = "model_name"


class PretrainedModelUrls:
    """The urls of the pretrained models which are stored in the CDN."""

    MODEL_FOLDER_URL = 'https://aka.ms/automl-resources/data/models-vision-pretrained'

    MODEL_URLS = {
        PretrainedModelNames.RESNET18:
        '{}/{}'.format(MODEL_FOLDER_URL, 'resnet18-5c106cde.pth'),
        PretrainedModelNames.RESNET50:
        '{}/{}'.format(MODEL_FOLDER_URL, 'resnet50-19c8e357.pth'),
        PretrainedModelNames.MOBILENET_V2:
        '{}/{}'.format(MODEL_FOLDER_URL, 'mobilenet_v2-b0353104.pth'),
        PretrainedModelNames.SE_RESNEXT50_32X4D:
        '{}/{}'.format(MODEL_FOLDER_URL, 'se_resnext50_32x4d-a260b3a4.pth'),
        PretrainedModelNames.FASTERRCNN_RESNET50_FPN_COCO:
        '{}/{}'.format(MODEL_FOLDER_URL, 'fasterrcnn_resnet50_fpn_coco-258fb6c6.pth'),
        PretrainedModelNames.MASKRCNN_RESNET50_FPN_COCO:
        '{}/{}'.format(MODEL_FOLDER_URL, 'maskrcnn_resnet50_fpn_coco-bf2d0c1e.pth')
    }


class PretrainedSettings:
    """Settings related to fetching pretrained models."""
    DOWNLOAD_RETRY_COUNT = 3


class DistributedLiterals:
    """String keys for distributed parameters."""
    DISTRIBUTED = "distributed"
    MASTER_ADDR = "MASTER_ADDR"
    MASTER_PORT = "MASTER_PORT"
    WORLD_SIZE = "world_size"


class DistributedParameters:
    """Default distributed parameters."""
    DEFAULT_DISTRIBUTED = True
    DEFAULT_BACKEND = "nccl"
    DEFAULT_MASTER_ADDR = "127.0.0.1"
    DEFAULT_MASTER_PORT = "29500"  # TODO: What if this port is not available.
    DEFAULT_RANDOM_SEED = 47


class LRSchedulerNames:
    """String names for scheduler parameters."""
    DEFAULT_LR_SCHEDULER = "STEP"
    STEP = "STEP"
    WARMUP_COSINE = "warmup_cosine"
