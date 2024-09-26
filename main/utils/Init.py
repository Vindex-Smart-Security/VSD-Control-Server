import requests
import socket
from concurrent.futures import ThreadPoolExecutor
from pyfiglet import figlet_format
from colorama import init, Fore
from utils.Websocket import start_server
from utils.Setup import log_message, setup_vsd_folder
import time
import os
import platform

init(autoreset=True)

async def handle_exit(shutdown_event):
    while True:
        user_input = input("Type 'exit()' to quit: ")
        if user_input.strip() == 'exit()':
            log_message("Exiting the application...", level='INFO')
            shutdown_event.set()  # Signal to shutdown
            break

# DESIGN

async def StartUp(shutdown_event):
    display_banner()
    
    time.sleep(2)

    network_status = await check_network()

    if not network_status['reachable']:
        log_message("Network connection failed. Exiting...", level='ERROR')
        exit(1)

    log_message("Network successfully connected.", level='SUCCESS')

    if not Check_File_System():
        log_message("File system check failed. Running setup...", level='ERROR')
        setup_vsd_folder() 
    else:
        log_message("File system check passed.", level='SUCCESS')

    while True:
        if shutdown_event.is_set():
            log_message("Shutdown event detected, stopping StartUp...", level='INFO')
            return
        
        time.sleep(1)

    await start_server()


def display_banner():
    banner = figlet_format("VSD Control")
    print(Fore.CYAN + banner)
    print(Fore.CYAN + "=" * 56, " \n") 

# NETWORK
def get_public_ip():
    try:
        response = requests.get('https://api.ipify.org', timeout=5)
        return response.text
    except requests.RequestException:
        return 'Unable to retrieve public IP'

async def check_network(url='https://vindexsecurity.com'):
    network_info = {}
    
    # Get the public IP address
    network_info['public_ip'] = get_public_ip()
    
    # Get the IP address of the target URL
    try:
        ip_address = socket.gethostbyname(url.split("//")[-1])
        network_info['ip_address'] = ip_address
    except socket.gaierror:
        network_info['ip_address'] = 'Unable to resolve IP address'

    # Check network connectivity
    try:
        response = requests.get(url, timeout=5)
        network_info['reachable'] = True
        network_info['status_code'] = response.status_code
        network_info['content_length'] = len(response.content)
        network_info['headers'] = response.headers
        network_info['response_time'] = response.elapsed.total_seconds()
    except requests.ConnectionError:
        network_info['reachable'] = False
        network_info['error'] = 'ConnectionError'
    except requests.Timeout:
        network_info['reachable'] = False
        network_info['error'] = 'TimeoutError'
    except Exception as e:
        network_info['reachable'] = False
        network_info['error'] = str(e)
        
    return network_info

def Check_File_System():
    appdata_local = os.path.join(os.environ['APPDATA'], '..', 'Local')
    vsd_folder = os.path.join(appdata_local, 'VSD')
    
    if os.path.exists(vsd_folder) and os.path.isdir(vsd_folder):
        log_message(f"Found VSD folder at: {vsd_folder}", level="INFO")
        
        files = os.listdir(vsd_folder)
        if files:
            log_message("Files found in VSD folder", level='INFO')

            return True
        else:
            log_message("No files found in the VSD folder.", level='WARNING')
            return False
    else:
        log_message("VSD folder not found in AppData\\Local.", level='WARNING')
        return False

def read_config_file():
    appdata_local = os.path.join(os.environ['APPDATA'], '..', 'Local')
    vsd_folder = os.path.join(appdata_local, 'VSD')
    config_file_path = os.path.join(vsd_folder, 'config.ini')
    
    if os.path.exists(config_file_path):
        with open(config_file_path, 'r') as file:
            return file.read()  
    else:
        log_message("config.ini not found in the VSD folder.", level='WARNING')
        return None

