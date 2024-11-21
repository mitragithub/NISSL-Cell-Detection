# Nissl Detection Code #
# Input: Image File (tiff/jp2)
# Output: CSV for the cell centers in the image
# Usage: python3 .\cell_functions_new_tiles.py .\test_image.tif
# Last Updated: Nov 21, 2024 by Samik Banerjee (CSHL)

# Calling all imports
import numpy as np 
from skimage.io import imread, imsave # Image read write functions
from skimage.filters import threshold_otsu 
from skimage import io
from matplotlib import pyplot as plt
import skimage
from sklearn.mixture import GaussianMixture
import skimage.measure as measure
import pandas as pd
from shapely.geometry.polygon import Polygon
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

# Gaussian mixture models
def gmm_fn(X, n_components):
    gmm_model = GaussianMixture(n_components, random_state = 42, init_params = 'kmeans', covariance_type = 'tied')
    cluster_labels  = gmm_model.fit_predict(X)
    means = gmm_model.means_
    return gmm_model, cluster_labels

fName = sys.argv[1] # Read the image

file_extension = pathlib.Path(fName).suffix # Get the extension of the file

# Read the image
if file_extension == '.tif':
    im = imread(fName)
else:
    im = imread_fast(fName)
w, h, c = im.shape # Get image size

pts_all = [] # Initialize the centroids list

# Heuristic Parameters
window = 2048 # Window size for processing non-overlapping
ch_mean = 200 # channel mean
window_thesh = 10000 # Check for pixels in window within the tissue region
small_holes = 16 # small holes in the connected component
cell_area_min = 40 # cell area is greater than 40 pixels
overlap_cell_threshold = 75 # connected components > 75 px are more than one cell
cell_radius = 4 # cell radius


# Loop row,col for non-overlapping moving window processing
for row in range(0, w, window):
    # print(row,w)
    for col in range(0, h, window):      
        # Check window size within image dimensions
        if row + window-1 < w:
            row_end = row + window - 1
        else:
            row_end = w - 1
        if col + window - 1 < h:
            col_end = col + window - 1
        else:
            col_end = h - 1
        im1 = im[row : row_end, col : col_end, :] # Get image window
                
        # Check: #pxls for image window channel-mean < 200 is higher than 100000 
        im1_new = np.mean(im1, 2) # O/P is a gray scale image for channel mean
        # io.imshow(im1_new<200)
        # plt.show()
        if np.sum(im1_new < ch_mean) > window_thesh:
            im1_inv_gray = 255 - im1_new # invert the image
            thresh = threshold_otsu(im1_inv_gray) # dynamic threshold per tile
            binary = im1_inv_gray > thresh # binarize the iamge on OTSU threshold

            inv_im1_hole = skimage.morphology.remove_small_holes(binary, small_holes) # remove samll hole less tha 16 px
            inv_im1_mod = skimage.morphology.remove_small_objects(inv_im1_hole, min_size=cell_area_min) # remove samll objects less tha 40 px, these are not cells
        
            # Label the image to get all the connected components
            lbl_im1, cnt = measure.label(inv_im1_mod, connectivity=1, return_num=True )

            objects = skimage.measure.regionprops(lbl_im1) # objects in the connected components
            big_objects = [obj for obj in objects if obj['area'] > overlap_cell_threshold] # bigger components are separated to decomposed
            singular_cell_obj = [obj for obj in objects if (obj['area'] <= overlap_cell_threshold and obj['area'] > cell_area_min)] # these are single cells

            # Iterate to get the centriods of single cells
            for p in range(len(singular_cell_obj)):
                pts_all.append(np.int64(singular_cell_obj[p].centroid) + [row, col])
            
            # Iterate to decompose larger components
            for p in range(len(big_objects)):
                
                ## !OPTIONAL: If we need bounding boxes
                # pgon = Polygon(
                #     [(big_objects[p].bbox[0], big_objects[p].bbox[1]),
                #     (big_objects[p].bbox[0], big_objects[p].bbox[3]),
                #     (big_objects[p].bbox[2], big_objects[p].bbox[3]),
                #     (big_objects[p].bbox[2], big_objects[p].bbox[1])])

                # Calculate number of cells to be fitted in the component
                num_obj = np.int64(np.ceil(big_objects[p].area / (2 * np.pi * cell_radius * cell_radius)))

                # Fit same no. of GMMs in the component as the number of cells that can be fitted
                pgon_pts = big_objects[p].coords
                gmm_model, cluster_labels = gmm_fn(pgon_pts, n_components = num_obj)

                # Each component is a single cell, get the centroids
                for pc in range(len(gmm_model.means_)):
                    pts_all.append(np.int64(gmm_model.means_[pc,:] + [row, col]))


pts_all_arr = np.array(pts_all)

# Write out to CSV all the centriods
df = pd.DataFrame(pts_all_arr)
df.to_csv(fName[0:-3] + 'csv',index = False ,  header = False)




