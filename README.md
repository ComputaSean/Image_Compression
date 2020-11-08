# Image Compression #
An image compression program that reduces image size and detail by averaging out pixel colors in similarly colored rectangular regions. \
This is accomplished using a region quadtree to recursively divide the picture out into quadrants.
The pixels of a quadtree region are averaged out if their standard deviation for each color channel falls below a threshold, or if the node representing the region exceeds the maximum tree depth.

Users control the level of compression and detail by specifying the color threshold and maximum tree depth. A low threshold and high maximum tree depth results in a lightly compressed image with less space savings but more fine detail preserved.
A high threshold and low maximum tree depth results in a heavily compressed image with significant space savings but less fine detail preserved.

Some examples of compressed pictures are shown below. A visualization of the compression is also included, with smaller green rectangles indicating areas where more fine detail is preserved and larger rectangles indicating the opposite i.e., many pixels were averaged out over a large area.

Note that resized images are displayed in this README due to formatting. It is best to open the pictures in a new tab to closely examine details.  

## Iceberg ##
Original image size was 2.25 MB. \
Argument of max_depth = 11 and max_std_dev = 3 resulted in a compressed image size of 631 KB. \
Picture source: https://pixabay.com/photos/cold-frozen-glacier-ice-iceberg-1866516/

Original Image \
<img src = /Example%20Images/iceberg.jpg width = 1920>
Compressed Image \
<img src = /Example%20Images/iceberg_compressed.jpg width = 1920>
Visualization of Compression \
<img src = /Example%20Images/iceberg_compressed_visualized.jpg width = 1920>

## Mona Lisa ##
Original image size was 2.48 MB. \
Argument of max_depth = 11 and max_std_dev = 3 resulted in a compressed image size of 915 KB. \
Picture source: https://pixabay.com/photos/mona-lisa-painting-art-oil-painting-67506/

Original Image \
<img src = /Example%20Images/mona_lisa.jpg width = 480> \
Compressed Image \
<img src = /Example%20Images/mona_lisa_compressed.jpg width = 480> \
Visualization of Compression \
<img src = /Example%20Images/mona_lisa_compressed_visualized.jpg width = 480>

## Urban ##
Original image size was 1.98 MB. \
Argument of max_depth = 10 and max_std_dev = 3 resulted in a compressed image size of 850 KB. \
Picture source: https://pixabay.com/photos/urban-downtown-london-ontario-2004489/

Original Image \
<img src = /Example%20Images/urban.jpg width = 1920>
Compressed Image \
<img src = /Example%20Images/urban_compressed.jpg width = 1920>
Visualization of Compression \
<img src = /Example%20Images/urban_compressed_visualized.jpg width = 1920>

## Japanese Umbrellas ##
Original image size was 2.80 MB. \
Argument of max_depth = 10 and max_std_dev = 3 resulted in a compressed image size of 1.64 MB. \
Picture source: https://pixabay.com/photos/japanese-umbrellas-umbrella-636870/

Original Image \
<img src = /Example%20Images/umbrellas.jpg width = 1920>
Compressed Image \
<img src = /Example%20Images/umbrellas_compressed.jpg width = 1920>
Visualization of Compression \
<img src = /Example%20Images/umbrellas_compressed_visualized.jpg width = 1920>
