#  Compared SQL Query

To run the example, please first install the python dependencies listed in requirements.txt, install [norfair](https://github.com/hanryxu/norfair) and download the following data and models:

- Create the following directories:
  - vqpy/examples/aicity_query/data/checkpoints/CLIP_recogition_color/
  and then download the [model](https://drive.google.com/drive/folders/1J6zSRS7ubWinO9BxKIt7e8lI2Z1zD6g2), which should be placed in the above directory.

- Download [Banff](link), [Jackson](link) and [Southampton](link), and put them in the directory `Three_Datasets`. Ensure that `Three_Datasets` and the root directory `vqpy` are at the same level.


- Move the bash file `eval.sh` to the parent directory of root directory `vqpy`, which means that `eval.sh` and the root directory `vqpy` are at the same level. Then use: `bash eval.sh`.