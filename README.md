# NISSL-Cell-Detection
Detection of Cells in NISSL stained Brain images

<details>
  <summary> $${\color{magenta} Requirements}$$ </summary>

  + Python 3.7+
  + scikit-image
  + scikit-learn
  + matplotlib
  + pandas
  + pathlib
  + os
  + sys
  + shapely
  + numpy
  + $${\color{orange}KAKADU (!Optional) }$$
  
</details>


The package contains two files:
1. ```cell_functions_new_tiles.py ```
2. ```display_results.py ```

<details>
  <summary> $${\color{yellow}Running\ cell\_functions\_new\_tiles.py}$$ </summary>
  
  + $${\color{red}Input}$$: ```Image File (tiff/jp2)```
  
  + $${\color{green}Output}$$: ```CSV for the cell centers in the image```
  
  + $${\color{lightblue}Usage}$$: ``` python3 .\cell_functions_new_tiles.py .\test_image.tif ```
  
</details>

<details>
  <summary> $${\color{yellow}Running\ display\_results.py}$$ </summary>
  
  + $${\color{red}Input}$$: ```Image File (tiff/jp2)```, ```CSV for the cell centers in the image```
  
  + $${\color{green}Output}$$: ```Image with cell centers```
  
  + $${\color{lightblue}Usage}$$: ``` python3 .\display_results.py .\test_image.tif ```
  
</details>

## Description of the Algorithm

$${\color{red}Input}$$: ```Image File (tiff/jp2)```

To use JPEG-2000 encoded images, the temp folder must be created in the working directory.<br>
KAKADU (https://kakadusoftware.com/) is required for decoding JPEG-2000 ( _.jp2_ ) images. <br>

$${\color{green}Output}$$: ```CSV for the cell centers in the image```

### Pseudocode

+ read the image <br>
   ![image](./assets/test_image1.png)
+ Calculate channel-mean <br>
    ![channel_mean](./assets/channel_mean.png)
+ Invert the image <br>
    ![inverted_image](./assets/image_inv.png)
+ Binarize the Image based on OTSU <br>
    ![binary](./assets/binary.png)
+ Fill the small holes in the image < 16 pixels <br>
    ![small holes](./assets/remove_small_holes.png)
+ Remove small objects less than 40 pixels (these are assumed as not cells) <br>
    ![small objects](./assets/remove_small_objects.png)
+ Find the Connected Components
+ Connected components <= 75 pixels and > 40 pixels, are demarcated as singular cells
    ![singular](./assets/singular_cells.png)
+ Connected components > 75 pixels are demarcated as overlapping cells
+ 
