import subprocess
from typing import List

from logger import Logger, LoggerStatus


class AurBuilder:
    @staticmethod
    def build():
        """
        Clones the yay repository and installs the AUR helper.
        """
        aur_repo_url = "https://aur.archlinux.org/yay.git"
        clone_dir = "/tmp/yay"

        if AurBuilder.__check_repo_exists(clone_dir):
            Logger.add_record(f"[+] yay repository already exists in {clone_dir}", LoggerStatus.SUCCESS)
        else:
            AurBuilder.__execute_command(["git", "-C", "/tmp", "clone", aur_repo_url], "Cloning yay repository")

        AurBuilder.__execute_command(["makepkg", "-si"], "Installing yay", cwd=clone_dir)

    @staticmethod
    def __check_repo_exists(clone_dir: str) -> bool:
        """
        Checks if the yay repository has already been cloned.
        """
        return os.path.exists(clone_dir)

    @staticmethod
    def __execute_command(command: List[str], action_description: str, cwd: str = None):
        """
        Executes a system command and logs the outcome.

        :param command: List of command arguments.
        :param action_description: Description of the action being performed.
        :param cwd: Directory to run the command in (optional).
        """
        try:
            result = subprocess.run(command, cwd=cwd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                    text=True)
            Logger.add_record(f"[+] {action_description} succeeded", LoggerStatus.SUCCESS)
            if result.stdout:
                Logger.add_record(f"Output: {result.stdout.strip()}", LoggerStatus.SUCCESS)
            if result.stderr:
                Logger.add_record(f"Error: {result.stderr.strip()}", LoggerStatus.FAILURE)
        except subprocess.CalledProcessError as e:
            Logger.add_record(f"Failed to {action_description}: {e.stderr.strip()}", LoggerStatus.FAILURE)
        except Exception as e:
            Logger.add_record(f"Unexpected error during {action_description}: {str(e)}", LoggerStatus.FAILURE)
