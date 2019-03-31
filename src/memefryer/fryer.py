from pkg_resources import resource_listdir, resource_filename
import face_recognition
import os
import random
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter
import numpy as np
import cv2 as cv

class EmojiSet(object):
    emojis_path = None
    emojis = None


    def pick_random_emoji(self):
        position = random.randint(0, len(self.emojis) - 1)
        return os.path.join(self.emojis_path, self.emojis[position])

class FaceEmojiSet(EmojiSet):

    emojis_path = resource_filename("memefryer", "resources/face_emoji")
    emojis = list(filter(lambda x: ".png" in x, resource_listdir("memefryer", "resources/face_emoji")))

class HandEmojiSet(EmojiSet):
    emojis_path = resource_filename("memefryer", "resources/hand_emoji")
    emojis = list(filter(lambda x: ".png" in x, resource_listdir("memefryer", "resources/hand_emoji")))

class _Fryer(object):

    def fry_from_file(self, image_path, output_path, random_transformations=False, with_emoji=True):
        """

        :param image_path: input path of an image
        :param output_path: output path where to save the result
        :param random_transformations: applies some randomness to the result
        :param with_emoji: replace faces with emojis
        :return:
        """
        img = Image.open(image_path)
        img = self.fry_image(img, random_transformations, with_emoji)
        img.save(output_path)

    def fry_image(self,PIL_image, random_transformations=False, with_emoji=True):
        """
        Fries an image
        :param PIL_image: a PIL image to be transformed
        :param random_transformations: applies some randomness to the result
        :param with_emoji: replace faces with emojis
        :return: a fried PIL image
        """
        if with_emoji:
            self._emojify(PIL_image)
        return self._color_transformations(PIL_image, random_transformations)

    def _color_transformations(self, img, random_transformations):
        """
        Apply all the transformations necessary to fry the image
        :param img:
        :param random_operations:
        :return:
        """
        img = self._level_image(img)
        basic_operations = [(ImageEnhance.Contrast, 0.9),
                            (ImageEnhance.Color, 10.0),
                            (ImageEnhance.Contrast, 0.9),
                            (ImageEnhance.Sharpness, 15.0),]

        other_operations = [
            (ImageEnhance.Contrast, 0.9),
            (ImageEnhance.Contrast, 1.2),
            (ImageEnhance.Brightness, 1.25),
            (ImageEnhance.Contrast, 0.9),
            (ImageEnhance.Color, 5.0),
        ]

        if random_transformations:
            random.shuffle(other_operations)

        for operation, value in basic_operations+other_operations:
            img = operation(img).enhance(value)


        return img

    def _emojify(self, img):
        """
        Detects faces and superimposes an emoji over them.
        Returns the path to the new picture, deleting the old one.
        """
        self._emojify_hands(img)
        self._emojify_face(img)
    def _emojify_face(self,img):
        faces = face_recognition.face_locations(np.array(img))

        if len(faces) == 0:
            return img

        for face in faces:
            self._replace_with_emoji(img, face, FaceEmojiSet())

    def _emojify_hands(self,img):
        hands = self._find_hands(img)
        for (x,y,w,h) in hands:
            self._replace_with_emoji(img,(y,x+w,y+h,x) ,HandEmojiSet(), scale_factor=1.0)
        return img

    def _find_hands(self,img):

        file_name= resource_filename("resources","haar_hands.xml")
        file_path= resource_filename("memefryer", "resources")
        hands_detector = cv.CascadeClassifier(os.path.join(file_path,file_name))

        gray = cv.cvtColor(np.asarray(img), cv.COLOR_BGR2GRAY)
        hands = hands_detector.detectMultiScale(gray, 1.3, 5)
        return hands

    def _replace_with_emoji(self, img, face_position, emoji_set, scale_factor=0.20):
        """

        :param img:
        :param face_position:
        :return:
        """
        (top, right, bottom, left) = face_position

        emoji_img = self.get_random_emoji_img(face_position, scale_factor, emoji_set)
        diff_x = int((right - left) * (scale_factor/2))
        diff_y = int((bottom - top) * (scale_factor/2))

        img.paste(emoji_img, (left - diff_x, top - diff_y), mask=emoji_img)

    def get_random_emoji_img(self, face_position, scale_factor, emoji_set):

        (top, right, bottom, left) = face_position
        emoji_path = emoji_set.pick_random_emoji()
        emoji_img = Image.open(emoji_path)
        size_x = int((right - left) * (1 + scale_factor))
        size_y = int((bottom - top) * (1 + scale_factor))
        return emoji_img.resize((size_x, size_y))

    def _level_image(self, img):
        """
        Shamelessly inspired by(copy-pasted from):
        https://stackoverflow.com/questions/3105603/doing-the-same-as-imagemagicks-level-in-python-pil
        :param img:
        :return:
        """
        imgCV = np.asarray(img)
        hsv = cv.cvtColor(imgCV, cv.COLOR_RGB2HSV)
        h, s, v = cv.split(hsv)
        ceil = np.percentile(v, 75)
        floor = np.percentile(v, 25)
        a = 255 / (ceil - floor)
        b = floor * 255 / (floor - ceil)
        v = np.maximum(0, np.minimum(255, v * a + b)).astype(np.uint8)
        hsv = cv.merge((h, s, v))
        rgb = cv.cvtColor(hsv, cv.COLOR_HSV2RGB)
        return Image.fromarray(rgb)
