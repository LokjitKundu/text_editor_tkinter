# Text Editor

A simple text editor built using Python and Tkinter, replicating notepad.

## Features

* Create, open, save, and save text files with a new name (Save As)
* Print files using the system print command
* Undo and redo support
* Cut, copy, paste, delete, and select-all operations
* Go To Line navigation
* Zoom In, Zoom Out, and Restore Default Zoom
* Status Bar with line and column tracking
* Dynamic menu state management
  * Cut and Copy are disabled when the editor is empty
  * Paste is disabled when the clipboard is empty
  * Delete is disabled when no text is selected
* Error handling for unsupported file types and text encodings
* Vertical scrollbar for document navigation
* Custom application icon

## Planned Features

The following features are planned for future updates:

* Unsaved File Indicator (*)
* Keyboard Shortcuts

## Screenshot

![PyNote](screenshots/text_editor_screenshot.png)

## Requirements

* Python 3.8+ (tested on Python 3.13.5)

## Run Locally

```bash
git clone https://github.com/LokjitKundu/text_editor_tkinter.git

cd text_editor_tkinter

python run.py
```

## Project Structure

```text
text_editor_tkinter/
│
├── assets/
│   └── text_editor_icon.ico
│
├── screenshots/
│   └── text_editor_screenshot.png
│
├── app.py
│
├── run.py
│
├── LICENSE
│
├── .gitignore
│
└── README.md
```

## Author

Lokjit Kundu