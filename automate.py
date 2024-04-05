import asyncio
from github import Github
import os
import logging
from logging.handlers import RotatingFileHandler

class Automation:
    def __init__(self):
        self.setup_logger()
        self.github = Github(os.getenv('ACCESS_TOKEN'))
        self.repo_name = os.getenv('REPOSITORY')
        self.owner = os.getenv('OWNER')

    def setup_logger(self):
        formatter = logging.Formatter('%(asctime)s %(name)-8s %(module)s %(lineno)d %(levelname)-8s %(message)s')
        handler = RotatingFileHandler('automation.log', maxBytes=120000, backupCount=1, delay=False)
        handler.setFormatter(formatter)
        self.logger = logging.getLogger('Automation')
        self.logger.setLevel(logging.INFO)
        self.logger.addHandler(handler)

    async def check_for_new_commits(self):
        try:
            repo = self.github.get_repo(f"{self.owner}/{self.repo_name}")
            latest_commit = repo.get_commits().get_page(0)[0]
            self.logger.info("New commit found: %s", latest_commit)
            await self.deploy()
        except Exception as e:
            self.logger.error("Error checking for new commits: %s", e)

    async def deploy(self):
        try:
            # Perform deployment steps
            self.logger.info("Deploying...")
            # Example deployment steps
            await asyncio.sleep(5)  # Simulate deployment process
            self.logger.info("Deployment completed successfully.")
        except Exception as e:
            self.logger.error("Error during deployment: %s", e)

    async def main(self):
        await self.check_for_new_commits()

if __name__ == "__main__":
    automation = Automation()
    asyncio.run(automation.main())
