# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Classes and functions to injest data for object detection."""

from abc import ABC, abstractmethod
import json
import os
import numpy as np
from torch.utils.data import Dataset
from collections import defaultdict
from sklearn.model_selection import train_test_split
import torch
from ..common.augmentations import transform
from azureml.core import Dataset as AmlDataset
from azureml.automl.core.shared.exceptions import ClientException
from azureml.automl.core.shared import logging_utilities

from azureml.contrib.automl.dnn.vision.common.logging_utils import get_logger
from azureml.contrib.automl.dnn.vision.common.utils import _read_image
from ..common.constants import DatasetFieldLabels, PredefinedLiterals
from ...common.aml_dataset_base_wrapper import AmlDatasetBaseWrapper
from ...common.labeled_dataset_helper import AmlLabeledDatasetHelper
from ...common.exceptions import AutoMLVisionDataException

logger = get_logger(__name__)


class ObjectDetectionDatasetBaseWrapper(ABC, Dataset):
    """Class the establishes interface for object detection datasets"""

    @abstractmethod
    def __getitem__(self, index):
        """Get item by index

        :param index: Index of object
        :type index: Int
        :return: Item at Index
        :rtype: Object Detection Record
        """
        pass

    @abstractmethod
    def __len__(self):
        """Get the number of items in dataset

        :return: Number of items in dataset
        :rtype: Int
        """
        pass

    @property
    @abstractmethod
    def num_classes(self):
        """Get the number of classes in dataset

        :return: Number of classes
        :rtype: Int
        """
        pass

    @abstractmethod
    def label_to_index_map(self, label):
        """Get the index associated with a given class

        :param label: Label name
        :type: String
        :return: Index associated with label
        :rtype: Int
        """
        pass

    @abstractmethod
    def index_to_label(self, index):
        """Get the label associated with a certain index

        :param index: Index
        :type index: Int
        :return: Class name
        :rtype: String
        """
        pass

    @property
    @abstractmethod
    def classes(self):
        """Get a list of classes ordered by index.

        :return: List of classes
        :rtype: List of Strings
        """
        pass


class ObjectAnnotation:
    """Class that contains all of the information associated with
    a single bounding box."""

    def __init__(self, labels):
        """
        :param labels: Information about the bounding box in
        the image, must contain label, topX, topY, bottomX, bottomY.
        :type labels: Dictionary
        """

        self._bounding_box = None
        self._missing_properties = True
        self._label = None
        self._area = None
        self._iscrowd = 0

        self._width = None
        self._height = None

        self._init_labels(labels)

    @property
    def bounding_box(self):
        """Get bounding box coordinates

        :return: Bounding box in form [top, left, bottom, right] in pixel coordinates
        :rtype: List of floats
        """
        return self._bounding_box

    @property
    def label(self):
        """Get bounding box classification

        :return: Classification for bounding box object
        :rtype: String
        """
        return self._label

    @property
    def area(self):
        """Get bounding box area

        :return: Area of bounding box
        :rtype: Float
        """
        return self._area

    @property
    def iscrowd(self):
        """Get image is iscrowd

        :return: 0 for not crowd, 1 for crowd
        :rtype: int
        """
        return self._iscrowd

    @property
    def missing_properties(self):
        """Are the properties related to width, height, area been filled in."""
        return self._missing_properties

    def _init_labels(self, labels):

        if (DatasetFieldLabels.CLASS_LABEL not in labels or
                DatasetFieldLabels.X_0_PERCENT not in labels or
                DatasetFieldLabels.Y_0_PERCENT not in labels or
                DatasetFieldLabels.X_1_PERCENT not in labels or
                DatasetFieldLabels.Y_1_PERCENT not in labels):
            raise AutoMLVisionDataException("Incomplete Record", has_pii=False)

        self._label = labels[DatasetFieldLabels.CLASS_LABEL]

        if DatasetFieldLabels.IS_CROWD in labels:
            self._iscrowd = int(labels[DatasetFieldLabels.IS_CROWD] == "true")

        self._x0_percentage = float(labels[DatasetFieldLabels.X_0_PERCENT])
        self._y0_percentage = float(labels[DatasetFieldLabels.Y_0_PERCENT])
        self._x1_percentage = float(labels[DatasetFieldLabels.X_1_PERCENT])
        self._y1_percentage = float(labels[DatasetFieldLabels.Y_1_PERCENT])

        # TODO - change to always have the fill_box_properties method called
        # depending on the model, this will be overridden by fill_box_properties
        self._bounding_box = [self._label,
                              self._x0_percentage, self._y0_percentage,
                              self._x1_percentage, self._y1_percentage]

    def fill_box_properties(self, height=None, width=None):
        """Fills box properties that are computed from image's width and height.

        :param height: height in pixels
        :type height: int
        :param width: width in pixels
        :type width: int
        """
        self._bounding_box = [self._x0_percentage * width,
                              self._y0_percentage * height,
                              self._x1_percentage * width,
                              self._y1_percentage * height]

        self._area = (self._bounding_box[2] - self._bounding_box[0]) * \
                     (self._bounding_box[3] - self._bounding_box[1])

        self._width = width
        self._height = height
        self._missing_properties = False


