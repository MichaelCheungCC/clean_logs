import logging
import os
import shutil

class clean():
    
    def __init__(self, master_path, delete_path):
        self.master_path = master_path
        self.delete_path = delete_path
        self.total_size_deleted = 0


    def remove_files(self, file_path: str):
        try:
            file_size = os.path.getsize(file_path)
            os.remove(file_path)
            logging.info(f"Deleted file {file_path} with size: {self.convert_size(file_size)}")
            self.total_size_deleted += file_size
        except OSError as e:
            logging.error(f"Error deleting file: {file_path} - {e}")
    
    
    def remove_directories(self, directory_path: str):
        try:
            folder_size = self.get_folder_size(directory_path)
            shutil.rmtree(directory_path)
            logging.info(f"Deleted directory {directory_path} with size: {self.convert_size(folder_size)}")
            self.total_size_deleted += folder_size
        except OSError as e:
            if folder_size - self.get_folder_size(directory_path) > 0: # Handle partial deletion of shutil.rmtree()
                logging.info(f"Deleted partial directory {directory_path} with size: {self.convert_size(folder_size)}")
                self.total_size_deleted += folder_size
            logging.error(f"Error deleting directory: {directory_path} - {e}")
            self.remove_recursion(directory_path)
            
    
    def get_folder_size(self, folder_path: str):
        temp_size = 0
        for path, dirs, files in os.walk(folder_path):
            for f in files:
                file_path = os.path.join(path, f)
                temp_size += os.path.getsize(file_path)
        return temp_size


    def convert_size(self, size):
        """
        Convert folder size according to the order of magnitude
        :param size: int
        """
        size_units = ["bytes", "KB", "MB", "GB", "TB"]
        size_unit_index = 0
        size_in_units = size

        while size_in_units >= 1024 and size_unit_index < len(size_units) - 1:
            size_in_units /= 1024
            size_unit_index += 1

        return str(round(size_in_units)) + " " + size_units[size_unit_index]
            

    def remove_files_and_subdirectories(self):
        """
        Removal of files and subdirectories from all delete_path from master_path
        """
        for root, directories, files in os.walk(self.master_path):
            for directory in directories:
                root_directory = os.path.join(root, directory)
                if self.delete_path == root_directory[-(len(self.delete_path)):]:
                    logging.info(f"Removing files and folders inside: {root_directory}")
                    
                    for i in os.listdir(root_directory):
                        object_path = os.path.join(root_directory, i)
                        if os.path.isfile(object_path):
                            self.remove_files(object_path)
                        else:
                            self.remove_directories(object_path)


    def remove_recursion(self, path):
        """
        Removal of files and subdirectories for recursive handling
        :param size: str
        """
        for root, directories, files in os.walk(path):
            for file in files:
                self.remove_files(os.path.join(root, file))
            for directory in directories:
                root_directory = os.path.join(root, directory)
                logging.info(f"Removing files and folders inside: {root_directory}")
                self.remove_directories(root_directory)


    def __del__(self):
        logging.info(f"Total size deleted in {self.delete_path}: {self.convert_size(self.total_size_deleted)}")



if __name__ == "__main__":
    pass