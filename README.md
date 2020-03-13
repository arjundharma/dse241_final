# DSE241 Final Project - Terrorism Data Analysis

## Arjun Dharma, Rahil Dedhia, and Thomas Waldschmidt

The source of the data is this Kaggle dataset: https://www.kaggle.com/START-UMD/gtd/

In order to run the notebooks, follow the following steps (requires Python3.6 to be installed):
* Download the dataset from the Kaggle link above into this directory. We couldn't include it in the repo because it is larger than 100MB
* `pip install -r requirements.txt`
* Run the notebook `DSE241_Final.ipynb`. If you run into issues with the geoplots at the end, you need to install conda. If that doesn't work, reference the notebook in `DSE241_TW_Work.ipynb` to see the maps.

In order to run the interactive map visualization, run the following commands (requires Python3.6 to be installed):
* `pip install -r requirements`
* `bokeh serve --show generate_geoviz.p`
