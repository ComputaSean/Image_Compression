import numpy as np


class QuadTree:
    """
    Recursively splits an image into pixel quadrants of varying sizes.
    The smaller the pixel quadrants the more detail that is preserved.
    Changing the input parameters will determine resulting image fidelity.
    """

    def __init__(self, image, max_depth, max_std_dev):
        """
        Creates a quadtree from the given image. Construction runtime is O(nlog(n)).

        Precondition: image is a square image whose side length is divisible by 4
        This precondition allows the quadtree to cleanly divide the region into equal quadrants.

        :param image: 3D array of the image with row, col, and rgb values as the first, second, and third indices
        :param max_depth: maximum depth of the resulting quadtree
        :param max_std_dev: tolerance for pixel disparity before requiring a split
        """
        # Invalid image dimensions
        if image.shape[0] != image.shape[1] or image.shape[0] % 4 != 0:
            self.root = None
        else:
            self.root = QuadTree.construct(image, max_depth, max_std_dev)

    @staticmethod
    def construct(image, max_depth, max_std_dev):
        """
        Decompose a raster array of an image into a quadtree.

        :param image: 3D array of the image with row, col, and rgb values as the first, second, and third indices
        :param max_depth: maximum depth of the quadtree rooted at the returned node
        :param max_std_dev: tolerance for pixel disparity before requiring a split
        :return: root node of quadtree representing the image
        """
        # Base Case: Stop when there's only 1 pixel, maximum depth is achieved, or if pixels of image are similar enough
        if image.shape[0] <= 1 or max_depth <= 0 or QuadTree.check_homogeneity(image, max_std_dev):
            return LeafNode(image)

        # Recursive Case: Divide into partitions for finer detail
        else:
            num_rows = image.shape[0]
            num_cols = image.shape[1]

            # Construct all 4 regions of the quadtree
            # Quadrant labelling follows typical convention
            q1 = QuadTree.construct(image[:num_rows // 2, num_cols // 2:, :], max_depth - 1, max_std_dev)
            q2 = QuadTree.construct(image[:num_rows // 2, :num_cols // 2, :], max_depth - 1, max_std_dev)
            q3 = QuadTree.construct(image[num_rows // 2:, :num_cols // 2, :], max_depth - 1, max_std_dev)
            q4 = QuadTree.construct(image[num_rows // 2:, num_cols // 2:, :], max_depth - 1, max_std_dev)

            return InternalNode(q1, q2, q3, q4)

    @staticmethod
    def check_homogeneity(image, threshold):
        """
        Returns whether the pixels of image are similar enough in color.

        :param image: 3D array of the image with row, col, and rgb values as the first, second, and third indices
        :param threshold: tolerance for average pixel color deviation
        :return: True if pixels are similar enough in color; False otherwise
        """
        # Check if any color channel exceeds the given threshold
        for val in np.std(image, (0, 1)):
            if val > threshold:
                return False
        return True

    def highlight_leaves(self):
        """
        Creates a black border around all pixel quadrants/leaves of the quadtree.

        :return: None
        """
        if self.root is not None:
            QuadTree.highlight_leaves_helper(self.root)

    @staticmethod
    def highlight_leaves_helper(cur_node):
        """
        Creates a black border around all leaves of all quadrants of the current node.

        :param cur_node: current node of the quadtree
        :return: None
        """
        if type(cur_node) is LeafNode:
            LeafNode.highlight_border(cur_node.get_pixels())
        else:
            # Recursively highlight all leaves in all quadrants
            for i in range(4):
                QuadTree.highlight_leaves_helper(cur_node.get_quadrant(i))

    def get_height(self):
        """
        Gets the height of the quadtree.

        :return: quadtree height
        """
        return QuadTree.get_height_helper(self.root)

    @staticmethod
    def get_height_helper(cur_node):
        """
        Helepr for get_height().

        :param cur_node: current node of the quadtree
        :return: height of the quadtree rooted at cur_node
        """
        if cur_node is None or type(cur_node) is LeafNode:
            return 0
        else:
            return max(QuadTree.get_height_helper(cur_node.get_quadrant(0)),
                       QuadTree.get_height_helper(cur_node.get_quadrant(1)),
                       QuadTree.get_height_helper(cur_node.get_quadrant(2)),
                       QuadTree.get_height_helper(cur_node.get_quadrant(3))) + 1


class InternalNode:
    """
    Corresponds to a node of the quadtree that is a parent to some other node.
    """

    def __init__(self, q1, q2, q3, q4):
        self.quadrants = [q1, q2, q3, q4]

    def set_quadrant(self, index, node):
        self.quadrants[index] = node

    def get_quadrant(self, index):
        return self.quadrants[index]


class LeafNode:
    """
    Corresponds to a node of the quadtree that represents some pixel quadrant of an image.
    All pixels of the leaf node will take on their collective averaged pixel color.
    """

    def __init__(self, pixels):
        # Single pixels don't need to be averaged out
        if pixels.shape != (1, 1, 3):
            LeafNode.average_pixels(pixels)
        self.pixels = pixels

    def get_pixels(self):
        return self.pixels

    @staticmethod
    def average_pixels(pixels):
        """
        Sets the color of every pixel in pixels to be the averaged pixel color of all pixels.

        :param pixels: pixel quadrant that a leaf node represents
        :return: None
        """
        rgb = np.average(pixels, (0, 1))  # Calculate pixel color average
        # Set every pixel of the quadrant to the average color
        for row in range(pixels.shape[0]):
            for col in range(pixels.shape[1]):
                pixels[row][col][0] = rgb[0]
                pixels[row][col][1] = rgb[1]
                pixels[row][col][2] = rgb[2]

    @staticmethod
    def highlight_border(pixels):
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
