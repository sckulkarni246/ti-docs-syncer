# Welcome to ti-docs-syncer
This is a Python-based tool which allows **anyone** to download datasheets, TRMs and errata docs for TI's embedded products. You could do the same for analog products as well - fork away!

## Why this tool?

Every once in a while, we end up using a datasheet or TRM which is an older version than what your customer or designer is referring to.
The manual act of downloading newer versions is tedious - especially if you also have a well-defined way of storing docs in a neat folder structure (eg: device_doctype instead of TI nomenclature spruixc, etc.).

Hope this is helpful to you!

## Versions

2025
- 1.4 - 27th April - Modified config for F29x, DRA8x and some TDA4 devices

2024
- 1.3 - 16th August - Support added for commenting entries in config file - creates a dummy sync file explicity now
- 1.2 - 5th August - Merged Selva's contribution - we now check for existence of a doc before downloading a new copy
- 1.1 - 31st July - Accept inputs with only folder name and device name - TRM and ERRATA will be skipped
- 1.0 - 24th July - Base version - first test on a Windows PC - works - takes 15 mins on a fast network

## Pre-requisites
### Software
- Python3
  - Additional Python3 packages (manual)
    - requests (to install, execute `pip3 install requests`)
    - pandas to (install, execute `pip3 install pandas`)
  - Additional Python3 packages (using requirements.txt)
    - pip3 install -r requirements.txt --proxy=\<if you need a proxy\>

*You are responsible for internet connectvity - we don't check for connectivity in the script*

## Usage

0. **[OPTIONAL]** If you are making a new config, ensure that each row is in the below format - provide the right path path to this new config in `ti-docs-syncer.py`
    - family,device-name,trm-name,errata-name
1. Handle TODOs in `ti-docs-syncer.py` - DO NOT PROCEED WITHOUT THIS!
2. To run the script, execute: `python3 ti-docs-syncer.py`
3. Observe logs!

**NOTE: Do not delete folders or docs manually unless absolutely necessary. If you need to do this, also delete the corresponding entry from the syncFileNames.csv file.**

## Contributors
- Shashank Kulkarni s-kulkarni@ti.com
- Selva Kumaran Rajan - selva@ti.com

Future scope

- We always download the datasheet on every run. This can be made conditional.

Have inputs in mind? Send them to s-kulkarni@ti.com (Shashank Kulkarni - EP FAE)