class CommonObjectDetectionDatasetWrapper(ObjectDetectionDatasetBaseWrapper):
    """Wrapper for object detection dataset"""

    def __init__(self, is_train=False, prob=0.5, ignore_data_errors=True, transform=None,
                 use_bg_label=True, label_compute_func=None, settings=None):
        """
        :param is_train: which mode (training, inference) is the network in?
        :type is_train: boolean
        :param prob: target probability of randomness for each augmentation method
        :type prob: float
        :param ignore_data_errors: boolean flag on whether to ignore input data errors
        :type ignore_data_errors: bool
        :param transform: function to apply for data transformation
        :type transform: function that gets 2 parameters: image tensor and targets tensor
        :param use_bg_label: flag to indicate if we use incluse the --bg-- label
        :type use_bg_label: bool
        :param label_compute_func: function to use when computing labels
        :type label_compute_func: func
        :param settings: additional settings to be used in the dataset
        :type settings: dict
        """
        self._is_train = is_train
        self._prob = prob
        self._ignore_data_errors = ignore_data_errors
        self._transform = transform
        self._use_bg_label = use_bg_label
        self._label_compute_func = label_compute_func
        self._settings = settings

        self._image_urls = []
        self._annotations = defaultdict(list)
        self._object_classes = []
        self._class_to_index_map = {}
        self._labels = None

    def __len__(self):
        """Get number of records in dataset

        :return: Number of records
        :rtype: Int
        """
        return len(self._image_urls)

    def __getitem__(self, index):
        """Get dataset item by index

        :return: Image, bounding box information, and image information, with form:
                 -Image: Torch tensor
                 -Labels: Dictionary with keys "boxes" and "labels", where boxes is a list of lists of
                          pixel coordinates, and "labels" is a list of integers with the class of each bounding box,
                 -Image Information: is a dictionary with the image url, image width and height,
                                     and a list of areas of the different bounding boxes
        :rtype: Tuple of form (Torch Tensor, Dictionary, Dictionary)
        """
        image_url = self._image_urls[index]
        image = _read_image(self._ignore_data_errors, image_url)
        if image is None:
            return None, {}, {}

        height = image.height
        width = image.width

        bounding_boxes = []
        classes = []
        iscrowd = []

        for annotation in self._annotations[image_url]:
            self._fill_missing_fields_annotation(annotation, height=height, width=width)
            bounding_boxes.append(annotation.bounding_box)
            annotation_index = self._class_to_index_map[annotation.label]
            classes.append(annotation_index)
            iscrowd.append(annotation.iscrowd)

        boxes = torch.as_tensor(bounding_boxes, dtype=torch.float32)
        labels = torch.as_tensor(classes, dtype=torch.int64)

        # validate bbox w/ condition of (x_min < x_max and y_min < y_max)
        # if no valid bbox left, return None to skip this image, otherwise pass only valid ones
        is_valid = (boxes[:, 0] < boxes[:, 2]) * (boxes[:, 1] < boxes[:, 3])
        boxes = boxes[is_valid, :]
        labels = labels[is_valid]
        iscrowd = torch.as_tensor(iscrowd, dtype=torch.int8)
        iscrowd = iscrowd[is_valid].tolist()
        if not boxes.shape[0]:
            logger.warning("(train: {}) No valid bbox for image index: {}.".format(self._is_train, index))
            return None, {}, {}

        # data augmentations
        image, boxes, areas, height, width = transform(image, boxes, self._is_train, self._prob, self._transform)

        return (image,
                {"boxes": boxes, "labels": labels},
                {"areas": areas, "iscrowd": iscrowd, "filename": image_url,
                 "height": height, "width": width})

    @staticmethod
    def _fill_missing_fields_annotation(annotation, height=None, width=None):
        """Fills object annotation in place

        :param annotation: annotation object
        :type annotation: azureml.contrib.automl.dnn.vision.object_detection.data.datasets.ObjectAnnotation
        :param height: image height in pixels
        :type height: int
        :param width: image width in pixels
        :type width: int
        """
        if height is None or width is None:
            raise ClientException("width or height cannot be None", has_pii=False)

        if annotation.missing_properties:
            annotation.fill_box_properties(width=width, height=height)

    @property
    def num_classes(self):
        """Get number of classes in dataset

        :return: Number of classes in dataset
        :rtype: Int
        """
        return len(self._object_classes)

    @property
    def classes(self):
        """Get list of classes in dataset

        :return: List of classses
        :rtype: List of strings
        """
        return self._object_classes

    @property
    def transform(self):
        """The post augmentation transform.

        :return: the transform function
        :rtype: function that gets 2 parameters: image tensor and targets tensor
        """
        return self._transform

    @transform.setter
    def transform(self, value):
        """The post augmentation transform.

        :return: the transform function
        :rtype: function that gets 2 parameters: image tensor and targets tensor
        """
        self._transform = value

    def label_to_index_map(self, label):
        """Get mapping from class name to numeric
        class index.

        :param label: Class name
        :type label: String
        :return: Numeric class index
        :rtype: Int
        """
        return self._class_to_index_map[label]

    def index_to_label(self, index):
        """Get the class name associated with numeric index

        :param index: Numeric class index
        :type index: Int
        :return: Class name
        :rtype: String
        """
        return self._object_classes[index]

    def train_val_split(self, valid_portion=0.2):
        """Splits a dataset into two datasets, one for training and and for validation.

        :param valid_portion: (optional) Portion of dataset to use for validation. Defaults to 0.2.
        :type valid_portion: Float between 0.0 and 1.0
        :return: Training dataset and validation dataset
        :rtype: Tuple of form (CommonObjectDetectionSubsetWrapper, CommonObjectDetectionSubsetWrapper)
        """
        number_of_samples = len(self._image_urls)
        indices = np.arange(number_of_samples)
        training_indices, validation_indices = train_test_split(indices, test_size=valid_portion)

        train_dataset = CommonObjectDetectionSubsetWrapper(self, training_indices)
        validation_dataset = CommonObjectDetectionSubsetWrapper(self, validation_indices)
        validation_dataset._is_train = False

        return train_dataset, validation_dataset

    def reset_classes(self, classes):
        """Update dataset wrapper with a list of new classes

        :param classes: classes
        :type classes: string list
        """
        self._object_classes = sorted(classes, reverse=False)
        self._class_to_index_map = {object_class: i for
                                    i, object_class in
                                    enumerate(self._object_classes)}

    def collate_function(self, batch):
        """Collate function for the dataset"""
        return tuple(zip(*batch))

    @staticmethod
    def _prepare_images_and_labels(image_urls, annotations, object_classes, use_bg_label, label_compute_func):
        object_classes = list(object_classes)
        if use_bg_label:
            object_classes = [PredefinedLiterals.BG_LABEL] + object_classes
        # "-" is smaller than capital letter
        object_classes = sorted(object_classes, reverse=False)  # make sure --bg-- is mapped to zero index
        # Use sorted to make sure all workers get the same order of data in distributed training/validation
        image_urls = sorted(image_urls)
        class_to_index_map = {object_class: i for
                              i, object_class in
                              enumerate(object_classes)}
        labels = None
        if label_compute_func is not None:
            labels = label_compute_func(image_urls, annotations, class_to_index_map)

        return object_classes, image_urls, class_to_index_map, labels


