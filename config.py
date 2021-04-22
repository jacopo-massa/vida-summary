import os

import dropbox
import pandas as pd
from PIL import Image
from dotenv import load_dotenv

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(ROOT_DIR, "data")
CSV_DIR = os.path.join(DATA_DIR, "csv")

IMG_DIR = os.path.join(DATA_DIR, "img")
if not os.path.exists(IMG_DIR):
    os.mkdir(IMG_DIR)
GRID_DIR = os.path.join(IMG_DIR, "grid")
if not os.path.exists(GRID_DIR):
    os.mkdir(GRID_DIR)

DATASET_FILE = os.path.join(CSV_DIR, "dataset.csv")
CATEGORIES_FILE = os.path.join(CSV_DIR, "categories.csv")
CROSSCAT_FILE = os.path.join(CSV_DIR, "cross_categories.csv")
SUBCAT_FILE = os.path.join(CSV_DIR, "sub_categories.csv")
DATACAT_FILE = os.path.join(CSV_DIR, "data_cat.csv")
ISOMAP_FILE = os.path.join(CSV_DIR, "isomap.csv")

# build pandas dataframes from csv files
cat = pd.read_csv(CATEGORIES_FILE, index_col=0)
data = pd.read_csv(DATASET_FILE, index_col=0)
data_cat = pd.read_csv(DATACAT_FILE, index_col=0)
cross_cat = pd.read_csv(CROSSCAT_FILE, index_col=0)
sub_cat = pd.read_csv(SUBCAT_FILE, index_col=0)
isomap_df = pd.read_csv(ISOMAP_FILE, index_col=0)


# Load env variables
# if hosted on Heroku, need to set up CONFIG VARIABLES !!!
load_dotenv(os.path.join(ROOT_DIR, ".env"))

# DROPBOX settings
DB_DIR = "img/"
dbx = dropbox.Dropbox(os.environ['DROPBOX_ACCESS_TOKEN'])


def zoomable(zoom_x=True, zoom_y=True):
    return dict(yaxis={'fixedrange': not zoom_y}, xaxis={'fixedrange': not zoom_x})


def get_image_path(img_name, grid=False):
    which = GRID_DIR if grid else IMG_DIR
    path = os.path.join(which, img_name + ".png")

    if not os.path.exists(path):
        dbx_path = DB_DIR + ("grid/" if grid else "") + img_name + ".png"
        with open(path, "wb") as f:
            _, res = dbx.files_download(path=dbx_path)
            f.write(res.content)

    return path


def get_image(img_name, grid=False):
    path = get_image_path(img_name, grid)
    return Image.open(path)


if __name__ == '__main__':
    pass