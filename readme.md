# Timesheet-Jira-Export

Log all work within Jira against your tickets, run this tool and a spreadsheet is created automatically.


## Install

 1. clone repo
 2. create virtual env e.g. 
	 `virtualenv -p /usr/bin/python3 venv` or `python3 -m venv .`
 3. enter venv 
	 `source venv/bin/activate`
 4. install dependencies 
	 `pip install -r requirements.txt`
 5. rename example-config.conf to config.conf and populate with correct information
 6. run using 
	 `python timesheet.py`

New export will be found in the output folder.

### Note

 - The code is looking for a label for all tasks, if there is no label then the Jira task is skipped. This is for future logic of automatically selecting the correct column in the timesheet template.
 - All time will currently be logged under System Review until the logic is added to select the correct column
 - The code assumes it is being run on a Friday, so it can accurately calculate dates.
