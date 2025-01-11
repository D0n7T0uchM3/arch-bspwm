import subprocess
from typing import List
import warnings

from logger import Logger, LoggerStatus

logger = Logger()

class GraphicDrivers:
    """
    Deprecated: This class will be removed in future releases.
    Use the new GraphicsManager class instead.
    """
    def __init__(self):
        warnings.warn(
            "GraphicDrivers is deprecated and will be removed in future releases. "
            "Use GraphicsManager instead.",
            DeprecationWarning,
            stacklevel=2
        )

    @staticmethod
    def build():
        """
        Prepares multilib repository and installs hybrid graphic drivers.
        """
        logger.add_record("GraphicDrivers.build() is deprecated and will be removed soon.", LoggerStatus.FAILURE)
        GraphicDrivers.__prepare_multilib()
        GraphicDrivers.__update_multilib_repo()
        GraphicDrivers.__install_hybrid_drivers()

    @staticmethod
    def __install_hybrid_drivers():
        """
        Installs Nvidia and Intel drivers along with necessary Mesa packages.
        """
        logger.add_record("[+] Installing Nvidia & Intel Drivers", status=LoggerStatus.SUCCESS)
        commands = [
            ["sudo", "pacman", "-S", "--noconfirm", "mesa"],
            ["sudo", "pacman", "-S", "--noconfirm", "lib32-mesa"],
            ["sudo", "pacman", "-S", "--noconfirm", "xf86-video-nouveau", "xf86-video-intel", "vulkan-intel"]
        ]
        GraphicDrivers.__execute_commands(commands, "Installing hybrid drivers")

    @staticmethod
    def __prepare_multilib():
        """
        Enables the multilib repository in pacman.conf.
        """
        logger.add_record("[+] Preparing Multilib Repository", status=LoggerStatus.SUCCESS)
        commands = [
            ["sudo", "sed", "-i", "s/^#\\[multilib\\]/[multilib]/", "/etc/pacman.conf"],
            ["sudo", "sed", "-i", "/^\\[multilib\\]$/,/^\\[/ s/^#\\(Include = /etc/pacman.d/mirrorlist\\)/\\1/", "/etc/pacman.conf"]
        ]
        GraphicDrivers.__execute_commands(commands, "Preparing multilib repository")

    @staticmethod
    def __update_multilib_repo():
        """
        Updates the multilib repository.
        """
        logger.add_record("[+] Updating Multilib Repository", status=LoggerStatus.SUCCESS)
        commands = [
            ["sudo", "pacman", "-Sl", "multilib"],
            ["sudo", "pacman", "-Sy", "--noconfirm"]
        ]
        GraphicDrivers.__execute_commands(commands, "Updating multilib repository")

    @staticmethod
    def __execute_commands(commands: List[List[str]], action_description: str):
        """
        Executes a list of system commands with logging and error handling.

        :param commands: List of commands to execute, each command is a list of arguments.
        :param action_description: Description of the action being performed.
        """
        for command in commands:
            try:
                logger.add_record(f"[+] {action_description}: {' '.join(command)}", LoggerStatus.SUCCESS)
                result = subprocess.run(
                    command,
                    check=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
                if result.stdout:
                    logger.add_record(f"Output: {result.stdout.strip()}", LoggerStatus.SUCCESS)
                if result.stderr:
                    logger.add_record(f"Error: {result.stderr.strip()}", LoggerStatus.FAILURE)
            except subprocess.CalledProcessError as e:
                logger.add_record(
                    f"Failed to {action_description.lower()}: {e.stderr.strip()}",
                    LoggerStatus.FAILURE
                )
            except Exception as e:
                logger.add_record(
                    f"Unexpected error during {action_description.lower()}: {str(e)}",
                    LoggerStatus.FAILURE
                )
