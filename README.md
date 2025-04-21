# FullstackAddon
![GitHub Repo stars](https://img.shields.io/github/stars/zachariahsharma/FullstackAddon)

Fusion 360 Add-In to automate the CAM process for 2D plates.

## Features

- Automatic import of STEP files based on MongoDB task definitions
- 2D true-shape nesting arrangement of parts using Fusion’s Arrange2D solver
- CAM setup generation with stock and work coordinate system configured via customizable templates
- Cleanup of empty or invalid toolpaths to streamline machining operations 
- Post-processing of toolpaths into NC programs for drills and profiles using Laguna templates 
- Continuous polling of a MongoDB `tasks` collection to orchestrate the entire pipeline

## Prerequisites

- Autodesk Fusion 360 with API support.  
- MongoDB running on `mongodb://127.0.0.1:27017/` with:
  - A `jira.tasks` collection containing task documents with `Status: "primed"`.  
  - A `jira.imported` collection defining parts and quantities 
- Python 3.x (used by Fusion’s embedded Python interpreter).  
- The Python `pymongo` package (automatically installed by the add‑in) 

## Installation

1. Clone this repository or download the ZIP.  
2. Copy the `FullstackAddon` folder into your Fusion 360 Add-Ins directory:  
   - **Windows**: `%appdata%\Autodesk\Autodesk Fusion 360\API\AddIns\`  
   - **macOS**: `~/Library/Application Support/Autodesk/Autodesk Fusion 360/API/AddIns/`
3. Edit `config.py` to set:  
   - `STEPBASEPATH`: directory for imported STEP files.  
   - `MMGBASEPATH`: directory for NC program outputs.  
4. Ensure MongoDB is running locally.  
5. Launch Fusion 360, open **Scripts and Add-Ins**, and run **FullstackAddon** 

## Configuration

Update `config.py` to adjust:

```python
DEBUG = True
ADDIN_NAME = 'FullstackAddon'
COMPANY_NAME = 'ACME'
STEPBASEPATH = '/path/to/step/files'
MMGBASEPATH = '/path/to/output/nc_files'
```

## Usage
	1.	Insert new task documents into jira.tasks with fields:
	•	Status: "primed"
	•	Parts: list of part IDs defined in jira.imported
	•	height, width, machine, Material, Thickness, depth, name
	2.	The add‑in polls every 60 seconds, processes primed tasks, and updates their status to "cammed".  ￼

## Pipeline Overview
	1.	importFiles: Imports STEP files into the current Fusion design  ￼
	2.	AutoArrange: Applies a 2D nesting arrangement to all imported occurrences  ￼
	3.	SetupGenerator: Creates CAM setups based on machine/material templates  ￼
	4.	DeleteToolpaths: Deletes empty or invalid toolpaths  ￼
	5.	export (NewNCProgram): Post‑processes toolpaths into NC files  ￼

## Project Structure
```
FullstackAddon/
├── Fullstack.py          # Entry point: polls tasks & orchestrates execution
├── config.py             # Global configuration variables
├── commands/
│   └── Execute.py        # Main execution pipeline for individual tasks
├── lib/
│   ├── fusionAddInUtils/   # Utilities for event handling & logging
│   ├── AutoArrange.py
│   ├── DeleteToolpaths.py
│   ├── ImportModules.py
│   ├── MultiImport.py
│   ├── NewNCProgram.py
│   └── SetupGenerator.py
└── lib/templates/         # CAM template files for HSM post‑processing
```

## Acknowledgements
	•	Autodesk Fusion 360 API and sample code  ￼ ￼
	•	Portland CNC’s STEP import utilities (adapted)  ￼
