""" Gaussian Blur """
import numpy as np
from PIL import ImageFilter


class GaussianBlur(object):
    # Implements Gaussian blur
    def __init__(self, kernel_size, prob=0.5, scale=0.2):
        self.prob = prob
        self.scale = scale
        # limits for random kernel sizes
        self.min_size = (1 - scale) * kernel_size
        self.max_size = (1 + scale) * kernel_size
        self.kernel_size = kernel_size

    def __call__(self, sample):
        # blur the image with a 50% chance
        prob = np.random.random_sample()
        if prob < self.prob:
            # choose randomized kernel size
            kernel_size = np.random.normal(
                self.kernel_size, self.scale * self.kernel_size
            )
            kernel_size = max(self.min_size, kernel_size)
            kernel_size = min(self.max_size, kernel_size)
            radius = int(kernel_size / 2)
            # return blurred image
            return sample.filter(ImageFilter.GaussianBlur(radius=radius))
        # return original image
        return sample
