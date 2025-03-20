from installation_tools import Executer

from logger import Logger

logger = Logger()

class PatchSystemBugs:
    @staticmethod
    def enable_all_patches():
        """
        Apply all system patches and fixes.
        """
        PatchSystemBugs.__fix_xterm_error_in_thunar()
        PatchSystemBugs.__make_zsh_the_default()
        PatchSystemBugs.__assign_permissions_to_configs()

    @staticmethod
    def __fix_xterm_error_in_thunar():
        """
        Fixes the xterm error in Thunar by symlinking Alacritty to xterm.
        """
        command = ["sudo", "ln", "-sf", "/usr/bin/alacritty", "/usr/bin/xterm"]
        Executer.execute_command(command, "Fixing xterm error in Thunar")

    @staticmethod
    def __make_zsh_the_default():
        """
        Sets q as the default shell for the user.
        """
        command = ["chsh", "-s", "/usr/bin/zsh"]
        Executer.execute_command(command, "Setting zsh as the default shell")

    @staticmethod
    def __assign_permissions_to_configs():
        """
        Recursively assigns permissions (700) to all files in ~/.config.
        """
        command = ["sudo", "chmod", "-R", "700", "~/.config/*"]
        Executer.execute_command(command, "Assigning permissions to config files")
