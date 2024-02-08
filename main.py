import logging
import datetime
import json
import configparser
from clean import *

project_dir = os.path.dirname(os.path.abspath(__file__))
now=datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

# Import paths to clean from JSON
with open(os.path.join(project_dir, "config.json")) as f:
    data = json.load(f)

# Import configurations
config=configparser.ConfigParser()
config.read(os.path.join(project_dir, "config.ini"))
log_path=config["Logging"]["log_path"]
log_name=config["Logging"]["log_name"] + now

# Configure the logging settings
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s", datefmt="%Y/%m/%d %H:%M:%S",
                handlers=[logging.FileHandler("{0}/{1}.log".format(log_path, log_name)),logging.StreamHandler()])


if __name__ == "__main__":
    for i in range(len(data)):
        master_path = data[i]["master_path"]
        delete_folder_str_list = data[i]["delete_folder_str_list"]
        for delete_folder_str in delete_folder_str_list:
            clean_obj = clean(master_path, delete_folder_str)
            clean_obj.remove_files_and_subdirectories()