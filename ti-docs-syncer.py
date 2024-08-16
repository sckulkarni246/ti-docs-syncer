import requests
import csv
import os
import sys
from pathlib import Path
import re
import pandas as pd

# TODO - Step 1: Replace the below with your desired path
prefix_dest = r"C:\Users\a0132277\TI Drive\EPFAE\docs\devices"

# TODO - Step 2: Have your own config file? Replace the below if yes - provide absolute path!
fn_config = "base-config-device-docs.txt"

# function will pass the URL Head request extract the filename from returned URL
def extract_fileName(url):
    response = requests.head(url, allow_redirects=True)
    match = re.search(r'/([^/?]+)\?', response.url)
    if match:
        return match.group(1)
    else:
        return ""

# function stores the fileNames fetched on csv and keep appending
def storeFileNames(string, filename):
    df = pd.DataFrame([string], columns=['syncFileNames'])
    df.to_csv(filename, mode='a', header=False, index=False)


# Global switches - can set to False to reduce verbosity of output
OPT_TEST = True

# Prefix and Suffix URLs/Paths
prefix_common = "https://www.ti.com/"
prefix_ds = "lit/gpn/"
prefix_trm = "lit/pdf/"
prefix_trm_alt = "lit/zip/"
prefix_errata = prefix_trm
suffix_ds = "_ds.pdf"
suffix_trm = "_trm.pdf"
suffix_trm_alt = "_trm.zip"
suffix_errata = "_errata.pdf"
syncFileName = 'syncFileNames.csv'

# we will read file names sync'ed in the past. Id not present, create dummy
try:
    sync_df = pd.read_csv(syncFileName, header=None, names=['syncFileNames'])
except:
    # create dummy dataframe if file not exists
    f_temp=open(syncFileName,'a')
    f_temp.close()
    sync_df = pd.DataFrame(columns=['syncFileNames'])

# We check that the destination is a valid one
if not os.path.exists(prefix_dest):
    print("Check your destination prefix!")
    sys.exit(0)
else:
    print("Destination is valid... proceeding")

# Parse and print config file (only if test option is enabled)
if OPT_TEST == True:
    with open(fn_config) as conffile:
        confreader = csv.reader(conffile, delimiter=",")
        for row in confreader:
            print(",".join(row))

'''
Open the CSV file - for each row repeat the below steps:
    - Create folder named row[0] if it does not exist
    - Fetch PDF named prefix_ds+row[1], write it as row[1]+suffix_ds
    - [If entry exists] Fetch PDF named prefix_trm+row[2], write it as row[0]+suffix_trm
    - [If entry exists] Fetch PDF named prefix_errata+row[3], write it as row[0]+suffix_errata
 '''
tmpfinalpath = ""
with open(fn_config) as conffile:
    confreader = csv.reader(conffile, delimiter=",")
    for row in confreader:
        if(row[0][0] == '#'):
            continue
        print("Syncing " + row[0] + ":" + row[1] + "...")
        tmpfinalpath = os.path.join(prefix_dest, str(row[0]))
        if not os.path.isdir(tmpfinalpath):
            os.makedirs(tmpfinalpath)
        else:
            pass

        # It is assumed that at least datasheet is needed - why else would you have an entry? :)
        tmpdsurl = prefix_common + prefix_ds + row[1]
        tmpdsfilename = Path(tmpfinalpath, row[1] + suffix_ds)
        responseds = requests.get(tmpdsurl)
        tmpdsfilename.write_bytes(responseds.content)

        # There may not be a TRM entry - we handle this
        try:
            tmptrmurl = prefix_common + prefix_trm + row[2]
            tmptrmurl_alt = prefix_common + prefix_trm_alt + row[2]
            extracted_fileName = extract_fileName(tmptrmurl)
            extracted_fileName_alt = extract_fileName(tmptrmurl_alt)
            tmptrmfilename = Path(tmpfinalpath, row[1] + suffix_trm)
            tmptrmfilename_alt = Path(tmpfinalpath, row[1] + suffix_trm_alt)
            # check if we get a blank - this is possible if the TRM is a zipped package
            if(extracted_fileName == ''):
                # TRM is a zippped package - we use alt everywhere
                extracted_fileName = extracted_fileName_alt
                tmptrmurl = tmptrmurl_alt
                tmptrmfilename = tmptrmfilename_alt
                pass
            else:
                # All good, we do nothing
                pass 
            # check if file is in sync with dir
            if not (sync_df['syncFileNames'].str.contains(extracted_fileName).any()):
                print(f"'{extracted_fileName}' is not present in dir. fetching...")
                responsetrm = requests.get(tmptrmurl)
                tmptrmfilename.write_bytes(responsetrm.content)
                storeFileNames(extracted_fileName, syncFileName)
            else:
                print(f"'{extracted_fileName}' is present in dir. skipping...")
        except IndexError:
            print("No TRM data!")

        # There may not be an ERRATA entry - we handle this
        try:
            tmperrataurl = prefix_common + prefix_errata + row[3]
            extracted_fileName = extract_fileName(tmperrataurl)
            tmperratafilename = Path(tmpfinalpath, row[1] + suffix_errata)
            # check if file is in sync with dir
            if not (sync_df['syncFileNames'].str.contains(extracted_fileName).any()):
                print(f"'{extracted_fileName}' is not present in dir. fetching...")
                responseerrata = requests.get(tmperrataurl)
                tmperratafilename.write_bytes(responseerrata.content)
                storeFileNames(extracted_fileName, syncFileName)
            else:
                print(f"'{extracted_fileName}' is present in dir. skipping...")
        except IndexError:
            print("No ERRATA data!")
