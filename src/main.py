import numpy as np
from PIL import Image

from ImagePartition.QuadTree import QuadTree

if __name__ == "__main__":
    """
    Compresses an image by averaging out pixel colors in similarly colored regions and reducing image detail.
    Set file path to image before usage!
    """

    file_path = ""

    image = Image.open(file_path)
    data = np.asarray(image)
    data.setflags(write=1)

    # Parameters to control resulting image quality
    max_depth = float('inf')  # Controls the max size of a quadtree pixel quadrant
    max_std_dev = 5  # Tolerance for pixel color deviation among a group of pixels

    tree = QuadTree(data, max_depth, max_std_dev)

    compressed_image = Image.fromarray(data)
    compressed_image.show()

    dot_index = file_path.rfind(".")
    # Save the compressed image
    compressed_image.save(file_path[:dot_index] + "_compressed." + file_path[dot_index + 1:])

    tree.highlight_leaves()
    compressed_visualized_image = Image.fromarray(data)
    # Save a visualization of the compression
    # Note that denser black regions means a higher level of detail is being preserved there
    compressed_visualized_image.save(file_path[:dot_index] + "_compressed_visualized." + file_path[dot_index + 1:])
