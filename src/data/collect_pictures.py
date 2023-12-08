import re
import os
import keyboard
import clipboard

from time import sleep, time

from PIL import Image
from pyautogui import click, press, moveTo, hotkey, mouseDown, mouseUp, screenshot


def emulate_shift_left_click(x, y):
    moveTo(x, y)
    keyboard.press("shift")
    click()
    keyboard.release("shift")


def enter_to_filter(text: str):
    click(1400, 160)
    sleep(0.2)
    hotkey("ctrl", "a")
    press("delete")
    hotkey(f"{text[0]}", f"{text[1]}")


def reformat_string(input_string):
    cleaned_string = re.sub("(\n|\r|[a-z])|:", "", input_string)
    parts = cleaned_string.split(" ")[1::]
    id_value = parts[0]
    lat_value = "{:.5f}".format(float(parts[1]))
    lng_value = "{:.5f}".format(float(parts[2]))
    reformatted_string = f"{id_value} {lat_value} {lng_value}"
    return reformatted_string


def rotate_camera() -> None:
    mouseDown(1900, 605)
    moveTo(0, 605, 0.2)
    mouseUp(1900, 605)
    mouseDown(1900, 605)
    moveTo(1605, 605, 0.2)
    mouseUp(1900, 605)


def take_screenshot(x_shift: int = 1425, y_shift: int = 770):
    image = screenshot()
    x, y = 160, 240
    cropped_image = image.crop((x, y, x + x_shift, y + y_shift))
    return cropped_image


def join_pictures_horizontally(pictures):
    widths, heights = zip(*(img.size for img in pictures))
    total_width = sum(widths)
    max_height = max(heights)
    combined_image = Image.new("RGB", (total_width, max_height))
    x_offset = 0
    for image in pictures:
        combined_image.paste(image, (x_offset, 0))
        x_offset += image.width

    return combined_image


def process_game_base(times: int) -> None:
    for j in range(times):
        start_time = time()
        # start game
        click(960, 1000)
        sleep(0.1)
        press("F12")
        sleep(4)

        for i in range(5):
            # click guess
            click(1200, 800)
            sleep(0.5)
            click(1200, 1000)
            sleep(0.5)

            # collect guess data
            enter_to_filter("guess")
            click(1400, 340)
            click(1455, 390)
            click(1475, 575)
            emulate_shift_left_click(1620, 610)
            hotkey("ctrl", "c")

            # process clipboard
            coordinates = clipboard.paste()
            coordinates = reformat_string(coordinates)
            clipboard.copy(coordinates)

            # collect picture data
            enter_to_filter("base")
            click(1400, 340, button="right")
            click(1415, 355)
            click(325, 17)
            click(1000, 600, button="right")
            sleep(0.1)
            click(1015, 640)
            sleep(0.1)
            hotkey("ctrl", "v")
            sleep(0.1)
            press("enter")
            sleep(0.1)
            click(1020, 530)
            sleep(0.2)
            click(1900, 1000)
            click(472, 17)

            # next round
            if i != 4:
                press("F12")
                click(720, 840)
                sleep(0.1)
                press("F12")
                sleep(4)
                continue

            mouseDown(25, 55)
            sleep(0.1)
            mouseUp(25, 55)
            press("F12")
            sleep(1)
            print(f"Collection {j + 1} finished with time: {time() - start_time}s")


def process_game_screenshot(times: int, image_path: str) -> None:
    for j in range(times):
        start_time = time()
        # start game
        click(960, 1000)
        sleep(4.5)

        for i in range(5):
            # take screenshot
            image = screenshot()
            x, y = 160, 240
            x_shift, y_shift = 1425, 770
            cropped_image = image.crop((x, y, x + x_shift, y + y_shift))
            sleep(0.1)

            # click guess
            press("F12")
            sleep(0.1)
            click(1200, 800)
            sleep(0.1)
            click(1200, 1000)
            sleep(0.1)

            # collect guess data
            enter_to_filter("guess")
            click(1400, 340)
            click(1455, 390)
            click(1475, 575)
            emulate_shift_left_click(1620, 610)
            hotkey("ctrl", "c")
            press("F12")

            # process clipboard
            coordinates = clipboard.paste()
            coordinates = reformat_string(coordinates)
            image_name = os.path.join(image_path, f"{coordinates}.png")
            cropped_image.save(image_name)

            # next round
            if i != 4:
                click(720, 840)
                sleep(3.5)
                continue

            mouseDown(25, 55)
            sleep(0.1)
            mouseUp(25, 55)
            print(f"Collection {j + 1} finished with time: {time() - start_time}s")


def process_game_panorama(times: int, image_path: str) -> None:
    for j in range(times):
        start_time = time()
        # start game
        click(960, 1000)
        sleep(4.5)

        for i in range(5):
            # take screenshots
            pictures = []
            for _ in range(3):
                screen = take_screenshot()
                pictures.append(screen)
                rotate_camera()
                sleep(0.7)

            pictures.append(take_screenshot(855, 770))
            panorama = join_pictures_horizontally(pictures)
            sleep(0.2)

            # click guess
            press("F12")
            sleep(0.1)
            click(1200, 800)
            sleep(0.1)
            click(1200, 1000)
            sleep(0.1)

            # collect guess data
            enter_to_filter("guess")
            click(1400, 340)
            click(1455, 390)
            click(1475, 575)
            emulate_shift_left_click(1620, 610)
            hotkey("ctrl", "c")
            press("F12")

            # process clipboard
            coordinates = clipboard.paste()
            coordinates = reformat_string(coordinates)
            image_name = os.path.join(image_path, f"{coordinates}.png")
            panorama.save(image_name)

            # next round
            if i != 4:
                click(720, 840)
                sleep(3.5)
                continue

            mouseDown(25, 55)
            sleep(0.01)
            mouseUp(25, 55)
            print(f"Collection {j + 1} finished with time: {time() - start_time}s")


if __name__ == "__main__":
    NUM_GAMES = 100
    SAVE_PATH = "C:\\Users\\emperor\\PycharmProjects\\lostgamer\\data\\raw\\panorama\\"
    process_game_panorama(NUM_GAMES, SAVE_PATH)
