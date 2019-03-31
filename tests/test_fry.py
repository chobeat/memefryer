from pkg_resources import ResourceManager
from memefryer import Fryer
import os
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter
def test_e2e(datadir):

    image_path=os.path.join(
        datadir,"lenna.png"
    )

    Fryer().fry_from_file(image_path,"/tmp/output.png")

def test_e2e_random(datadir):

    image_path=os.path.join(
            datadir,"lenna.png"
    )

    Fryer().fry_from_file(image_path,"/tmp/output.png", random_transformations=True)

def test_find_hands(datadir):
    image_path=os.path.join(
            datadir,"hand.jpg"
    )

    assert len(Fryer()._find_hands(Image.open(image_path)))==1



def test_e2e_hand(datadir):
    image_path=os.path.join(
            datadir,"hand.jpg"
    )

    Fryer().fry_from_file(image_path,"/tmp/hand.png")