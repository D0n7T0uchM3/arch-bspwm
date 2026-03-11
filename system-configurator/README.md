# Arch BSPWM Configurator

An interactive installer for setting up the BSPWM window manager on Arch Linux with all necessary dependencies and configurations.

## Features

- **No Sudo Required**: Runs as a regular user, using `yay` for package management
- **Interactive Installation**: User-friendly prompts with clear descriptions
- **Comprehensive Logging**: Colored console output and detailed log files
- **Error Recovery**: Robust error handling with retry mechanisms
- **Modular Design**: Clean, maintainable code structure
- **Type Safety**: Full type hints for better code reliability

## Prerequisites

- **Operating System**: Arch Linux
- **Python**: 3.6 or higher
- **Git**: Required for downloading AUR packages
- **Network**: Internet connection for package downloads

## Installation Options

The installer provides four main options:

1. **Install Dotfiles**: Copy BSPWM configuration files to your home directory
2. **Update Database**: Refresh the Arch package database
3. **Install BSPWM Dependencies**: Install all required packages for BSPWM
4. **Install Graphics Drivers**: Install NVIDIA and Intel graphics drivers

## Usage

### Basic Installation

```bash
cd system-configurator
python3 main.py
```

### What Gets Installed

#### Core BSPWM Packages
- `bspwm` - Binary space partitioning window manager
- `sxhkd` - Simple X hotkey daemon
- `polybar` - Status bar
- `rofi` - Application launcher and dmenu replacement
- `picom` - Compositor for X11
- `alacritty` - Terminal emulator

#### System Utilities
- `yay` - AUR helper (automatically installed)
- `firefox` - Web browser
- `thunar` - File manager
- `dunst` - Notification daemon
- `nitrogen` - Wallpaper setter
- `flameshot` - Screenshot utility

#### Development Tools
- `git`, `vim`, `code` - Development essentials
- `python-pip`, `rust`, `nodejs` - Programming languages
- `gcc`, `clang`, `cmake` - Compilers and build tools

#### Media & Graphics
- `mpv` - Media player
- `vlc` - Alternative media player
- `gimp` - Image editor
- `obs-studio` - Screen recording/streaming

#### System Management
- `htop`, `btop` - System monitors
- `networkmanager` - Network management
- `blueman`, `bluez` - Bluetooth support
- `timeshift` - System backups

[Complete package list available in `installation/packages.py`]

## Project Structure

```
system-configurator/
├── main.py                     # Entry point
├── settings.py                 # User interface
├── logger.py                   # Logging system
├── assets/
│   └── startup.sh             # Banner script
├── configuration/
│   ├── system_initializer.py  # Main configuration logic
│   └── software.py            # AUR helper installation
└── installation/
    ├── installation_tools.py  # Command execution
    ├── packages.py            # Package definitions
    ├── drivers.py             # Graphics drivers
    ├── daemons.py             # System services
    └── patches.py             # System fixes
```

## Configuration Files

The installer copies various configuration files to your home directory:

- `~/.config/bspwm/` - BSPWM configuration
- `~/.config/sxhkd/` - Keyboard shortcuts
- `~/.config/polybar/` - Status bar configuration  
- `~/.config/rofi/` - Application launcher themes
- `~/.config/alacritty/` - Terminal configuration
- `~/.xinitrc` - X11 startup script
- `~/bin/` - Utility scripts

## Logging

All installation activities are logged to:
- **Console**: Colored output with real-time feedback
- **File**: `build_debug.log` with detailed information

Log levels:
- 🟢 **SUCCESS**: Operations completed successfully
- 🔴 **ERROR**: Critical errors requiring attention
- 🔴 **FAILURE**: Operations that failed but installation continues

## Error Handling

The installer includes comprehensive error handling:

- **Package Installation**: Retry failed packages individually
- **File Operations**: Skip missing files with warnings
- **Network Issues**: Graceful handling of connection problems
- **User Interruption**: Clean exit on Ctrl+C

## Manual Steps Required

Some operations require manual configuration:

1. **Graphics Drivers**: Enable multilib repository in `/etc/pacman.conf`
2. **System Services**: Enable services like NetworkManager and Bluetooth
3. **Boot Configuration**: Configure bootloader for graphics drivers

## Development

### Code Quality

- **Type Hints**: Full type annotation for better IDE support
- **Documentation**: Comprehensive docstrings
- **Error Handling**: Defensive programming practices
- **Logging**: Extensive logging for debugging

### Adding Packages

To add new packages, edit `installation/packages.py`:

```python
PACKAGES = [
    # ... existing packages ...
    "your-new-package",
    "another-package"
]
```

### Extending Functionality

The modular design makes it easy to add new features:

1. **New Installation Steps**: Add to `SystemConfiguration` class
2. **Additional Services**: Extend `Daemons` class
3. **Custom Patches**: Add to `PatchSystemBugs` class

## Troubleshooting

### Common Issues

**yay Installation Fails**
- Ensure git is installed: `pacman -S git`
- Check network connectivity
- Verify base-devel group is installed

**Permission Denied**
- Don't run with sudo - the installer is designed for regular users
- Ensure your user is in the wheel group for package installation

**Package Installation Errors**
- Update package database: `yay -Sy`
- Check available disk space
- Review the log file for specific errors

**Graphics Driver Issues**
- Enable multilib repository manually
- Reboot after driver installation
- Check hardware compatibility

### Getting Help

1. Check the log file `build_debug.log` for detailed error information
2. Ensure all prerequisites are met
3. Run individual commands manually to isolate issues
4. Check Arch Linux documentation for package-specific problems

## Contributing

Contributions are welcome! Please:

1. Follow the existing code style
2. Add proper type hints
3. Include comprehensive error handling
4. Update documentation as needed
5. Test thoroughly before submitting

## License

This project is released under the MIT License. See the LICENSE file for details.

## Acknowledgments

- Arch Linux community for excellent documentation
- BSPWM developers for the window manager
- Contributors to all included open-source packages
