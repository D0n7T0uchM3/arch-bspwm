import subprocess
from typing import List

from logger import Logger, LoggerStatus


class Daemons:
    @staticmethod
    def enable_all_daemons():
        services_to_enable = [
            {"name": "NetworkManager", "start": False},
            {"name": "bluetooth.service", "start": True},
        ]

        for service in services_to_enable:
            Daemons.__manage_service(service["name"], enable=True, start=service["start"])

    @staticmethod
    def __manage_service(service_name: str, enable: bool = False, start: bool = False):
        """
        Enables and/or starts a system service using systemctl.

        :param service_name: Name of the service to manage.
        :param enable: Whether to enable the service.
        :param start: Whether to start the service.
        """

        if enable:
            Daemons.__run_command(["sudo", "systemctl", "enable", service_name], f"Enabling {service_name}")

        if start:
            Daemons.__run_command(["sudo", "systemctl", "start", service_name], f"Starting {service_name}")

    @staticmethod
    def __run_command(command: List[str], action_description: str):
        """
        Executes a system command and logs the outcome.

        :param command: List of command arguments.
        :param action_description: Description of the action being performed.
        """

        try:
            Logger.add_record(f"[+] {action_description}", status=LoggerStatus.SUCCESS)
            result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            Logger.add_record(f"Output: {result.stdout.strip()}", status=LoggerStatus.SUCCESS)
        except subprocess.CalledProcessError as e:
            Logger.add_record(f"Error while {action_description.lower()}: {e.stderr.strip()}",
                              status=LoggerStatus.FAILURE)
        except Exception as e:
            Logger.add_record(f"Unexpected error while {action_description.lower()}: {str(e)}",
                              status=LoggerStatus.FAILURE)
