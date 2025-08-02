import os

from installation.installation_tools import Executer
from logger import Logger, LoggerStatus

logger = Logger()

class AurBuilder:
    @staticmethod
    def build():
        """
        Clones the yay repository and installs the AUR helper with proper dependency handling.
        """
        aur_repo_url = "https://aur.archlinux.org/yay.git"
        clone_dir = "/tmp/yay"
        
        try:
            Executer.execute_command(
                ["sudo", "pacman", "-S", "--needed", "--noconfirm", "base-devel", "git"],
                "Installing build dependencies"
            )

            if AurBuilder.check_repo_exists(clone_dir):
                logger.add_record(f"[+] yay repository exists in {clone_dir}, updating...", 
                                status=LoggerStatus.SUCCESS)
                Executer.execute_command(
                    ["git", "-C", clone_dir, "pull"],
                    "Updating yay repository"
                )
            else:
                Executer.execute_command(
                    ["git", "clone", aur_repo_url, clone_dir],
                    "Cloning yay repository"
                )

            Executer.execute_command(
                ["makepkg", "-si", "--noconfirm", "--skipinteg"],
                "Installing yay",
                cwd=clone_dir
            )
            
            logger.add_record("[+] yay installed successfully", status=LoggerStatus.SUCCESS)
            
        except Exception as e:
            logger.add_record(
                f"[-] Failed to install yay: {str(e)}", 
                status=LoggerStatus.ERROR
            )
            
            try:
                Executer.execute_command(
                    ["sed", "-i", "'s/!debug/debug/'", "PKGBUILD"],
                    "Disabling debug packages",
                    cwd=clone_dir
                )
                Executer.execute_command(
                    ["makepkg", "-si", "--noconfirm"],
                    "Retrying yay installation without debug",
                    cwd=clone_dir
                )
            except Exception as fallback_error:
                logger.add_record(
                    f"[-] Fallback installation failed: {str(fallback_error)}", 
                    status=LoggerStatus.ERROR
                )
            raise

    @staticmethod
    def check_repo_exists(clone_dir: str) -> bool:
        """
        Checks if the yay repository has already been cloned.
        """
        return os.path.exists(os.path.join(clone_dir, ".git"))
    