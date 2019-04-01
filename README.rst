=========
memefryer
=========

Demand automatically fried memes!
Demand the future!

This library allows you to fry your memes automatically. It offers two basic features: a randomized frying filter and a "detect and superimpose" algorithm for face and hands emojis. Yes, we put emoji faces on top of faces in the photos. 

Dependencies
============

This library depends on opencv and some other packages specified in `requirements.txt`

Basic Usage
===========

```
from memefryer import Fryer
Fryer().fry_from_file(image_path="input.jpg", output_path="output.jpg", random_transformations=False, with_emoji=True)
```
        
===========
