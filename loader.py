import mapper
import driver
import subprocess
import os

def hex_to_file():
    bin_mapper = bytes.fromhex(mapper.mapper)
    bin_driver = bytes.fromhex(driver.driver)
    with open("mapper.exe", "wb") as file:
        file.write(bin_mapper)
        file.close()
    with open("driver.sys", "wb") as file:
        file.write(bin_driver)
        file.close()

def load_drv():
    run_arg = [
        'mapper.exe',
        'driver.sys'
    ]
    p = subprocess.run(run_arg, capture_output=True)
    print(p.stdout.decode())
    os.remove("mapper.exe")
    os.remove("driver.sys")

def run():
    hex_to_file()
    load_drv()

if __name__ == "__main__":
    run()