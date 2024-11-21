# Nissl Detection Display Code #
# Input: Image File (tiff/jp2), CSV for the cell centers in the image
# Output: Image with cell centers
# Usage: python3 .\display_results.py .\test_image.tif
# Last Updated: Nov 21, 2024 by Samik Banerjee (CSHL)

# Calling all imports
from skimage.io import imread, imsave # Image read write functions
from skimage import io
from matplotlib import pyplot as plt
import pandas as pd
import os
import sys
import pathlib


# !OPTIONAL: KAKADU image read function
def imread_fast(img_path):
    # img_path = img_path[0:-1]
    img_path_C= img_path.replace("&", "\&")
    base_C = os.path.basename(img_path_C)
    base_C = base_C[0 : -4]
    base = os.path.basename(img_path)
    base = base[0 : -4]
    err_code = os.system("kdu_expand -i " + img_path_C + " -o temp/" + base_C + ".tif -num_threads 16")
    img = imread('temp/' + base + '.tif')
    os.system("rm temp/" + base_C + '.tif')
    return img

# !OPTIONAL: Kakadu image write function
def imwrite_fast(img_path, opImg):
    img_path_C= img_path.replace("&", "\&")
    base_C = os.path.basename(img_path_C)
    base_C = base_C[0 : -4]
    base = os.path.basename(img_path)
    base = base[0 : -4]
    img = imsave('temp/' + base + '.tif', opImg)
    err_code = os.system("kdu_compress -i temp/" + base_C + ".tif -o " + img_path_C + " -rate 1 Creversible=yes Clevels=7 Clayers=8 Stiles=\{1024,1024\} Corder=RPCL Cuse_sop=yes ORGgen_plt=yes ORGtparts=R Cblk=\{32,32\} -num_threads 32")
    os.system("rm temp/" + base_C + '.tif')

fName = sys.argv[1] # Read the image

file_extension = pathlib.Path(fName).suffix # Get the extension of the file

# Read the image
if file_extension == '.tif':
    im = imread(fName)
else:
    im = imread_fast(fName)
w, h, c = im.shape # Get image size

# Read CSV for all the centriods
df = pd.read_csv(fName[0:-3] + 'csv', header = None)
pts = df.to_numpy()

# Show image and centroids
io.imshow(im)
plt.scatter(pts[:, 1], pts[:, 0], marker="*", color="red", s=20) # Display centroid on cells
plt.show()



