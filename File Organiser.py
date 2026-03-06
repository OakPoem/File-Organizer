import time
# Watchdog library Used for monitoring files
from watchdog.observers import Observer #watches file system and assigns events
from watchdog.events import FileSystemEventHandler # responds to events
import shutil # Used for moving files
import os

import json

script_dir=os.path.dirname(os.path.abspath(__file__)) # takes the full file path of the script file(File Organiser.py) and takes its directory(folder) name.
config_path=os.path.join(script_dir,"config.json") # Then it tells the program where config.json is located

# The above setup is required as for a script to work properly, python is executed from the main directory, and it searched for a config.json file in that directory, when in reality the file exisits here, so it gives a 'FileNotFound' type of error


with open(config_path,"r") as f: # opens the config file from the Current working directory only; in read mode(hence "r"), and assigns the file to a variable 'f' and closes file automatically
     config= json.load(f)



    # home_dir=os.path.expanduser('~') # outputs the User's HOME directory(C:\Users) equivalent
    # path=os.path.join(home_dir,"Downloads") # Folder to Monitor

# Dictionary for extension names and the folders they should go to
path=config["Path"]
Categories= config["Categories"]
Ignore=config["Ignore"]

class Handler(FileSystemEventHandler):
    def process(self, file_path): # Watchdog has built in special method name(idk what that means search it up future me)
        
        print("Processing", file_path)
        
        file_name=os.path.basename(file_path) # takes the name of file created in the file path(Ex: abcd.text is full name)
        extension= os.path.splitext(file_name)[1] # splits the name into 2 parts - abcd and .txt, then the [1] selects the .txt part of the name
        extension=extension.lower() # for consistency in handling extension names for different cases(uppercase,lowercase,etc)
        

        # os.path.join combines path(Downloads folder) + category(Folder present in Downloads) so now the program knows where to store the files
        

        # This is called Tuple unpacking and it basically takes the dictionary and distributes it into key:value pairs for every instance of the for loop.
        # so for the below code, it initializes 2 variables-category and extensions, and category is assigned to the keys, while extensions is assigned to values in the dict.
        # Like for the 1st iteration, it basically does: (category=)Images: (extensions=)[".jpg",etc.]

        if os.path.isdir(file_path): # if File is already inside the category sub folder(to prevent infinite loop)
             return

        if extension in Ignore: # if the file is a temproary extension(like a file currently being donwloaded), it will be ignored and the program will stop
                return
        
        parent_folder=os.path.dirname(file_path) # Assigns the folder the file is in 
        parent_folder=os.path.normpath(parent_folder) # Normalizes the parent folder to account for case differences, slashes, etc.
        watch_path=os.path.normpath(path)
        
        if parent_folder != watch_path: # if file is not already in Downloads, strop program. This stops duplicate files which were already categorized from being categorized again upon any sort of modification within those folders.
             return
        
        for category,extensions in Categories.items():

            destination_path= os.path.join(watch_path,category) # This defines the destination folder in accordance to each key value of the dict
             
            if extension in extensions:
                os.makedirs(destination_path,exist_ok=True) # Checks whether the destination folder even exists or not and creates one if it doesnt exist
                shutil.move(file_path,destination_path)
                return
    
    def on_created(self,event):
        self.process(event.src_path)
    
    def on_moved(self,event):
        self.process(event.dest_path)

            
    
File_Read=Observer() # initializes instance of observer to monitor directory with a variable called File_Read
Event_handler=Handler()# sane thing as above but with events
    

File_Read.schedule(Event_handler,path,recursive=False) # Recursive decides whether to watch only the main folder(False) or the main Folder + its Subfolders(True)
File_Read.start()  


# for future me: A try statement is used to give control to the program in way to self handle if errors occur. Ex: If i was playing a game and tried to load a save
#file and that save file was corrupted for some reason, then instead of the entire game crashing without any error message, I just add a (try) statement that 
# basically displays a nice little error box 

# This loop exists to keep the watchdog program alive indefinitely until it is KeyboardInterrupted(ctrl+c)
try:
    while True:
        time.sleep(5) # time interval otherwise its gonna use all of the CPU to constantly monitor
except KeyboardInterrupt:
    File_Read.stop()

File_Read.join( ) # idk whatthis does, think it waits until the observer thread stops to ensure that the program doesnt exit while the observer is still running, which can cause problems
