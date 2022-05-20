#!/usr/bin/env python

"""Snyk JIRA Issues Creator.
Install pysnyk module before running this script using pip install pysnyk.
Usage:
    python snyk-jira-issue-creator.py
Author:
    Virendra Kumar - 19 May 2022
"""
import argparse
import os
from snyk import SnykClient


def parse_command_line_args():
    parser = argparse.ArgumentParser(description="Snyk JIRA Issue Creator")
    parser.add_argument(
        "--orgId", type=str, help="The Snyk Organisation ID", required=True
    )
    parser.add_argument(
        "--projectId", type=str, help="The Snyk Project ID", required=True
    )
    parser.add_argument(
        "--jiraProjectId", type=int, help="The Jira Project ID", required=True
    )
    parser.add_argument(
        "--jiraIssueType", type=int, help="The Jira issue type", required=True
    )
    return parser.parse_args()


def create_jira_issue(project, issue, jira_project, issuetype):
    return project.jira_issues.create(issue.id, {"project": {"id": jira_project}, "issuetype": {"id": issuetype}, "summary": "%s - %s" % (project.name, issue.issueData.title)})



snyk_token = os.environ['SNYK_TOKEN']
args = parse_command_line_args()
org_id = args.orgId
project_id = args.projectId
jira_project_id = args.jiraProjectId
jira_issue_type = args.jiraIssueType

client = SnykClient(snyk_token)
org = client.organizations.get(org_id)
project = org.projects.get(project_id)
issues = project.issueset_aggregated.all().issues
jira_issues = project.jira_issues.all()

snyk_issue_with_jira_issues = list(jira_issues.keys())
print ("Total Snyk Issues With JIRA Issues  = ", len(snyk_issue_with_jira_issues))
for issue in issues:
    if issue.id not in list(jira_issues.keys()):
        print("Creating Jira issue for Snyk issue: %s" % issue.id)
        jira_issue = create_jira_issue(project, issue, jira_project_id, jira_issue_type)
        print("Created: [%s] - [%s]" % (jira_issue["id"], jira_issue["key"]))
    else:
        print("JIRA Ticket already exist for : %s" % issue.id)
