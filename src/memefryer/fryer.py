from pkg_resources import resource_listdir, resource_filename
from subprocess import call
import face_recognition
import os
import random
from shutil import copyfile


class Fryer(object):
    # improve the logic to decide the working file
    WORKING_FILE = "/tmp/fried_image"
    def __init__(self):

        self.emojis_path = resource_filename("memefryer", "emoji")
        self.emojis = list(filter(lambda x:".png" in x, resource_listdir("memefryer", "emoji")))

    def fry_image(self, image_path, output_path):
            copyfile(image_path,self.WORKING_FILE)
            self._emojify()
            self._color_filter()
            copyfile(self.WORKING_FILE,output_path)
            os.remove(self.WORKING_FILE)

    def _color_filter(self):
        # It's really a mess of options, but it works.
        call(["mogrify", "-contrast", "-contrast", "-level", "25%", "-modulate", "80,200", "-modulate", "100,150", "-level", "25%", "-contrast", "-contrast", self.WORKING_FILE])

    def _emojify(self):
        """
        Detects faces and superimposes an emoji over them.
        Returns the path to the new picture, deleting the old one.
        """
        faces = face_recognition.face_locations(face_recognition.load_image_file(self.WORKING_FILE))

        if len(faces) == 0:
            return self.WORKING_FILE

        imagemagick_cmd = ["convert", self.WORKING_FILE]

        # compose imagemagick command to add multiple faces
        for face in faces:
            imagemagick_cmd.extend(self._get_params_for_face(face))

        output_path = self.WORKING_FILE + ".composite.jpg"

        imagemagick_cmd.append(output_path)
        call(imagemagick_cmd)

        copyfile(output_path,self.WORKING_FILE)


    def _get_params_for_face(self, face):
        """
        Takes a tuple for the face position, returns a piece of ImageMagick commands.
        """
        (top, right, bottom, left) = face
        # For debug purposes, draw a rectangle over the face
        # draw_str = 'rectangle %d,%d %d,%d' % (left, top, right, bottom)
        # return ["-fill", "green", "-stroke", "black", "-draw", draw_str]
        emoji_path = self._pick_random_emoji()
        # Increase the size by 20%. Account for proper centering.
        scale_factor = 0.20
        size_str = "%dx%d" % ((right - left) * (1 + scale_factor), (bottom - top) * (1 + scale_factor))
        diff_x = (right - left) * (scale_factor / 2)
        diff_y = (bottom - top) * (scale_factor / 2)
        pos_str = "+%d+%d" % (left - diff_x, top - diff_y)
        geometry_str = size_str + pos_str
        return [emoji_path, "-geometry", geometry_str, "-composite"]


    def _pick_random_emoji(self):
        """
        Picks a random emoji among those available
        :return:
        """
        position = random.randint(0, len(self.emojis)-1)
        return os.path.join(self.emojis_path, self.emojis[position])
