import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import shutil
import os
import json

script_dir=os.path.dirname(os.path.abspath(__file__))
config_path=os.path.join(script_dir,"config.json")

with open(config_path,"r") as f:
    config= json.load(f)

path=config["Path"]
Categories= config["Categories"]
Ignore=config["Ignore"]

class Handler(FileSystemEventHandler):
    def process(self, file_path):

        print("Processing", file_path)

        file_name = os.path.basename(file_path)
        extension = os.path.splitext(file_name)[1]
        extension = extension.lower()
        parent_folder = os.path.dirname(file_path)
        parent_folder = os.path.normpath(parent_folder)
        watch_path = os.path.normpath(path)


        if os.path.isdir(file_path):
            return

        if extension in Ignore:
            return

        if parent_folder != watch_path:
            return
        

        stable_count = 0
        last_size = -1 # Initally set to -1 to ensure the first check always updates it(always false, especially for empty files)
        
        while stable_count <= 3:
            time.sleep(1)
            # File was deleted/moved by the system during the stability check, this prevents error spams and prevents program from crashing
            if not os.path.exists(file_path):
                return
            try:
                
                file_size = os.path.getsize(file_path)
                if last_size == file_size:
                    stable_count += 1
                else:
                    stable_count = 0
                    last_size = file_size
            except Exception as e:
                print(f"Error checking file : {file_path}: {e}")
                return
# Age check for files, to further categorize into Recent and Old folders(optional, remove quotations to use)
        """try: 
            actual_age = time.time() - os.path.getctime(file_path) # age of file in seconds.
        except FileNotFoundError:
            print(f"File not found")
            return #file got deleted after stability check
        
        if actual_age < 5259600:
                base_dir = os.path.join(path, "Recent")
        else:
            base_dir = os.path.join(path, "Old") """

        for category, extensions in Categories.items():
            
            if extension in extensions:
                destination_path = os.path.join(parent_folder, category)
                os.makedirs(destination_path, exist_ok=True)
                try:
                    shutil.move(file_path, destination_path)
                except Exception as e:
                    print(f"Error moving {file_name}: {e}")
                return

    def on_created(self, event):
        self.process(event.src_path)

    def on_moved(self, event):
        self.process(event.dest_path)

File_Read=Observer()
Event_handler=Handler()

print(f"Scanning existing files in : {path}")
for entry in os.scandir(path):
    if entry.is_file():
        Event_handler.process(entry.path)
print(f"Initial scan complete, starting live monitoring...")


File_Read.schedule(Event_handler,path,recursive=False)
File_Read.start()

print(f"Monitoring directory: {path}")

try:
    while True:
       time.sleep(5)
except KeyboardInterrupt:
    File_Read.stop()

File_Read.join()
