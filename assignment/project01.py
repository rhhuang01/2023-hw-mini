"""
Response time - single-threaded
"""

from machine import Pin
import time
import random
import json
<<<<<<< HEAD
from pathlib import Path


def get_params(param_file: str) -> dict:
    """Reads parameters from a JSON file."""

    param_path = Path(param_file).expanduser()
    if not param_path.is_file():
        raise OSError(f"File {param_file} not found")
=======


N: int = 5
sample_ms = 10.0
on_ms = 500
>>>>>>> b56a8cb76ed4c485c82fb68f5f7435e85c8b6fbd

    with open(param_file) as f:
        params = json.load(f)

    return params

def random_time_interval(tmin: float, tmax: float) -> float:
    """return a random time interval between max and min"""
    return random.uniform(tmin, tmax)


def blinker(N: int, led: Pin) -> None:
    # %% let user know game started / is over

    for _ in range(N):
        led.high()
        time.sleep(0.1)
        led.low()
        time.sleep(0.1)


def write_json(json_filename: str, data: dict) -> None:
    """Writes data to a JSON file.

    Parameters
    ----------

    json_filename: str
        The name of the file to write to. This will overwrite any existing file.

    data: dict
        Dictionary data to write to the file.
    """
<<<<<<< HEAD
    
    with open(json_filename, "w") as f:
        json.dump(data, f)
        
def append_json(json_filename: str, data: dict) -> None:
    """Appends data to a JSON file.

    Parameters
    ----------

    json_filename: str
        The name of the file to append data to. If the file doesn't exist, it will be created.

    data: dict
        Dictionary data to append to the file.
    """
    try:
        with open(json_filename, "r") as f:
            existing_data = json.load(f)
        existing_data.update(data)
    except FileNotFoundError:
        existing_data = data

    with open(json_filename, "w") as f:
        json.dump(existing_data, f)
        
def scorer(t: list[int | None],filename="proj1-score.json") -> None:
=======

    with open(json_filename, "w") as f:
        json.dump(data, f)


def scorer(t: list[int | None]) -> None:
>>>>>>> b56a8cb76ed4c485c82fb68f5f7435e85c8b6fbd
    # %% collate results
    misses = t.count(None)
    print(f"You missed the light {misses} / {len(t)} times")

    t_good = [x for x in t if x is not None]
<<<<<<< HEAD

    print(t_good)
    if bool(t_good):
            stats = {
                "min response time": min(t_good),
                "max response time": max(t_good),
                "avg response time": str(sum(t_good) / len(t_good)),
                "score": len(t) - misses,
            }
    else:
            stats = {
                "min response time": None,
                "max response time": None,
                "avg response time": None,
                "score": None,
            }
=======

    print(t_good)

    # add key, value to this dict to store the minimum, maximum, average response time
    # and score (non-misses / total flashes) i.e. the score a floating point number
    # is in range [0..1]
    data = {}
>>>>>>> b56a8cb76ed4c485c82fb68f5f7435e85c8b6fbd

    # %% make dynamic filename and write JSON

    now: tuple[int] = time.localtime()

    now_str = "-".join(map(str, now[:3])) + "T" + "_".join(map(str, now[3:6]))
<<<<<<< HEAD
    

    print("write", filename)

    write_json(filename, stats)
=======
    filename = f"proj1-{now_str}.json"

    print("write", filename)

    write_json(filename, data)
>>>>>>> b56a8cb76ed4c485c82fb68f5f7435e85c8b6fbd


if __name__ == "__main__":
    # using "if __name__" allows us to reuse functions in other script files
<<<<<<< HEAD
    params = get_params("project01.json")
    N = params["N"]
    sample_ms = params["sample_ms"]
    on_ms = params["on_ms"]
=======
>>>>>>> b56a8cb76ed4c485c82fb68f5f7435e85c8b6fbd

    led = Pin("LED", Pin.OUT)
    button = Pin(16, Pin.IN, Pin.PULL_UP)

    t: list[int | None] = []

    blinker(3, led)

    for i in range(N):
        time.sleep(random_time_interval(0.5, 5.0))

        led.high()

        tic = time.ticks_ms()
        t0 = None
        while time.ticks_diff(time.ticks_ms(), tic) < on_ms:
            if button.value() == 0:
                t0 = time.ticks_diff(time.ticks_ms(), tic)
                led.low()
                break
        t.append(t0)

        led.low()

    blinker(5, led)

    scorer(t)
