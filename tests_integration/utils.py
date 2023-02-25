import os

from PIL import Image

from definitions import PATH_TO_TESTS_INTEGRATION_IMG, PATH_TO_DOCS


def create_animation(images_path, animation_path, duration=100, loop=0):
    files = sorted(os.listdir(images_path))
    choose_only_png = [os.path.join(images_path, f) for f in files if f.endswith('.png')]

    with Image.open(choose_only_png[0]) as im:
        im.save(animation_path, save_all=True, append_images=[Image.open(picture) for picture in choose_only_png[1:]],
                duration=duration, loop=loop)


animation_path = f"{PATH_TO_DOCS}\\tests_integration_animation.gif"

create_animation(PATH_TO_TESTS_INTEGRATION_IMG, animation_path, duration=1000, loop=0)
