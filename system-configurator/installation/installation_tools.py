import subprocess
from typing import List

from logger import Logger, LoggerStatus

logger = Logger()

class Executer:
    def execute_command(command: List[str], action_description: str, cwd: str = None):
        """
        Executes a system command and logs the outcome.

        :param command: List of command arguments.
        :param action_description: Description of the action being performed.
        :param cwd: Directory to run the command in (optional).
        """
        try:
            result = subprocess.run(command, cwd=cwd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                    text=True)
            logger.add_record(f"[+] {action_description} succeeded", status=LoggerStatus.SUCCESS)
            if result.stdout:
                logger.add_record(f"Output: {result.stdout.strip()}", status=LoggerStatus.SUCCESS)
            if result.stderr:
                logger.add_record(f"Error: {result.stderr.strip()}", status=LoggerStatus.FAILURE)
        except subprocess.CalledProcessError as e:
            logger.add_record(f"Failed to {action_description}: {e.stderr.strip()}", status=LoggerStatus.FAILURE)
        except Exception as e:
            logger.add_record(f"Unexpected error during {action_description}: {str(e)}", status=LoggerStatus.FAILURE)