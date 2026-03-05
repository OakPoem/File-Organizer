# File-Organizer
A Python-based file organizer that auto-sorts multiple files into category-wise sub folders via config settings.


This is a File Organizer tool I created using Watchdog to monitor files and organize them accordingly.
This is my first project starting as a beginner in python, so the code may be  unoptimized in some cases.

This was written in python 3.14

This was Originally made for Windows. Although there should be no problems on Linux, due to my limited knowledge of OS, there is no guarantee

You can edit the config file according to your needs to match the amount of folders, the main folder to be monitored, and the extensions you want to filter into said folders.

This is an early learning project and may still have rough edges. Feedback and improvements are welcome.

Installation:
1. CLone the Repo :
    git clone <your-repo-url>
    cd file-organizer
2. Create virtual Enviorment:
    python -m venv .venv
    .\.venv\Scripts\activate
3. Install dependencies: pip install watchdog

4. Run the program by: python File Organiser.py

Stop with ctrl+c in the Terminal associated with the program.
