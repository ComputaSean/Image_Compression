from typing import Optional

from imagepartition.tree_node import TreeNode


class InternalNode(TreeNode):
    """
    A node of the quadtree that is a parent to some other node or None.
    """

    def __init__(self, q1: Optional[TreeNode], q2: Optional[TreeNode],
                 q3: Optional[TreeNode], q4: Optional[TreeNode]) -> None:
        self.quadrants = [q1, q2, q3, q4]

    def set_quadrant(self, index: int, node: Optional[TreeNode]) -> None:
        self.quadrants[index] = node

    def get_quadrant(self, index: int) -> Optional[TreeNode]:
        return self.quadrants[index]