class FileObjectDetectionDatasetWrapper(CommonObjectDetectionDatasetWrapper):
    """Wrapper for object detection dataset"""

    def __init__(self, annotations_file=None, image_folder=".", is_train=False,
                 prob=0.5, ignore_data_errors=True,
                 use_bg_label=True, label_compute_func=None, settings=None):
        """
        :param annotations_file: Annotations file
        :type annotations_file: str
        :param image_folder: target image path
        :type image_folder: str
        :param is_train: which mode (training, inferencing) is the network in?
        :type is_train: boolean
        :param prob: target probability of random horizontal flipping
        :type prob: float
        :param ignore_data_errors: flag to indicate if image data errors should be ignored
        :type ignore_data_errors: bool
        :param use_bg_label: flag to indicate if we use incluse the --bg-- label
        :type use_bg_label: bool
        :param label_compute_func: function to use when computing labels
        :type label_compute_func: func
        :param settings: additional settings to be used in the dataset
        :type settings: dict
        """
        super().__init__(is_train=is_train, prob=prob, ignore_data_errors=ignore_data_errors,
                         use_bg_label=use_bg_label, label_compute_func=label_compute_func,
                         settings=settings)

        if annotations_file is not None:
            annotations = self._read_annotations_file(annotations_file, ignore_data_errors=ignore_data_errors)
            self._init_dataset(annotations, image_folder,
                               ignore_data_errors=ignore_data_errors)

    def _init_dataset(self, annotations, image_folder, ignore_data_errors):

        image_urls = set()
        object_classes = set()

        if not annotations:
            raise AutoMLVisionDataException("No annotations to initialize datasets.", has_pii=False)

        for annotation in annotations:
            if (DatasetFieldLabels.IMAGE_URL not in annotation or
                    DatasetFieldLabels.IMAGE_DETAILS not in annotation or
                    DatasetFieldLabels.IMAGE_LABEL not in annotation):
                missing_required_fields_message = "Missing required fields in annotation"
                if ignore_data_errors:
                    logger.warning(missing_required_fields_message)
                else:
                    raise AutoMLVisionDataException(missing_required_fields_message, has_pii=False)

            try:
                object_info = ObjectAnnotation(annotation[DatasetFieldLabels.IMAGE_LABEL])
            except AutoMLVisionDataException as ex:
                if ignore_data_errors:
                    logging_utilities.log_traceback(ex, logger)
                    continue
                else:
                    raise

            image_url = os.path.join(image_folder, annotation[DatasetFieldLabels.IMAGE_URL])
            if not os.path.exists(image_url):
                file_missing_message = "File missing for image"
                if ignore_data_errors:
                    logger.warning(file_missing_message)
                    continue
                else:
                    raise AutoMLVisionDataException(file_missing_message, has_pii=False)

            image_urls.add(image_url)

            self._annotations[image_url].append(object_info)

            object_classes.add(annotation[DatasetFieldLabels.IMAGE_LABEL][DatasetFieldLabels.CLASS_LABEL])

        self._object_classes, self._image_urls, self._class_to_index_map, self._labels = \
            self._prepare_images_and_labels(image_urls, self._annotations, object_classes,
                                            self._use_bg_label, self._label_compute_func)

    @staticmethod
    def _read_annotations_file(annotations_file, ignore_data_errors=True):
        annotations = []
        line_no = 0
        with open(annotations_file, "r") as json_file:
            for line in json_file:
                try:
                    try:
                        line_no += 1
                        annotations.append(json.loads(line))
                    except json.JSONDecodeError:
                        raise AutoMLVisionDataException("Json decoding error in line no: {}".format(line_no),
                                                        has_pii=False)
                except AutoMLVisionDataException as ex:
                    if ignore_data_errors:
                        logging_utilities.log_traceback(ex, logger)
                    else:
                        raise

        return annotations


