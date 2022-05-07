#!/usr/bin/env python3
import sys
import subprocess
import logging
import json

logging.basicConfig(
    level=logging.DEBUG
)
logger = logging.getLogger(__name__)
logger.setLevel(
    logging.DEBUG
)
lgd = logger.debug
lgw = logger.warning

is_error = False
fan_data = {}

max_now = 0
max_max = 0

def get_display_label () -> str:
    # lgd(f'fan data is {fan_data}')
    f1 = get_fan_speed_display('fan1')
    f2 = get_fan_speed_display('fan2')
    return f'{f1} : {f2}'

def output_main_info():
    output = {
        'text': get_display_label(),
        'class': get_fan_speed_class()
    }
    sys.stdout.write(json.dumps(output)+ '\n')
    sys.stdout.flush()
    return output

def get_fan_speed(f: dict, k: str) -> tuple[int,int,int]:
    (s_now,s_min,s_max) = (0,0,0)
    if k == 'fan1':
        s_now = int(f['fan1_input'])
        s_min = int(f['fan1_min'])
        s_max = int(f['fan1_max'])
    if k == 'fan2':
        s_now = int(f['fan2_input'])
        s_min = int(f['fan2_min'])
        s_max = int(f['fan2_max'])
    return (s_now,s_min,s_max)

def get_fan_speed_display(k) -> str:
    global max_now
    global max_max
    if not k in fan_data:
        return "no data..."
    f = fan_data[k]
    [s_now,s_min,s_max] = get_fan_speed(f, k)
    if s_now > max_now:
        max_now = s_now
    if s_max > max_max:
        max_max = s_max
    # lgd(f'f is {f}')
    return f'{s_now}/{s_max}'

def get_fan_speed_class() -> str:
    cls = "low"
    p = int((max_now / max_max) * 100)
    if p > 55:
        cls = "medium"
    if p > 85:
        cls = "high"
    return cls

def get_fan_speed_data():
    global is_error
    global fan_data
    process = subprocess.Popen(
        "sensors -j",
        shell=True,
        stdout=subprocess.PIPE
    )
    try:
        out = process.communicate()[0].decode()
        data = json.loads(out)["applesmc-acpi-0"]
        fan_data['fan1'] = data['fan1']
        fan_data['fan2'] = data['fan2']
        # lgd(f'out is {data}')
    except Exception as e:
        lgw(f'error {e}')
        is_error = True

def main():
    # lgd('run script')
    get_fan_speed_data()
    output_main_info()

if __name__ == '__main__':
    main()


