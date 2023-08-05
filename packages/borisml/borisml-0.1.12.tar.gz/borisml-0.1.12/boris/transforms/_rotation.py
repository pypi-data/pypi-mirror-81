""" RandomRotate """
# Copyright (c) 2020. Mirage Technologies AG and its affiliates.
# All Rights Reserved

import numpy as np
from torchvision.transforms import functional as TF


class RandomRotate(object):
    """Randomly rotates the image by 90 degrees
    """

    def __init__(self, prob: float = 0.5, angle: int = 90):
        self.prob = prob
        self.angle = 90

    def __call__(self, sample):

        # rotate the image with a 50% chance
        prob = np.random.random_sample()
        if prob < self.prob:
            sample = TF.rotate(sample, self.angle)
        return sample
