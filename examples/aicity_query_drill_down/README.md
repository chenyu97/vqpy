#  AiCity Query Drill Down

To run the example, please first install the python dependencies listed in requirements.txt and download the following data and models:

- Create the following directories:
  - `vqpy/examples/aicity_query/data/checkpoints/CLIP_recogition_color/`
  - `vqpy/examples/aicity_query/data/checkpoints/CLIP_recogition_direction/`
  - `vqpy/examples/aicity_query/data/checkpoints/CLIP_recogition_type/`
  - `vqpy/examples/aicity_query/data/checkpoints/CLIP_recogition_v2_standard_extend/`
  
  and then download the [models](https://drive.google.com/drive/folders/1CivhsX0xGxRda9EkZ6uqM_CMaJV40KMO), which should be placed in the above directories, respectively.
- Create the following directory: `vqpy/examples/aicity_query/input_videos/`, and then download the [video data](link), which should be placed in the above directory.

- Create the following directory: `vqpy/examples/aicity_query/data/train/`, and then download the [image data](link), which should be placed in the above directory.

- Before run the example of aicity_query_drill_down, switch the git branch to `dev_cy_drilldown`, and pip reinstall vqpy.
  - To run compared_CVIP_for_drill_down, use:
  `python compared_CVIP_for_drill_down.py`
  - To run main_vqpy_for_drill_down, modify the `vqpy/vqpy/backend/operator/output_formatter.py` and ensure the output file is `results_vqpy/drill_down_vqpy`. After that, use: 
  `python main_vqpy_for_drill_down.py`
  - To run main_vqpy_annotation_for_drill_down, modify the `vqpy/vqpy/backend/operator/output_formatter.py` and ensure the output file is `results_vqpy_annotation/drill_down_vqpy_annotation`. After that, use: 
  `python main_vqpy_annotation_for_drill_down.py`