# TODO RK: remove this class
class CommonObjectDetectionSubsetWrapper(CommonObjectDetectionDatasetWrapper):
    """Creates a subset of a larger CommonObjectDetectionDatasetWrapper"""

    def __init__(self, parent_dataset, indices):
        """
        :param parent_dataset: Dataset to take a subset of
        :type parent_dataset: CommonObjectDetectionDatasetWrapper
        :param indices: Indices to use in subset
        :type indices: List of Ints
        """
        self._image_urls = parent_dataset._image_urls
        self._annotations = parent_dataset._annotations
        self._object_classes = parent_dataset._object_classes
        self._class_to_index_map = parent_dataset._class_to_index_map
        self._indices = indices
        self._is_train = parent_dataset._is_train
        self._prob = parent_dataset._prob
        self._ignore_data_errors = parent_dataset._ignore_data_errors

        self._parent_dataset = parent_dataset
        self._labels = parent_dataset._labels
        self._settings = parent_dataset._settings
        self.collate_function = parent_dataset.collate_function

    def _set_indices(self, indices):
        self._indices = indices

    def __len__(self):
        """Get the number of records in subset

        :return: Number of records
        :rtype: Int
        """
        return len(self._indices)

    def __getitem__(self, idx):
        """Get a record at a certain subset index

        :return: Dataset record (see __getitem__
        of CommonObjectDetectionDatasetWrapper)
        :rtype: Tuple (see __getitem__ of
        CommonObjectDetectionDatasetWrapper)
        """

        index = self._indices[idx]

        return self._parent_dataset.__getitem__(index)


