#!/bin/python3

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
                    label = singleIssue.fields.labels[0].replace('-', ' ')
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
                        time_log = worklog.timeSpent
                self.entries.append([id,label,int(total_time)])
    
    def create_timesheet(self):
        xfile = openpyxl.load_workbook(self.xlsx_template)
        sheet = xfile.get_sheet_by_name('Sheet1')
        sheet['D10'] = self.name
        start_of_the_week = date.today() - timedelta(days=4)
        sheet['I10'] = start_of_the_week.strftime("%-d-%b")
        sheet['C26'] = self.manager
        sheet['I29'] = self.date

        # week hours table
        sheet['D16'] = datetime.today() - timedelta(days=4)
        sheet['E16'] = "7.5"
        sheet['D17'] = datetime.today() - timedelta(days=3)
        sheet['E17'] = "7.5"
        sheet['D18'] = datetime.today() - timedelta(days=2)
        sheet['E18'] = "7.5"
        sheet['D19'] = datetime.today() - timedelta(days=1)
        sheet['E19'] = "7.5"
        sheet['D20'] = datetime.today()
        sheet['E20'] = "7.5"
        sheet['D21'] = datetime.today() + timedelta(days=1)
        sheet['D22'] = datetime.today() + timedelta(days=2)

        # weekly total
        sheet['I16'] = "37.5"
        sheet['I17'] = "37.5"
        sheet['I18'] = "0"

        # main table
        row = 6
        for task in self.entries:
            sheet[f'M{row}'] = task[0]
            sheet[f'T{row}'] = task[2]
            row += 1


        xfile.save(join(f'{getcwd()}/output', f'{self.name}-{self.date}-timesheet.xlsx'))


if __name__ == "__main__":
    ts = timeSheet()
    ts.get_issues_by_project()
    ts.create_timesheet()
