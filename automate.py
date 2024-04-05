import logging
from logging.handlers import RotatingFileHandler
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
import http.client
import json
import subprocess

class Automation:
    def __init__(self):
        """Python script to check for new commits using the GitHub API."""
        print("Hello, Thank You for viewing my code.")
        try:
            self.setup_environment()
            git_response = self.retrieve_latest_commit_date_for_github_repository(REPOSITORY)
            self.handle_deployment(git_response)
        except Exception as e:
            self.log.exception(e)
        finally:
            print('Execution Completed')

    def setup_environment(self):
        """Set up the environment and logger."""
        load_dotenv()
        self.env = os.getenv
        self.log = self.setup_logger(name=self.env('LOGGER'), log_file=self.env('LOG_FILE'), level=self.env('LEVEL'))
        local_now = datetime.utcnow() + timedelta(hours=5, minutes=30)
        local_time = local_now.strftime("%H:%M:%S.%f - %D %M,%Y")
        self.log.info(f"[Inside - setup_environment function] Current Time - {local_time}")

    def setup_logger(self, name, log_file, level):
        """Setting Up Logger"""
        formatter = logging.Formatter('%(asctime)s %(name)-8s %(module)s %(lineno)d %(levelname)-8s %(message)s')
        handler = RotatingFileHandler(log_file, maxBytes=120000, backupCount=1, delay=False)
        handler.setFormatter(formatter)
        logger = logging.getLogger(name)
        logger.setLevel(level)
        logger.addHandler(handler)
        return logger

    def handle_deployment(self, git_response):
        """Handle the deployment process."""
        if git_response:
            self.log.warning('Processing for Deployment')
            self.log.warning('Deployment Script Triggered Successfully')
            self.execute_deployment_script()
            self.log.warning('Deployment Script Execution Completed Successfully')
        else:
            self.log.warning('No Deployment')

    def execute_deployment_script(self):
        """Execute the deployment script."""
        subprocess.Popen('echo "Testing in Server Console using python."', shell=True)
        subprocess.Popen('pwd', shell=True)
        subprocess.Popen('ls -la', shell=True)
        subprocess.Popen('cd /home/kinnar/deployment/repo/vlearn_project_ci_cd_pipeline_b4/', shell=True)
        subprocess.Popen('pwd', shell=True)
        subprocess.Popen('ls -l', shell=True)
        subprocess.Popen('sh _deploy.sh', shell=True)

    def retrieve_latest_commit_date_for_github_repository(self, repository_name):
        """Retrieves the date of the last commit for the master branch of the user's GitHub repository."""
        https_conn = http.client.HTTPSConnection(GITHUB_API)
        try:
            self.log.info('Inside retrieve_latest_commit_date_for_github_repository function')
            github_request_path = f"/repos/{self.env('OWNER')}/{repository_name}/commits?page=1&per_page=1"
            self.log.warning(f'github_request_path -> {github_request_path}')

            https_conn.request(url=github_request_path, method='GET', headers=self.get_headers())
            git_api_resp = https_conn.getresponse()
            resp_data = git_api_resp.read().decode(UTF8)
            self.log.warning(f'Status :: {git_api_resp.status}')

            if git_api_resp.status == 200:
                api_resp_object = json.loads(resp_data)
                repo_last_commit_date = self.parse_commit_response(api_resp_object)
                return self.is_new_commit(repo_last_commit_date)
            else:
                message = f"ERROR: Request to GitHub failed with status {git_api_resp.status} and the reason was {git_api_resp.reason}"
                self.log.error(f'Message -> {message}')
                return False
        except Exception as e:
            self.log.exception(e)
            return False
        finally:
            https_conn.close()
            self.log.warning("HTTP Connection Closed Successfully")

    def get_headers(self):
        """Get the headers for the GitHub API request."""
        return {'Authorization': "Bearer " + self.env('ACCESS_TOKEN'), 'Accept': 'application/vnd.github.v3+json', 'User-Agent': self.env('OWNER')}

    def parse_commit_response(self, api_resp_object):
        """Parse the GitHub API response and extract the last commit date."""
        last_commit_ref = api_resp_object[0]['sha']
        last_commit_msg = api_resp_object[0]['commit']['message']
        committed_by = api_resp_object[0]['commit']['committer']['name']
        repo_last_commit_date = api_resp_object[0]['commit']['author']['date']
        repo_last_commit_date = datetime.strptime(repo_last_commit_date, "%Y-%m-%dT%H:%M:%SZ")
        self.log.warning(f'Reference {last_commit_ref[0:7]} | Last Commit Msg -> {last_commit_msg} ::|:: BY - {committed_by} ON - {repo_last_commit_date}')
        return repo_last_commit_date

    def is_new_commit(self, repo_last_commit_date):
        """Check if there is a new commit in the repository."""
        current_time = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
        current_time = datetime.strptime(current_time, "%Y-%m-%dT%H:%M:%SZ")
        interval = current_time - repo_last_commit_date
        seconds = interval.total_seconds()
        minutes = seconds // 60
        self.log.info(f'Interval of Current Time & Last Commit Time :: {interval} Timedelta [ M :: {minutes}]')
        return minutes < 5

def main():
    clsUnit = Automation()
    try:
        print("OK")
    except Exception as e:
        clsUnit.log.exception(e)
    finally:
        return 200, "SUCCESS"

if __name__ == "__main__":
    main()