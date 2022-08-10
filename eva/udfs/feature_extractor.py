# coding=utf-8
# Copyright 2018-2022 EVA
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import pandas as pd

import torch
from torch import Tensor
from torchvision import models
from torchvision.transforms import Compose, transforms

from typing import List
from eva.models.catalog.frame_info import FrameInfo
from eva.models.catalog.properties import ColorSpace
from eva.udfs.pytorch_abstract_udf import PytorchAbstractUDF


class FeatureExtractor(PytorchAbstractUDF):
    """
    """

    @property
    def name(self) -> str:
        return "FeatureExtractor"

    def __init__(self):
        super().__init__()
        self.model = models.resnet50(pretrained=True)
        for param in self.model.parameters():
            param.requires_grad = False
        self.model.fc = torch.nn.Identity()
        self.model.eval()

    @property
    def transforms(self) -> Compose:
        return Compose([
            transforms.ToTensor()
        ])

    @property
    def labels(self) -> List[str]:
        return []

    @property
    def input_format(self) -> FrameInfo:
        return FrameInfo(-1, -1, 3, ColorSpace.RGB)

    def _get_predictions(self, frames: Tensor) -> pd.DataFrame:
        """
        Performs feature extraction on input frames
        Arguments:
            frames (np.ndarray): Frames on which predictions need
            to be performed

        Returns:
            features (List[float])
        """
        outcome = pd.DataFrame()
        for f in frames:
            with torch.no_grad():
                outcome = outcome.append(
                    {
                        "features": self.model(torch.unsqueeze(f, 0))
                    },
                    ignore_index=True)
        return outcome
