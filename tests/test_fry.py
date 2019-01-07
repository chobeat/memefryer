from pkg_resources import resource_filename
from memefryer.fryer import Fryer
import os
def test_e2e():
    file_dir=resource_filename("tests","resources")
    image_path=os.path.join(
        file_dir,"lenna.png"
    )

    Fryer().fry_image(image_path,"/tmp/output.png")