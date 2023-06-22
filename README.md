# Challenge Of Doom: App Challenge 2023
Check out the website of the creators:
- https://jasongrace2282.github.io

#  Downloading the program

- To do: Use PyInstaller and InstallForge to create the builder-

x, y, z

- Cloning the GitHub repository<br>Alternatively, you could go to our GitHub repository (linked <a  href=https://github.com/EchoCodez/ChallengeOfDoom>here</a>) and clone it from here.<br>On Windows:

    1. Go to the code button on the top right:<br> ![Code Button](images/code_button.png)

	2. Click on it and select download zip. <br>![Download Zip](images/download_zip.png)

	3. Now navigate to the zipped file and click extract all. Remember your extracted location.<br> ![Save Extraction Location](images/extract_zip.png)

	4. Now open a new window in Visual Studio Code (download [here](https://code.visualstudio.com/download)). Click open folder.<br> ![Open New Folder in VS Code](images/open_folder_vscode.png)

	5. Click on the folder you extracted the GitHub repository too. You have officially cloned the repository!

    # Running the program
    1. Download python (3.10 or higher preferred) from [here](https://www.python.org/downloads/). Run the installer, and if you are on Windows, make sure to put a check on adding python and pip to your path.
    2. Then open a new terminal in VSCode. ![Open Terminal in VS Code](images/create_new_terminal.jpg)<br>In this terminal, type `pip install poetry`.
    3. After poetry has finished installing, type in the terminal `poetry install`. It should install all required packages.
    4. Navigate to `code/main.py` and run the `py` file. The app should now run and show you a setup scene!
    5. Congratulations, you have now installed and ran the program!

# Directory Structure
```bash
.
├── .gitignore
├── README.md
├── code
│   ├── api
│   │   ├── FolderDescription.md
│   │   ├── __init__.py
│   │   └── diagnosis.py
│   ├── health
│   │   ├── __init__.py
│   │   └── health_log.py
│   ├── main.py
│   ├── medicine
│   │   ├── FolderDescription.md
│   │   ├── __init__.py
│   │   ├── medicine.py
│   │   └── notifications.py
│   ├── setup
│   │   ├── FolderDescription.md
│   │   ├── __init__.py
│   │   ├── setup.py
│   │   ├── setup_questions.py
│   │   └── special.py
│   └── utils
│       ├── FolderDescription.md
│       ├── __init__.py
│       ├── data_classes.py
│       ├── generic.py
│       ├── mcq.py
│       └── parse_json.py
├── images
│   ├── code_button.png
│   ├── create_new_terminal.jpg
│   ├── download_zip.png
│   ├── extract_zip.png
│   └── open_folder_vscode.png
├── json
│   ├── credentials.json
│   ├── logs.json
│   ├── medicines.json
│   ├── preferences.json
│   ├── symptoms.json
│   ├── token.json
│   └── user-data.json
├── poetry.lock
└── pyproject.toml
```

# Parts and Pieces
To check out what each folder does, read its respective `FolderDescription.md`

# Data gathered by us
Rest assured that no data is gathered by our team! Every piece of info you put into this program is stored locally on your computer, so you don't have to worry about our policies regarding your personal info!

# Libraries and tools used
- Python 3.11.2
- GitHub
- tkinter
- customtkinter (and extensions)
- json
- os and sys
- datetime and calendar
- plyer and apscheduler
- typing, io, dataclasses
- hmac, base64, and hashlib
