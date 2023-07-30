import os
from os.path import splitext, exists, join
from shutil import move
import time
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

#configure logger
logdatetime = time.strftime("%m%d%S")
logging.basicConfig(filename="fileautomator" + logdatetime + ".log",
                    level=logging.INFO, 
                    format='%(asctime)s %(message)s',
                    filemode='w')

#based on file type, send to appropriate folder
path = "/home/anna/Downloads"
imgs_dir = "/home/anna/Pictures"
packages_dir = "/home/anna/Downloads/packages"
samples_dir = "/home/anna/Downloads/samples"

# image types
image_extensions = [".jpg", ".jpeg", ".jpe", ".jif", ".jfif", ".jfi", ".png", ".gif", ".webp", ".tiff", ".tif", ".psd", ".raw", ".arw", ".cr2", ".nrw",
                    ".k25", ".bmp", ".dib", ".heif", ".heic", ".ind", ".indd", ".indt", ".jp2", ".j2k", ".jpf", ".jpf", ".jpx", ".jpm", ".mj2", ".svg", ".svgz", ".ai", ".eps", ".ico"]
# sample types
samples_extensions = [".cpp", ".c", ".py", ".h"]

# pkg types
pkg_extensions = [".deb", ".zip", ".tar"]


#obj = os.scandir(path)

#list all files & directories in path
#for entry in obj:
#    if entry.is_dir() or entry.is_file():
#        print(entry.name)

#if file name exists add "downloaded" to it
def exists_name(dest, name):
    filename, extension = splitext(name)
    
    #if exists add word
    while exists(f"{dest}/{name}"):
        name = f"{filename}_downloaded{extension}"

    return name

#tell python how to move from one dir to another while changing name if it has to
def mv(dest, entry, name):
    if exists(join(dest, name)):
        new_name = exists_name(dest, name)
        move(join(dest, name), join(dest, new_name))
    move(entry, dest)

#class to move files into desired directory
class mv_files(FileSystemEventHandler):
    def on_modified(self, event):
        with os.scandir(path) as obj:
            for entry in obj:
                name = entry.name
                
                self.check_imgs(entry, name)
                self.check_pkgs(entry, name)
                
    def check_imgs(self, entry, name):
        for image_extension in image_extensions:
            if name.endswith(image_extension) or name.endswith(image_extension.upper()):
                mv(imgs_dir, entry, name)
                #log info
                logging.info(f"Moved: {name} to {imgs_dir}")
    def check_pkgs(self, entry, name):
        for pkg_extension in pkg_extensions:
            if name.endswith(pkg_extension) or name.endswith(pkg_extension.upper()):
                mv(packages_dir, entry, name)
                #log info
                logging.info(f"Moved: {name} {packages_dir}")
    def check_pkgs(self, entry, name):
        for samples_extension in samples_extensions:
            if name.endswith(samples_extension) or name.endswith(samples_extension.upper()):
                mv(samples_dir, entry, name)
                #log info
                logging.info(f"Moved: {name} {samples_dir}")

                
                
#have the file running and listening (watchdog)
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    path_dir = path
    event_handler = mv_files()
    observer = Observer()
    observer.schedule(event_handler, path_dir, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
