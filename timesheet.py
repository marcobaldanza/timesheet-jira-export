#!/bin/python3

from calendar import week
import openpyxl
import configparser
from jira import JIRA
from datetime import date, datetime, timedelta
from os.path import exists, join
from os import sys, getcwd


class timeSheet:
    def __init__(self) -> None:
        if not exists("config.conf"):
            sys.exit("config.conf file missing")
        self.config = configparser.ConfigParser()
        self.config.read('config.conf')
        try:
            self.name = self.config['settings']['name']
            self.manager = self.config['settings']['manager']
            self.jira_project = self.config['settings']['jira_project']
            self.jira_token = self.config['settings']['jira_token']
            self.email = self.config['settings']['email']
            self.jira_options = {'server': self.config['settings']['jira_url']}
            self.xlsx_template = f"template/{self.config['settings']['xlsx_template']}"
        except KeyError:
            sys.exit("Required key/values: name, jira_token, email, jira_url, xlsx_template")
        
        self.date = date.today().strftime("%d-%m-%y")
        today = date.today()
        self.start_of_week = today - timedelta(days=today.weekday())
        self.tuesday = self.start_of_week + timedelta(days=1)
        self.wednesday = self.start_of_week + timedelta(days=2)
        self.thursday = self.start_of_week + timedelta(days=3)
        self.friday = self.start_of_week + timedelta(days=4)
        self.end_of_week = self.start_of_week + timedelta(days=6)

        self.jira = JIRA(options=self.jira_options, basic_auth=(
            self.email, self.jira_token))
        
        self.entries = []

    def get_issues_by_project(self):
        # Search all issues mentioned against a project name.
        for singleIssue in self.jira.search_issues(jql_str=f'project = {self.jira_project}'):
            if str(singleIssue.fields.assignee) == self.name and singleIssue.fields.labels:
                try:
                    # label
                    label = singleIssue.fields.labels[0]
                except IndexError:
                    # No label exists
                    pass
                issue = self.jira.issue(singleIssue.key, expand='changelog')
                id = singleIssue.key
                total_time = 0
                for worklog in issue.fields.worklog.worklogs:
                    ## time
                    # split the datetime object by 'T'
                    logdate_spl = worklog.created.split('T')
                    # get just the date from list
                    logdate_str = logdate_spl[0]
                    # convert date string to datetime obj
                    logdate = datetime.strptime(logdate_str, '%Y-%m-%d')
                    # ensure log date is within the last 4 days
                    if logdate.date() >= self.start_of_week:
                        total_time += worklog.timeSpentSeconds / 3600
                self.entries.append([id,label,int(total_time)])
    
    def create_timesheet(self):
        xfile = openpyxl.load_workbook(self.xlsx_template)
        sheet = xfile.get_sheet_by_name('Sheet1')
        sheet['D10'] = self.name
        sheet['I10'] = self.start_of_week.strftime("%d-%b")
        sheet['C26'] = self.manager
        sheet['I29'] = self.date

        # week hours table
        sheet['D16'] = self.start_of_week
        sheet['E16'] = "7.5"
        sheet['D17'] = self.start_of_week + timedelta(days=1)
        sheet['E17'] = "7.5"
        sheet['D18'] = self.start_of_week + timedelta(days=2)
        sheet['E18'] = "7.5"
        sheet['D19'] = self.start_of_week + timedelta(days=3)
        sheet['E19'] = "7.5"
        sheet['D20'] = self.start_of_week + timedelta(days=4)
        sheet['E20'] = "7.5"
        sheet['D21'] = self.start_of_week + timedelta(days=5)
        sheet['D22'] = self.end_of_week

        # weekly total
        sheet['I16'] = "37.5"
        sheet['I17'] = "37.5"
        sheet['I18'] = "0"

        # main table
        row = 6
        week_time_total = 0
        for task in self.entries:
            col_letter = self.find_proj_column(sheet, task[1])
            sheet[f'M{row}'] = task[0]
            sheet[f'{col_letter}{row}'] = task[2]
            week_time_total += task[2]
            row += 1
        sheet[f'M{row}'] = "BAU"
        sheet[f'AE{row}'] = 37.5 - week_time_total


        xfile.save(join(f'{getcwd()}/output', f'{self.name}-{self.date}-timesheet.xlsx'))

    def find_proj_column(self, sheet, label):
        for row_cells in sheet.iter_rows(min_row=4, max_row=4):
            for cell in row_cells:
                if label == str(cell.value):
                    return cell.column_letter

if __name__ == "__main__":
    ts = timeSheet()
    ts.get_issues_by_project()
    ts.create_timesheet()
