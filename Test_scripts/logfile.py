import random
import time

def write_coordinates_to_logfile(logfile_path):
    with open(logfile_path, "w") as f:
        while True:
            x = random.randint(0, 100)
            y = random.randint(0, 100)
            z = random.randint(0, 100)
            f.write(f"{x} {y} {z}\n")
            f.flush()  # flush the buffer to ensure immediate writing to file
            time.sleep(0.1)

def read_coordinates_from_logfile(logfile_path):
    while True:
        with open(logfile_path, "r") as f:
            for line in f:
                x, y, z = map(int, line.strip().split())
                # update the 3D window with the coordinates here
            time.sleep(1)

# example usage
logfile_path = "coordinates.log"
write_coordinates_to_logfile(logfile_path)
# run the read_coordinates_from_logfile function in another terminal or process
