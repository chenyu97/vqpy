#  Compared SQL Query

To run the example, please first install the python dependencies listed in requirements.txt and download the following data and models:

- Create the following directories:
  - vqpy/examples/aicity_query/data/checkpoints/CLIP_recogition_color/
  and then download the [model](https://drive.google.com/drive/folders/1J6zSRS7ubWinO9BxKIt7e8lI2Z1zD6g2), which should be placed in the above directory.

- Download [Banff](link), [Jackson](link) and [Southampton](link), and put them in the directory `Three_Datasets`. Ensure that `Three_Datasets` and the root directory `vqpy` are at the same level.

- When running the example as the script, the command should look like:
  - To run vqpy to query red car, use: 
  `python Q1_Query_Red_Car.py`
  - To run vqpy to query speeding car, use: 
  `python Q2_Query_Speeding_Car.py`
  - To run vqpy to query red speeding car, use:
  `python Q3_Query_red_speeding_car.py`