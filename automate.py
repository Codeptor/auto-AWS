from datetime import datetime,timedelta
import logging
from logging.handlers import RotatingFileHandler
import os
from dotenv import load_dotenv
from constants import GITHUB_API,REPOSITORY,UTF8
import http.client
import json
import subprocess


class Automation:
    def __init__(self):
        """_Python script to check for new commits using the GitHub API._
        """
        print("Hello, Thank You for viewing my code.")
        try:
            if self.datetimeUtil():
                self.ManageCredentials()
                gitResp = self.retrieve_latest_commit_date_for_github_repository(in_repository_name=str(REPOSITORY))
                self.log.warning(gitResp)
               
                if gitResp:
                    self.log.warning('Processing for Deployment')
                    self.log.warning('Deployment Script Triggered Successfully')
                    subprocess.Popen('echo "Testing in Server Console using python."', shell=True)
                    subprocess.Popen('pwd', shell=True)