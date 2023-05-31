# Challenge Of Doom: App Challenge 2023

# Downloading the program
<ol>
    <li>TODO: Use PyInstaller and InstallForge to create the builder</li>
    x, y, z
    <li>Cloning the github repository</li>
    Alternatively, you could go to our github repository (linked <a href=https://github.com/EchoCodez/ChallengeOfDoom>here</a>) and clone it from here.<br>
    On windows:<br>
    Go to the code button on the top right:<br><br>
    <img src="random/code_button.png"><br><br>
    Click on it and select download zip<br><br>
    <img src="random/download_zip.png"><br><br>
    Now navigate to the zipped file and click extract all. Remember your extracted location.<br><br>
    <img src="random/extract_zip.png"><br><br>
    Now open a new window in Visual Studio Code (download <a href="https://code.visualstudio.com/download">here</a>). Click open folder.
    <img src="random/open_folder_vscode.png"><br><br>
    Click on the folder you extracted the github repository too. You have officially cloned the repository!<br>
    Note: To run the program, all you need to do now is open <code>code/main.py</code> and run it.
</ol>

# Directory Structure
```bash
.
├── .gitignore
├── README.md
├── code
│   ├── api
│   │   ├── api.py
│   │   └── diagnosis.py
│   ├── log
│   │   ├── health_log.py
│   │   ├── meal.jpg
│   │   └── test.py
│   ├── main.py
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
├── main.spec
└── random
    ├── code_button.png
    ├── download_zip.png
    ├── extract_zip.png
    └── open_folder_vscode.png
```

# Parts and Pieces
To check out what each folder does, read its respective `FolderDescription.md`

# Libraries and tools used
<ul>
    <li>Python 3.11.2</li>
    <li>Github</li>
    <li>tkinter</li>
    <li>customtkinter</li>
    <li>json</li>
    <li>os and sys</li>
    <li>Other libraries like: typing, io, and dataclasses</li>
</ul>
