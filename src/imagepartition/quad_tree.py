from typing import Optional

import numpy as np

from imagepartition.internal_node import InternalNode
from imagepartition.leaf_node import LeafNode
from imagepartition.tree_node import TreeNode


class QuadTree:
    """
    Recursively splits a raster image into pixel quadrants of varying sizes.
    Pixel quadrants are represented by leaf nodes. Empty pixel quadrants correspond to None.
    The smaller the pixel quadrants the more detail that is preserved.
    Changing the input parameters will determine the resulting image fidelity.
    """

    def __init__(self, raster: np.array, max_depth: int, max_std_dev: int) -> None:
        """
        Creates a quadtree from the given raster image.
        Construction runtime is O(nlog(n)).

        :param raster: 3D array of the image with row, col, and rgba values as the first, second, and third indices
        :param max_depth: maximum depth of the resulting quadtree
        :param max_std_dev: tolerance for pixel disparity in a quadrant before requiring a recursive split
        """
        # Invalid raster dimensions
        if len(raster.shape) != 3:
            self.root = None
        else:
            self.root = QuadTree.construct(raster, max_depth, max_std_dev)

    @staticmethod
    def construct(raster: np.array, max_depth: int, max_std_dev: int) -> Optional[TreeNode]:
        """
        Decompose a raster image into a quadtree.

        :param raster: 3D array of the image with row, col, and rgba values as the first, second, and third indices
        :param max_depth: maximum depth of the quadtree rooted at the returned node
        :param max_std_dev: tolerance for pixel disparity before requiring a split
        :return: root node of quadtree representing the image
        """
        # Base Case: raster doesn't represent any pixels
        if raster.size == 0:
            return None

        # Base Case: stop when maximum depth is achieved, or if pixels of raster are similar enough
        elif max_depth <= 0 or QuadTree.check_homogeneity(raster, max_std_dev):
            return LeafNode(raster)

        # Recursive Case: Divide into partitions for finer detail
        else:
            # Construct all 4 regions of the quadtree by splitting raster along the row and column axes
            quadrants = [second_split for first_split in np.array_split(raster, 2, axis=0)
                         for second_split in np.array_split(first_split, 2, axis=1)]

            q1 = QuadTree.construct(quadrants[0], max_depth - 1, max_std_dev)
            q2 = QuadTree.construct(quadrants[1], max_depth - 1, max_std_dev)
            q3 = QuadTree.construct(quadrants[2], max_depth - 1, max_std_dev)
            q4 = QuadTree.construct(quadrants[3], max_depth - 1, max_std_dev)

            return InternalNode(q1, q2, q3, q4)

    @staticmethod
    def check_homogeneity(raster: np.array, threshold: int) -> bool:
        """
        Returns whether the pixels of the raster image are similar enough in color.

        :param raster: 3D array of the image with row, col, and rgba values as the first, second, and third indices
        :param threshold: tolerance for average pixel color deviation
        :return: True if pixels are similar enough in color; False otherwise
        """
        # Check if any color channel exceeds the given threshold
        for val in np.std(raster, (0, 1)):
            if val > threshold:
                return False
        return True

    def highlight_leaves(self) -> None:
        """
        Creates a black border around all pixel quadrants/leaves of the quadtree.

        :return: None
        """
        if self.root is not None:
            QuadTree.highlight_leaves_helper(self.root)

    @staticmethod
    def highlight_leaves_helper(cur_node: TreeNode) -> None:
        """
        Creates a black border around all pixel quadrants/leaves of the current node.

        :param cur_node: current node of the quadtree
        :return: None
        """
        if type(cur_node) is LeafNode:
            LeafNode.highlight_border(cur_node.pixels)
        else:
            # Recursively highlight all leaves in all quadrants
            for i in range(4):
                quadrant = cur_node.get_quadrant(i)
                if quadrant is not None:
                    QuadTree.highlight_leaves_helper(cur_node.get_quadrant(i))

    def get_height(self) -> int:
        """
        Gets the height of the quadtree.

        :return: quadtree height
        """
        return QuadTree.get_height_helper(self.root)

    @staticmethod
    def get_height_helper(cur_node: TreeNode) -> int:
        """
        Helper for get_height().

        :param cur_node: current node of the quadtree
        :return: height of the quadtree rooted at cur_node
        """
        if cur_node is None or type(cur_node) is LeafNode:
            return 0
        else:
            subtree_heights = np.array([0, 0, 0, 0])
            for i in range(4):
                quadrant = cur_node.get_quadrant(i)
                if quadrant is not None:
                    subtree_heights[i] += QuadTree.get_height_helper(quadrant)
            return max(subtree_heights) + 1
