"""
Morse Code decoder

based on https://github.com/printnplay/Pico-MicroPython/blob/main/MorseCodeCreator.py
"""

from machine import Pin

from pathlib import Path

# need to also copy pathlib.py to the Pico

import time
import json

# Create a dictionary of Morse Code. "." is for Short (dots), "-" is for Long (dashes)
MorseCodes = {
    " ": "",
    "a": ".-",
    "b": "-...",
    "c": "-.-.",
    "d": "-..",
    "e": ".",
    "f": "..-.",
    "g": "--.",
    "h": "....",
    "i": "..",
    "j": ".---",
    "k": "-.-",
    "l": ".-..",
    "m": "--",
    "n": "-.",
    "o": "---",
    "p": ".--.",
    "q": "--.-",
    "r": ".-.",
    "s": "...",
    "t": "-",
    "u": "..-",
    "v": "...-",
    "w": ".--",
    "x": "-..-",
    "y": "-.--",
    "z": "--..",
    "1": ".----",
    "2": "..---",
    "3": "...--",
    "4": "....-",
    "5": ".....",
    "6": "-....",
    "7": "--...",
    "8": "---..",
    "9": "----.",
    "0": "-----",
}


def get_params(param_file: str) -> dict:
    """Reads parameters from a JSON file."""

    param_path = Path(param_file).expanduser()
    if not param_path.is_file():
        raise OSError(f"File {param_file} not found")

    with param_path.open("r") as f:
        params = json.load(f)

    return params


def letterlookup(stringvalue: str) -> str:
    for k in MorseCodes:
        if MorseCodes[k] == stringvalue:
            return k
    return " "


def blinkletter(letter: str, params: dict) -> None:
    """blink LED Morse code letters"""

    led = machine.Pin("LED", machine.Pin.OUT)

    if letter != "":
        currentletter = MorseCodes[letter]
    if letter == " ":
        time.sleep(params["inter_letter_ms"] / 1000.0)
        return

    print(letter + " : " + currentletter)
    for c in currentletter:
        if c == "-":
            blinkspeed = params["blink_slow_ms"] / 1000.0
        if c == ".":
            blinkspeed = params["blink_fast_ms"] / 1000.0

        led.high()
        time.sleep(blinkspeed)
        led.low()
        time.sleep(blinkspeed)

    time.sleep(0.6)


def play(message: str, params: dict) -> None:
    for c in message:
        blinkletter(str.lower(c), params)


def record(params: dict) -> str:
    """capture morse code message from button presses
    we show via the LED the button presses as captured.
    This can help illustrate issues over sample time being too large
    """

    led = machine.Pin("LED", machine.Pin.OUT)
    button = Pin(16, Pin.IN, Pin.PULL_UP)
    letter = ""
    word = ""
    count = 0

    exit_threshold_ms = params["exit_threshold_ms"]
    dot_dash_threshold_ms = params["dot_dash_threshold_ms"]
    Tsample = params["sample_ms"] / 1000.0

    print(f"tap Morse Code message! Wait {exit_threshold_ms / 1000.} seconds to exit")

    tic_char = time.ticks_ms()

    while True:
        if button.value() == 0:
            # Button being pressed
            if count == 0:
                tic_char = time.ticks_ms()
            count += 1
            led.high()
        else:
            toc = time.ticks_ms()
            tdiff = time.ticks_diff(toc, tic_char)
            led.low()
            # Button released, measure if dot or dash
            if count > 0:
                if tdiff < dot_dash_threshold_ms:
                    letter += "."
                else:
                    letter += "-"
            count = 0

            if tdiff > 3 * dot_dash_threshold_ms:
                if letter != "":
                    word += letterlookup(letter)
                    letter = ""
                    print(word)

            if tdiff > exit_threshold_ms:
                print("You recorded " + word)
                print("Exiting recording mode")

                return word

        time.sleep(Tsample)


if __name__ == "__main__":
    params = get_params("exercise03.json")

    # %% play wakeup hello message
    play("hello", params)

    # %% record and playback message
    play(record(params), params)
