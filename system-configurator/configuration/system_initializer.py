from logger import Logger, LoggerStatus
from configuration.software import AurBuilder
import os

from installation import packages
from installation.installation_tools import Executer
from installation.drivers import GraphicDrivers
from installation.patches import PatchSystemBugs
from installation.daemons import Daemons

logger = Logger()

class SystemConfiguration:
    @staticmethod
    def install_packages(package_names: list, aur: bool = False):
        installer = "yay -S --noconfirm"

        for package in package_names:
            Executer.execute_command([installer, package], f"Installation of {package}")

    @staticmethod
    def start(*args):
        logger.add_record(f"[+] Starting assembly. Options {args}", status=LoggerStatus.SUCCESS)
        if args[0]: SystemConfiguration.__start_option_1()
        if args[1]: SystemConfiguration.__start_option_2()
        if args[2]: SystemConfiguration.__start_option_3()
        if args[3]: GraphicDrivers.install()

        Daemons.enable_all_daemons()
        PatchSystemBugs.enable_all_patches()

    @staticmethod
    def __start_option_1():
        SystemConfiguration.__create_default_folders()
        SystemConfiguration.__copy_bspwm_dotfiles()

    @staticmethod
    def __start_option_2():
        Executer.execute_command(["sudo", "pacman", "-Sy"], f"Updates")

    @staticmethod
    def __start_option_3():
        AurBuilder.build()
        SystemConfiguration.install_packages(packages.PACKAGES)
        logger.add_record("[+] Installed BSPWM Dependencies", status=LoggerStatus.SUCCESS)

    @staticmethod
    def __create_default_folders():
        try:
            home_dir = os.path.expanduser("~")
            default_folders = ["Videos", "Documents", "Downloads", "Music", "Desktop"]
            
            for folder in default_folders:
                full_path = os.path.join(home_dir, folder)
                Executer.execute_command(["mkdir", "-p", full_path], f"Creating folder: {folder}")
            
            source_images = "../Images"
            Executer.execute_command(["cp", "-r", source_images, home_dir], "Copying Images folder")
            
            logger.add_record("[+] Created default directories", status=LoggerStatus.SUCCESS)
        except Exception as e:
            logger.add_record(f"[-] Failed to create default directories: {str(e)}", status=LoggerStatus.ERROR)
            raise

    @staticmethod
    def __copy_bspwm_dotfiles():
        try:
            home_dir = os.path.expanduser("~")
            items_to_copy = [
                ("../Xresources", ".Xresources"),
                ("../gtkrc-2.0", ".gtkrc-2.0"),
                ("../xinitrc", ".xinitrc"),
                ("../.bin/", ".bin"),
                ("../.config/", ".config")
            ]
            
            for source_path, dest_name in items_to_copy:
                dest_path = os.path.join(home_dir, dest_name)
                
                recursive = True if source_path.endswith('/') or os.path.isdir(source_path) else False
                cmd = ["cp", "-r"] if recursive else ["cp"]
                
                Executer.execute_command(cmd + [source_path, dest_path], 
                                    f"Copying {source_path} to {dest_path}")
            
            logger.add_record("[+] Copied Dotfiles & GTK", status=LoggerStatus.SUCCESS)
        except Exception as e:
            logger.add_record(f"[-] Failed to copy dotfiles: {str(e)}", status=LoggerStatus.ERROR)
            raise
