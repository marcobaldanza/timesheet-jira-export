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

### Jira Access Token
You need to create a [Jira access token](https://id.atlassian.com/manage-profile/security/api-tokens) in order for the code to authenticate with Jira

 1. Login to Jira
 2. Click (top right) cog
 3. Select 'Atlassian account settings'
 4. Select 'Security'
 5. Under **API tokens** select 'Create and manage API tokens'
 6. Click 'Create API Token'
 7. Give it a label and click 'Create'
 8. Copy the token text and paste into your config.conf file

New export will be found in the output folder.

### Note

 - The code is looking for a label for all tasks, if there is no label then the Jira task is skipped. This is for future logic of automatically selecting the correct column in the timesheet template.
 - All time will currently be logged under System Review until the logic is added to select the correct column
 - The code assumes it is being run on a Friday, so it can accurately calculate dates.


### Todo
 - Only account for logs added that week
 - Add calculation for BAU row
 - Enable running on any day of the week
 - Add hours to the correct column depending on task label 