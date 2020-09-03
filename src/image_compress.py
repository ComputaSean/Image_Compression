import sys

import numpy as np
from PIL import Image

from imagepartition.quad_tree import QuadTree

if __name__ == "__main__":
    """
    Compresses an image by averaging out pixel colors in similarly colored rectangle regions and reducing image detail.
    A compressed copy of the original image "x.y" is saved as "x_compressed.y".
    
    Arguments:
        max_depth - controls the max depth of the quadtree and consequently the max size of a quadtree pixel quadrant
        max_std_dev - specifies the tolerance for pixel color deviation among a group of pixels
        show_compression - set to non-zero value to save a visualization of the compression 
        file_path - file path to image
    """

    arg_list = sys.argv
    if len(arg_list) != 5:
        print("Usage: \"python3 image_compression.py max_depth max_std_dev show_compression file_path\"")
        exit(1)

    # Parameters to control resulting image quality
    max_depth = int(arg_list[1])
    max_std_dev = int(arg_list[2])

    show_compression = int(arg_list[3])

    file_path = arg_list[4]
    image = Image.open(file_path)
    data = np.asarray(image)
    data.setflags(write=1)

    tree = QuadTree(data, max_depth, max_std_dev)

    compressed_image = Image.fromarray(data)
    compressed_image.show()

    dot_index = file_path.rfind(".")
    # Save the compressed image
    compressed_image.save(file_path[:dot_index] + "_compressed." + file_path[dot_index + 1:])

    if show_compression != 0:
        tree.highlight_leaves()
        compressed_visualized_image = Image.fromarray(data)
        # Save a visualization of the compression
        # Note that denser black regions means a higher level of detail is being preserved there
        compressed_visualized_image.save(file_path[:dot_index] + "_compressed_visualized." + file_path[dot_index + 1:])
