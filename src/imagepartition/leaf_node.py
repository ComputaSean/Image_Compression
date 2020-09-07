import numpy as np

from imagepartition.tree_node import TreeNode


class LeafNode(TreeNode):
    """
    Corresponds to a node of the quadtree that represents some pixel quadrant of an image.
    All pixels of the leaf node will take on their collective averaged pixel color.
    """

    def __init__(self, pixels: np.ndarray) -> None:
        # Single pixels don't need to be averaged out
        if pixels.shape[0] != 1 and pixels.shape[1] != 1:
            LeafNode._average_pixels(pixels)
        self.pixels = pixels

    @staticmethod
    def _average_pixels(pixels: np.ndarray) -> None:
        """
        Sets the color of every pixel in pixels to be the averaged pixel color of all pixels.

        :param pixels: pixel quadrant that a leaf node represents
        :return: None
        """
        rgb = np.mean(pixels, (0, 1))  # Calculate pixel color average
        # Set every pixel of the quadrant to the average color
        for row in range(pixels.shape[0]):
            for col in range(pixels.shape[1]):
                pixels[row][col][0] = rgb[0]
                pixels[row][col][1] = rgb[1]
                pixels[row][col][2] = rgb[2]

    @staticmethod
    def highlight_border(pixels: np.ndarray) -> None:
        """
        Creates a black border around the given pixel quadrant.

        :param pixels: pixel quadrant that a leaf node represents
        :return: None
        """
        for row in range(pixels.shape[0]):
            for col in range(pixels.shape[1]):
                if row == 0 or col == 0 or row == pixels.shape[0] - 1 or col == pixels.shape[1] - 1:
                    pixels[row][col][0] = 0
                    pixels[row][col][1] = 0
                    pixels[row][col][2] = 0
