from pkg_resources import resource_filename
from memefryer.fryer import Fryer
import os
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter
def test_e2e():
    file_dir=resource_filename("tests","resources")
    image_path=os.path.join(
        file_dir,"lenna.png"
    )

    Fryer().fry_from_file(image_path,"/tmp/output.png")

def test_e2e_random():
    file_dir=resource_filename("tests","resources")
    image_path=os.path.join(
        file_dir,"lenna.png"
    )

    Fryer().fry_from_file(image_path,"/tmp/output.png", random_transformations=True)

def test_find_hands():
    file_dir=resource_filename("tests","resources")
    image_path=os.path.join(
        file_dir,"hand.jpg"
    )

    assert len(Fryer()._find_hands(Image.open(image_path)))==1



def test_e2e_hand():
    file_dir=resource_filename("tests","resources")
    image_path=os.path.join(
        file_dir,"hand.jpg"
    )

    Fryer().fry_from_file(image_path,"/tmp/hand.png")