from pkg_resources import resource_filename
from memefryer.fryer import Fryer
import os
import pytest
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