class AmlDatasetObjectDetectionWrapper(CommonObjectDetectionDatasetWrapper, AmlDatasetBaseWrapper):
    """Wrapper for Aml labeled dataset for object detection dataset"""

    def __init__(self, dataset_id, is_train=False, prob=0.5,
                 workspace=None, ignore_data_errors=False, datasetclass=AmlDataset,
                 download_files=True, use_bg_label=True, label_compute_func=None,
                 settings=None):
        """
        :param dataset_id: dataset id
        :type dataset_id: str
        :param is_train: which mode (training, inferencing) is the network in?
        :type is_train: boolean
        :param prob: target probability of random horizontal flipping
        :type prob: float
        :param ignore_data_errors: Setting this ignores and files in the labeled dataset that fail to download.
        :type ignore_data_errors: bool
        :param datasetclass: The source dataset class.
        :type datasetclass: class
        :param download_files: Flag to download files or not.
        :type download_files: bool
        :param use_bg_label: flag to indicate if we use incluse the --bg-- label
        :type use_bg_label: bool
        :param label_compute_func: function to use when computing labels
        :type label_compute_func: func
        :param settings: additional settings to be used in the dataset
        :type settings: dict
        """
        super().__init__(is_train=is_train, prob=prob, ignore_data_errors=ignore_data_errors,
                         use_bg_label=use_bg_label, label_compute_func=label_compute_func,
                         settings=settings)

        self._labeled_dataset_helper = AmlLabeledDatasetHelper(dataset_id, workspace, ignore_data_errors,
                                                               datasetclass,
                                                               image_column_name=self.DATASET_IMAGE_COLUMN_NAME,
                                                               download_files=download_files)
        self._label_column_name = self._labeled_dataset_helper.label_column_name
        images_df = self._labeled_dataset_helper.images_df

        self._init_dataset(images_df, ignore_data_errors=ignore_data_errors)

    def _init_dataset(self, images_df, ignore_data_errors=True):

        image_urls = set()
        object_classes = set()

        for index, label in enumerate(images_df[self._label_column_name]):

            image_url = self._labeled_dataset_helper.get_image_full_path(index)

            if not os.path.exists(image_url):
                mesg = "File missing for image"
                raise AutoMLVisionDataException(mesg, has_pii=False)

            image_urls.add(image_url)

            for annotation in label:
                try:
                    object_info = ObjectAnnotation(annotation)
                except AutoMLVisionDataException as ex:
                    if ignore_data_errors:
                        logging_utilities.log_traceback(ex, logger)
                        continue
                    else:
                        raise

                self._annotations[image_url].append(object_info)

                object_classes.add(annotation[DatasetFieldLabels.CLASS_LABEL])

        self._object_classes, self._image_urls, self._class_to_index_map, self._labels = \
            self._prepare_images_and_labels(image_urls, self._annotations, object_classes,
                                            self._use_bg_label, self._label_compute_func)

    def get_images_df(self):
        """Return images dataframe"""
        return self._labeled_dataset_helper.images_df
