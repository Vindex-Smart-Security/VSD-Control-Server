import os
import shutil
import json
import configparser
import platform
from colorama import init, Fore
from datetime import datetime

init(autoreset=True)

def log_message(message, level='INFO'):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if level == 'INFO':
        print(Fore.CYAN + f"[{timestamp}] INFO: {message}")
    elif level == 'SUCCESS':
        print(Fore.GREEN + f"[{timestamp}] SUCCESS: {message}")
    elif level == 'WARNING':
        print(Fore.YELLOW + f"[{timestamp}] WARNING: {message}")
    elif level == 'ERROR':
        print(Fore.RED + f"[{timestamp}] ERROR: {message}")

def setup_vsd_folder():
    appdata_local = os.path.join(os.environ['APPDATA'], '..', 'Local')
    vsd_folder = os.path.join(appdata_local, 'VSD')
    backup_config_path = os.path.join(appdata_local, "config.bak")

    # Check if the VSD folder exists
    if not os.path.exists(vsd_folder):
        log_message("VSD folder not found. Creating folder...", level='ERROR')
        os.makedirs(vsd_folder)
        log_message(f"VSD folder created successfully at: {vsd_folder}", level='SUCCESS')
        
        # Create a backup only if the VSD folder was created
        create_backup(backup_config_path, vsd_folder)
    else:
        log_message("VSD folder found. Checking for config files...", level='INFO')

    # Check for the config.ini file
    config_file_path = os.path.join(vsd_folder, 'config.ini')
    
    if not os.path.isfile(config_file_path):
        log_message("config.ini not found. Attempting to restore from backup...", level='ERROR')
        if restore_from_backup(backup_config_path, vsd_folder):
            log_message("config.ini restored from backup.", level='SUCCESS')
        else:
            log_message("Failed to restore config.ini from backup. Generating a new template...", level='ERROR')
            generate_config_template(config_file_path)
            log_message(f"Default config.ini template created at: {config_file_path}", level='SUCCESS')
    else:
        log_message("config.ini found. Checking for other files...", level='SUCCESS')

def restore_from_backup(backup_folder, target_folder):
    try:
        # Copying config.ini from backup to the VSD folder
        backup_file_path = os.path.join(backup_folder, 'config.ini')
        if os.path.isfile(backup_file_path):
            shutil.copy(backup_file_path, target_folder)
            log_message(f"Restored config.ini from backup at: {backup_file_path}", level='SUCCESS')
            return True
        else:
            log_message("Backup config.ini not found.", level='ERROR')
            return False
    except Exception as e:
        log_message(f"Error restoring from backup: {e}", level='ERROR')
        return False
    
def create_backup(backup_config_path, vsd_folder):
    # Ensure the VSD folder exists
    if not os.path.exists(vsd_folder):
        os.makedirs(vsd_folder)
        log_message(f"Created VSD folder at: {vsd_folder}", level='SUCCESS')

    if os.path.exists(backup_config_path):
        log_message(f"Backup config found at: {backup_config_path}", level='INFO')
        shutil.copy(backup_config_path, os.path.join(vsd_folder, 'config.bak'))  # Create a backup file
        log_message(f"Backup file created successfully at {os.path.join(vsd_folder, 'config.bak')}", level='SUCCESS')
    else:
        log_message("Backup config file does not exist. No backup created.", level='WARNING')

def generate_config_template(config_file_path):
    config = configparser.ConfigParser()
    config['DEFAULT'] = {
        'Setting1': 'Value1',
        'Setting2': 'Value2',
        'Setting3': 'Value3'
    }
    config['Database'] = {
        'DBHost': 'localhost',
        'DBPort': '3306',
        'DBUser': 'user',
        'DBPassword': 'password'
    }
    config['Network'] = {
        'Timeout': '30',
        'Retries': '3'
    }

    with open(config_file_path, 'w') as configfile:
        config.write(configfile)

