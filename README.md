# NISSL-Cell-Detection
Detection of Cells in NISSL stained Brain images

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
