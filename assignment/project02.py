"""
use two simultaneously running threads to:

* read Photocell periodically and save to JSON file
* code similar to your project01.py in a second thread simultaneously
"""

import machine
import time
import _thread
<<<<<<< HEAD
from pathlib import Path
import json
=======

>>>>>>> b56a8cb76ed4c485c82fb68f5f7435e85c8b6fbd
import project01

# project01.py also needs to be copied to the Pico

<<<<<<< HEAD
def get_params(param_file: str) -> dict:
    """Reads parameters from a JSON file."""

    param_path = Path(param_file).expanduser()
    if not param_path.is_file():
        raise OSError(f"File {param_file} not found")

    with open(param_file) as f:
        params = json.load(f)

    return params
=======
>>>>>>> b56a8cb76ed4c485c82fb68f5f7435e85c8b6fbd

def photocell_logger(N: int, sample_interval_s: float) -> None:
    """
    get raw uint16 values from photocell N times and save to JSON file

    Parameters
    ----------

    N: int
        number of samples to take
    """

    print("start light measurement thread")

    adc = machine.ADC(28)

    values: list[int] = []

    start_time: tuple[int] = time.localtime()

    for _ in range(N):
        values.append(adc.read_u16())
        time.sleep(sample_interval_s)

    end_time: tuple[int] = time.localtime()
    # please also log the end_time and sample interval in the JSON file
    #  i.e. two additional key, value in the dict

    data = {
<<<<<<< HEAD
        "start_time":start_time,
        "end_time":end_time,
        "sample_interval":sample_interval_s,
=======
>>>>>>> b56a8cb76ed4c485c82fb68f5f7435e85c8b6fbd
        "light_uint16": values,
        "start_time": start_time,
    }

    now: tuple[int] = time.localtime()

    now_str = "-".join(map(str, now[:3])) + "T" + "_".join(map(str, now[3:6]))
<<<<<<< HEAD
    filename = f"proj2-light.json"
=======
    filename = f"proj2-light-{now_str}.json"
>>>>>>> b56a8cb76ed4c485c82fb68f5f7435e85c8b6fbd

    print("light measurement done: write", filename)

    project01.write_json(filename, data)


def blinker_response_game(N: int) -> None:
    # %% setup input and output pins
    led = machine.Pin("LED", machine.Pin.OUT)
<<<<<<< HEAD
    button1 = machine.Pin(16, machine.Pin.IN, machine.Pin.PULL_UP)
    button2 = machine.Pin(0, machine.Pin.IN, machine.Pin.PULL_UP)
    
    # %% please read these parameters from JSON file like project 01 instead of hard-coding
    params = get_params("project02.json")
    sample_ms = params["sample_ms"]
    on_ms = params["on_ms"]

    tl0: list[float | None] = []
    tl1: list[float | None] = []
=======
    button = machine.Pin(16, machine.Pin.IN, machine.Pin.PULL_UP)

    # %% please read these parameters from JSON file like project 01 instead of hard-coding
    sample_ms = 10.0
    on_ms = 500

    t: list[float | None] = []

>>>>>>> b56a8cb76ed4c485c82fb68f5f7435e85c8b6fbd
    project01.blinker(3, led)

    for i in range(N):
        time.sleep(project01.random_time_interval(0.5, 5.0))

        led.high()

        tic = time.ticks_ms()
        t0 = None
<<<<<<< HEAD
        t1 = None
        while time.ticks_diff(time.ticks_ms(), tic) < on_ms:
            if button1.value() == 0:
                t0 = time.ticks_diff(time.ticks_ms(), tic)
                led.low()
                if button2.value() == 0:
                    t1 = time.ticks_diff(time.ticks_ms(), tic)
                    led.low()
                    break
            if button2.value() == 0:
                t1 = time.ticks_diff(time.ticks_ms(), tic)
                led.low()
                if button1.value() == 0:
                    t0 = time.ticks_diff(time.ticks_ms(), tic)
                    led.low()
                    break
        tl0.append(t0)
        tl1.append(t1)
        led.low()
    project01.blinker(5, led)
    project01.scorer(tl0, "proj2-score-player1.json")
    project01.scorer(tl1, "proj2-score-player2.json")


_thread.start_new_thread(photocell_logger, (10, 0.5))
blinker_response_game(10)
=======
        while time.ticks_diff(time.ticks_ms(), tic) < on_ms:
            if button.value() == 0:
                t0 = time.ticks_diff(time.ticks_ms(), tic)
                led.low()
                break
        t.append(t0)

        led.low()

    project01.blinker(5, led)

    project01.scorer(t)


_thread.start_new_thread(photocell_logger, (10, 0.5))
blinker_response_game(5)
>>>>>>> b56a8cb76ed4c485c82fb68f5f7435e85c8b6fbd
