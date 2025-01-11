import subprocess
from typing import List

from logger import Logger, LoggerStatus

logger = Logger()

class PatchSystemBugs:
    @staticmethod
    def enable_all_patches():
        """
        Apply all system patches and fixes.
        """
        PatchSystemBugs.__fix_xterm_error_in_thunar()
        PatchSystemBugs.__make_fish_the_default()
        PatchSystemBugs.__assign_permissions_to_configs()

    @staticmethod
    def __fix_xterm_error_in_thunar():
        """
        Fixes the xterm error in Thunar by symlinking Alacritty to xterm.
        """
        command = ["sudo", "ln", "-sf", "/usr/bin/alacritty", "/usr/bin/xterm"]
        PatchSystemBugs.__run_command(command, "Fixing xterm error in Thunar")

    @staticmethod
    def __make_fish_the_default():
        """
        Sets Fish as the default shell for the user.
        """
        command = ["chsh", "-s", "/usr/bin/fish"]
        PatchSystemBugs.__run_command(command, "Setting Fish as the default shell")

    @staticmethod
    def __assign_permissions_to_configs():
        """
        Recursively assigns permissions (700) to all files in ~/.config.
        """
        command = ["sudo", "chmod", "-R", "700", "~/.config/*"]
        PatchSystemBugs.__run_command(command, "Assigning permissions to config files")

    @staticmethod
    def __run_command(command: List[str], description: str):
        """
        Executes a system command and logs the outcome.

        :param command: The command to be executed as a list of strings.
        :param description: A description of the action being performed.
        """
        try:
            logger.add_record(f"[+] {description}", status=LoggerStatus.SUCCESS)
            result = subprocess.run(
                command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
            )
            if result.stdout:
                logger.add_record(f"Output: {result.stdout.strip()}", status=LoggerStatus.SUCCESS)
            if result.stderr:
                logger.add_record(f"Error: {result.stderr.strip()}", status=LoggerStatus.FAILURE)
        except subprocess.CalledProcessError as e:
            logger.add_record(f"Failed to {description.lower()}: {e.stderr.strip()}", status=LoggerStatus.FAILURE)
        except Exception as e:
            logger.add_record(f"Unexpected error during {description.lower()}: {str(e)}", status=LoggerStatus.FAILURE)