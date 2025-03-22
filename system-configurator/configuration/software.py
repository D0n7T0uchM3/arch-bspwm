import os

from installation.installation_tools import Executer
from logger import Logger, LoggerStatus

logger = Logger()

class AurBuilder:
    @staticmethod
    def build():
        """
        Clones the yay repository and installs the AUR helper.
        """
        aur_repo_url = "https://aur.archlinux.org/yay.git"
        clone_dir = "/tmp/yay"

        if AurBuilder.check_repo_exists(clone_dir):
            logger.add_record(f"[+] yay repository already exists in {clone_dir}", status=LoggerStatus.SUCCESS)
        else:
            Executer.execute_command(["git", "-C", "/tmp", "clone", aur_repo_url], "Cloning yay repository")

        Executer.execute_command(["makepkg", "-si"], "Installing yay", cwd=clone_dir)

    @staticmethod
    def check_repo_exists(clone_dir: str) -> bool:
        """
        Checks if the yay repository has already been cloned.
        """
        return os.path.exists(clone_dir)
    