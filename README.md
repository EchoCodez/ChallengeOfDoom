# Challenge Of Doom: App Challenge 2023
Check out the website of the creators:
- https://jasongrace2282.github.io

# Downloading the program
<ol>
    <li>TODO: Use PyInstaller and InstallForge to create the builder</li>
    x, y, z
    <li>Cloning the github repository</li>
    Alternatively, you could go to our github repository (linked <a href=https://github.com/EchoCodez/ChallengeOfDoom>here</a>) and clone it from here.<br>
    On windows:<br>
    Go to the code button on the top right:<br><br>
    <img src="images/code_button.png"><br><br>
    Click on it and select download zip<br><br>
    <img src="images/download_zip.png"><br><br>
    Now navigate to the zipped file and click extract all. Remember your extracted location.<br><br>
    <img src="images/extract_zip.png"><br><br>
    Now open a new window in Visual Studio Code (download <a href="https://code.visualstudio.com/download">here</a>). Click open folder.
    <img src="images/open_folder_vscode.png"><br><br>
    Click on the folder you extracted the github repository too. You have officially cloned the repository!<br>
    Note: To run the program, all you need to do now is open <code>code/main.py</code> and run it.
</ol>

# Directory Structure
```bash
.
├── .gitignore
├── README.md
├── code
│   ├── main.py
│   ├── api
│   │   └── diagnosis.py
│   ├── log
│   │   ├── health_log.py
│   │   ├── meal.jpg
│   │   └── test.py
│   ├── medicine
│   │   ├── medicine.py
│   │   └── notifications.py
│   ├── processes
│   │   ├── __init__.py
│   │   └── health_log.py
│   ├── setup
│   │   ├── __init__.py
│   │   ├── setup.py
│   │   └── setup_questions.py
│   └── utils
│       ├── __init__.py
│       ├── data_classes.py
│       ├── generic.py
│       ├── mcq.py
│       ├── parse_json.py
│       └── special.py
├── json
│   ├── conditions.json
│   ├── health
│   │   ├── 09_05_23.json
│   │   ├── 10_05_23.json
│   │   └── 12_05_23.json
│   ├── logs.json
│   ├── medicines.json
│   ├── possible_diseases.json
│   ├── preferences.json
│   ├── symptoms.json
│   └── user-data.json
├── logs
│   └── runlog.log
└── random
    ├── code_button.png
    ├── download_zip.png
    ├── extract_zip.png
    └── open_folder_vscode.png
```

# Parts and Pieces
To check out what each folder does, read its respective `FolderDescription.md`

# Data gathered by us
Rest assured that no data is gathered by our team! Every piece of info you put into this program is stored locally on your computer, so you don't have to worry about our policies regarding your personal info!

# Libraries and tools used
<ul>
    <li>Python 3.11.2</li>
    <li>Github</li>
    <li>tkinter</li>
    <li>customtkinter (and extensions)</li>
    <li>json</li>
    <li>os and sys</li>
    <li>datetime and calender</li>
    <li>plyer and apscheduler</li>
    <li>typing, io, dataclasses</li>
    <li>hmac, base64, and hashlib</li>
</ul>
