import socket
import threading
import datetime
import random
import requests
import json


# Helper function to generate random date and time
def random_datetime():
    return datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")


# Helper function to simulate satellite orientation and position
def random_orientation():
    return [random.uniform(-180, 180) for _ in range(3)]  # Orientation in degrees


def random_position():
    return [random.uniform(-10000, 10000) for _ in range(3)]  # Position in kilometers


# Helper functions to simulate COM data
def random_frequency():
    return random.randint(400000000, 450000000)  # Frequency in Hz


def random_data_volume():
    return random.randint(1000, 5000)  # Data volume in bytes


# Helper function to get a Mars rover image
def get_mars_rover_image():
    rover_url = "https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos?sol=1000&api_key=WgIuHBbHhTRhGykrKjM8LZ8Y9Hte5UWNiN2apNIk"
    response = requests.get(rover_url)
    if response.status_code == 200:
        data = response.json()
        if data["photos"]:
            latest_photo = data["photos"][0]
            return latest_photo["img_src"]
    return "No image available"


def simulate_error():
    # Randomly simulate an error occurrence
    if random.random() < 0.1:  # 10% chance of error
        return True
    return False


# EPS Command: Get Configuration 1
def eps_cmd_get_config1_cb():
    # This could represent the voltage of boost converters
    vboost = [random.randint(3000, 4000) for _ in range(3)]
    return f"Config 1: [VBoost: {vboost}]"


# EPS Command: Set Configuration 1
def eps_cmd_set_config1_cb():
    # Simulate setting vboost values
    vboost = [random.randint(3000, 4000) for _ in range(3)]
    return f"Config 1 Set: [VBoost: {vboost}]"


# EPS Command: Get Configuration 2
def eps_cmd_get_config2_cb():
    # This could represent battery configurations
    vbatt_max = random.randint(8000, 9000)
    vbatt_safe = random.randint(6000, 7000)
    return f"Config 2: [VBatt Max: {vbatt_max}, VBatt Safe: {vbatt_safe}]"


# EPS Command: Set Configuration 2
def eps_cmd_set_config2_cb():
    vbatt_max = random.randint(8000, 9000)
    vbatt_safe = random.randint(6000, 7000)
    return f"Config 2 Set: [VBatt Max: {vbatt_max}, VBatt Safe: {vbatt_safe}]"


# EPS Command: Get Configuration 3
def eps_cmd_get_config3_cb():
    # This could represent the status of outputs
    output_status = [random.choice(["ON", "OFF"]) for _ in range(3)]
    return f"Config 3: [Output Status: {output_status}]"


# EPS Command: Set Configuration 3
def eps_cmd_set_config3_cb():
    output_status = [random.choice(["ON", "OFF"]) for _ in range(3)]
    return f"Config 3 Set: [Output Status: {output_status}]"


# EPS Command: Set Timeout
def eps_cmd_set_timeout_cb():
    # Simulate setting a watchdog timer timeout
    timeout = random.randint(100, 600)  # Random timeout in seconds
    return f"Timeout Set: [WDT: {timeout}s]"


# EPS Command: Set Heater Control
def eps_cmd_set_heater_ctrl_cb():
    mode = random.choice(["AUTO", "MANUAL"])
    temp_high = random.randint(15, 25)  # High temperature threshold
    temp_low = random.randint(0, 10)  # Low temperature threshold
    return f"Heater Control Set: [Mode: {mode}, Temp High: {temp_high}C, Temp Low: {temp_low}C]"


# EPS Command: Reset Watchdog Timer Ground
def eps_cmd_reset_wdt_gnd_cb():
    return "WDT Ground Reset: Success"


# EPS Command: Set PPT Mode
def eps_cmd_set_pptmode_cb():
    mode = random.choice(["MPPT", "FIXED"])
    return f"PPT Mode Set: [Mode: {mode}]"


# EPS Command: Set VBoost
def eps_cmd_set_vboost_cb():
    vboost = [random.randint(3000, 4000) for _ in range(3)]
    return f"VBoost Set: [{', '.join(map(str, vboost))}]"


# EPS Telemetry Data Request
def eps_telem_hk_get_cb():
    error_occurred = simulate_error()
    return {
        "timestamp": random_datetime(),
        "vboost": [random.randint(3000, 4000) for _ in range(3)],
        "vbatt": random.randint(6000, 9000),
        "curout": [random.randint(100, 500) for _ in range(6)],
        "curin": [random.randint(100, 500) for _ in range(3)],
        "cursun": random.randint(100, 500),
        "cursys": random.randint(100, 500),
        "temp": [random.randint(-40, 80) for _ in range(6)],
        "output": [random.randint(0, 1) for _ in range(8)],
        "output_on_delta": [random.randint(0, 1000) for _ in range(8)],
        "output_off_delta": [random.randint(0, 1000) for _ in range(8)],
        "wdt_i2c_time_left": random.randint(0, 10000),
        "wdt_gnd_time_left": random.randint(0, 10000),
        "counter_boot": random.randint(0, 100),
        "counter_wdt_i2c": random.randint(0, 100),
        "counter_wdt_gnd": random.randint(0, 100),
        "counter_wdt_csp": [random.randint(0, 100) for _ in range(2)],
        "wdt_csp_pings_left": [random.randint(0, 10) for _ in range(2)],
        "bootcause": random.randint(0, 2),
        "latchup": [random.randint(0, 10) for _ in range(6)],
        "battmode": random.randint(0, 2),
        "pptmode": random.randint(0, 2),
        "error": error_occurred,
        "error_code": "E01" if error_occurred else "None",
    }


# EPS Telemetry Housekeeping Persistent Data Request
def eps_telem_hk_persist_get_cb():
    error_occurred = simulate_error()
    return {
        "timestamp": random_datetime(),
        "boot_count": random.randint(1, 100),
        "resets": random.randint(1, 10),
        "uptime": random.randint(0, 10000),  # System uptime in seconds
        "last_reset_reason": random.choice(["Power Cycle", "Watchdog", "Manual"]),
        "error": error_occurred,
        "error_code": "E02" if error_occurred else "None",
    }


# COM Command: Get System Configuration
def com_cmd_get_config_sys_cb():
    csp_address = random.randint(1, 10)
    i2c_enabled = random.choice([True, False])
    can_enabled = random.choice([True, False])
    return f"System Config: [CSP Address: {csp_address}, I2C Enabled: {i2c_enabled}, CAN Enabled: {can_enabled}]"


# COM Command: Set System Configuration
def com_cmd_set_config_sys_cb():
    csp_address = random.randint(1, 10)
    i2c_enabled = random.choice([True, False])
    can_enabled = random.choice([True, False])
    return f"System Config Set: [CSP Address: {csp_address}, I2C Enabled: {i2c_enabled}, CAN Enabled: {can_enabled}]"


# COM Command: Get Transmit Configuration
def com_cmd_get_config_tx_cb():
    tx_power = random.randint(1, 5)  # Arbitrary TX power level
    beacon_interval = random.randint(5, 15)  # Beacon interval in seconds
    return (
        f"Transmit Config: [TX Power: {tx_power}, Beacon Interval: {beacon_interval}s]"
    )


# COM Command: Set Transmit Configuration
def com_cmd_set_config_tx_cb():
    tx_power = random.randint(1, 5)
    beacon_interval = random.randint(5, 15)
    return f"Transmit Config Set: [TX Power: {tx_power}, Beacon Interval: {beacon_interval}s]"


# COM Command: Get Receive Configuration
def com_cmd_get_config_rx_cb():
    frequency = random_frequency()
    baudrate = random.choice([1200, 2400, 4800, 9600])
    return f"Receive Config: [Frequency: {frequency} Hz, Baudrate: {baudrate}]"


# COM Command: Set Receive Configuration
def com_cmd_set_config_rx_cb():
    frequency = random_frequency()
    baudrate = random.choice([1200, 2400, 4800, 9600])
    return f"Receive Config Set: [Frequency: {frequency} Hz, Baudrate: {baudrate}]"


# COM Telemetry: Housekeeping Data
def com_telem_hk_get_cb():
    error_occurred = simulate_error()
    return {
        "timestamp": random_datetime(),
        "board_temp": random.randint(-10, 50),
        "pa_temp": random.randint(-10, 60),
        "last_rssi": random.randint(-120, 0),
        "signal_quality": random.randint(0, 100),  # Simulated signal quality
        "uptime": random.randint(0, 10000),
        "error": error_occurred,
        "error_code": "E03" if error_occurred else "None",
    }


# COM Telemetry: Command Data
def com_telem_hk_cmd_get_cb():
    error_occurred = simulate_error()
    return {
        "timestamp": random_datetime(),
        "tx_count": random.randint(50, 200),
        "rx_count": random.randint(50, 200),
        "tx_bytes": random_data_volume(),
        "rx_bytes": random_data_volume(),
        "command_ack_rate": random.uniform(
            0, 1
        ),  # Simulated command acknowledgment rate
        "error": error_occurred,
        "error_code": "E04" if error_occurred else "None",
    }


# CAM Command: Snap an image
def cam_cmd_snap_cb():
    image_url = get_mars_rover_image()
    timestamp = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
    return f"Image Snapped: [Image URL: {image_url}, Timestamp: {timestamp}]"


# CAM Command: Store image
def cam_cmd_store_cb():
    image_id = random.randint(100, 200)
    storage_status = "Secured"
    size = random.uniform(1.0, 5.0)  # Image size in MB
    return f"Image Stored: [Image ID: {image_id}, Storage Status: {storage_status}, Size: {size:.1f}MB]"


# CAM Command: List stored images
def cam_cmd_img_list_cb():
    stored_images = random.sample(range(100, 200), 5)  # Randomly pick 5 image IDs
    return f"Stored Images: [Total: 5, Image IDs: {stored_images}]"


# CAM Command: Flush image storage
def cam_cmd_img_flush_cb():
    freed_space = random.uniform(10.0, 30.0)  # Freed space in MB
    return f"Image Storage Flushed: [Status: Success, Freed Space: {freed_space:.1f}MB]"


# CAM Command: Adjust focus
def cam_cmd_focus_cb():
    new_focus_level = random.uniform(5.0, 10.0)
    return f"Focus Adjusted: [New Focus Level: {new_focus_level:.1f}, Status: Sharp]"


# CAM Command: Recover file system
def cam_cmd_recover_fs_cb():
    recovered_files = random.randint(1, 5)
    return (
        f"File System Recovery: [Status: Completed, Recovered Files: {recovered_files}]"
    )


# CAM Telemetry: Housekeeping Data
def cam_telem_hk_get_cb():
    error_occurred = simulate_error()
    stored_images = random.sample(range(100, 200), 5)
    return {
        "timestamp": random_datetime(),
        "stored_images": stored_images,
        "total_storage_used": random.uniform(10.0, 30.0),  # Total storage used in MB
        "camera_status": random.choice(["Operational", "Standby", "Error"]),
        "error": error_occurred,
        "error_code": "E05" if error_occurred else "None",
    }


# CAM Telemetry: Command Data
def cam_telem_hk_cmd_get_cb():
    error_occurred = simulate_error()
    stored_images = random.sample(range(100, 200), 5)
    return {
        "timestamp": random_datetime(),
        "recently_captured": stored_images,
        "capture_success_rate": random.uniform(
            0, 1
        ),  # Simulated image capture success rate
        "error": error_occurred,
        "error_code": "E06" if error_occurred else "None",
    }


# ADCS Command: Set Timeout
def adcs_cmd_set_timeout_cb():
    new_timeout = random.randint(60, 180)  # Timeout in seconds
    return f"Timeout Set: [New Timeout: {new_timeout}s, Status: Updated]"


# ADCS Command: Get State
def adcs_cmd_get_state_cb():
    mode = random.choice(["Stable", "Maneuver", "Drift"])
    orientation = random_orientation()
    return f"ADCS State: [Mode: {mode}, Orientation: {orientation}]"


# ADCS Telemetry: Housekeeping Data
def adcs_telem_hk_get_cb():
    error_occurred = simulate_error()
    return {
        "timestamp": random_datetime(),
        "temperature": random.randint(-40, 80),
        "power_usage": random.randint(10, 100),
        "orientation": random_orientation(),
        "angular_velocity": [
            random.uniform(-1, 1) for _ in range(3)
        ],  # Angular velocity in degrees/s
        "error": error_occurred,
        "error_code": "E07" if error_occurred else "None",
    }


# ADCS Telemetry: Command Data
def adcs_telem_hk_cmd_get_cb():
    error_occurred = simulate_error()
    return {
        "timestamp": random_datetime(),
        "position": random_position(),
        "velocity": [random.uniform(-5, 5) for _ in range(3)],
        "maneuver_count": random.randint(0, 10),  # Number of maneuvers performed
        "error": error_occurred,
        "error_code": "E08" if error_occurred else "None",
    }


# OBC Command: Get MASAT State
def obc_cmd_get_masat_state_cb():
    mode = random.choice(["Science", "Standby", "Safe"])
    temp = random.randint(-20, 40)  # Temperature in Celsius
    power_status = random.choice(["Nominal", "Low", "Critical"])
    current_time = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
    return f"MASAT State: [Mode: {mode}, Temp: {temp}C, Power: {power_status}, Time: {current_time}]"


# OBC Command: Load Image
def obc_cmd_load_imag_cb():
    image_id = random.randint(1, 100)
    size = random.uniform(1.0, 5.0)  # Image size in MB
    return f"Image Load: [Status: Success, Image ID: {image_id}, Size: {size:.1f}MB]"


# OBC Command: Track Target
def obc_cmd_track_target_cb():
    target_id = random.randint(10000, 99999)
    status = random.choice(["Locked", "Searching", "Lost"])
    coordinates = [random.uniform(-180, 180), random.uniform(-90, 90)]  # Lat, Long
    return f"Tracking Target: [Target ID: {target_id}, Status: {status}, Coordinates: {coordinates}]"


# OBC Command: Time Sync
def obc_cmd_timesync_cb():
    synced_time = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
    return f"Time Sync: [Status: Success, Synced Time: {synced_time}]"


# OBC Command: Jump to RAM
def obc_cmd_jump_ram_cb():
    address = hex(random.randint(0x1000, 0xFFFF))
    return f"Jump to RAM: [Address: {address}, Status: Executed]"


# OBC Command: Set Boot Configuration
def obc_cmd_boot_conf_cb():
    new_boot_mode = random.choice(["Science Mode", "Safe Mode", "Bootloader"])
    return f"Boot Config Set: [New Boot Mode: {new_boot_mode}, Status: Updated]"


# OBC Command: Delete Configuration
def obc_cmd_conf_del_cb():
    config_id = random.randint(1, 10)
    return f"Config Deleted: [Config ID: {config_id}, Status: Removed]"


# OBC Command: RAM to ROM
def obc_cmd_ram_to_rom_cb():
    bytes_transferred = random.randint(1024, 4096)  # Bytes transferred
    return f"RAM to ROM: [Status: Completed, Bytes Transferred: {bytes_transferred}]"


# OBC Command: Get Boot Count
def obc_cmd_boot_count_get_cb():
    current_count = random.randint(1, 100)
    return f"Boot Count: [Current Count: {current_count}]"


# OBC Command: Reset Boot Count
def obc_cmd_boot_count_reset_cb():
    return "Boot Count Reset: [Status: Reset, New Count: 0]"


# OBC Command: Get Persistent Telemetry
def obc_telem_hk_persist_get_cb():
    error_occurred = simulate_error()
    return {
        "timestamp": random_datetime(),
        "boot_count": random.randint(1, 100),
        "resets": random.randint(1, 10),
        "total_uptime": random.randint(0, 10000),  # Total uptime in seconds
        "last_boot_reason": random.choice(["Power Cycle", "Watchdog", "Manual"]),
        "config_change_count": random.randint(0, 50),  # Number of configuration changes
        "error": error_occurred,
        "error_code": "E09" if error_occurred else "None",
    }


# OBC Command: Get Telemetry
def obc_telem_hk_get_cb():
    error_occurred = simulate_error()
    return {
        "timestamp": random_datetime(),
        "cpu_load": random.uniform(0, 1),  # CPU load as a fraction of total capacity
        "memory_usage": random.uniform(
            0, 1
        ),  # Memory usage as a fraction of total capacity
        "temperature": random.randint(-20, 70),  # Temperature in Celsius
        "power_status": random.choice(["Nominal", "Low", "Critical"]),
        "active_processes": random.randint(0, 100),  # Number of active processes
        "error": error_occurred,
        "error_code": "E10" if error_occurred else "None",
    }


# OBC Command: Get Telemetry
def obc_telem_hk_cmd_get_cb():
    error_occurred = simulate_error()
    return {
        "timestamp": random_datetime(),
        "last_command": random.choice(
            ["CMD_A", "CMD_B", "CMD_C"]
        ),  # Simulated last command
        "command_success_rate": random.uniform(0, 1),  # Simulated command success rate
        "recent_errors": random.randint(0, 5),  # Number of recent errors
        "error": error_occurred,
        "error_code": "E11" if error_occurred else "None",
    }


# Mock implementations for command handling
def handle_obc_command(command):
    if command == "obc_cmd_get_masat_state_cb":
        return obc_cmd_get_masat_state_cb()
    elif command == "obc_cmd_load_imag_cb":
        return obc_cmd_load_imag_cb()
    elif command == "obc_cmd_track_target_cb":
        return obc_cmd_track_target_cb()
    elif command == "obc_cmd_timesync_cb":
        return obc_cmd_timesync_cb()
    elif command == "obc_cmd_jump_ram_cb":
        return obc_cmd_jump_ram_cb()
    elif command == "obc_cmd_boot_conf_cb":
        return obc_cmd_boot_conf_cb()
    elif command == "obc_cmd_conf_del_cb":
        return obc_cmd_conf_del_cb()
    elif command == "obc_cmd_ram_to_rom_cb":
        return obc_cmd_ram_to_rom_cb()
    elif command == "obc_cmd_boot_count_get_cb":
        return obc_cmd_boot_count_get_cb()
    elif command == "obc_cmd_boot_count_reset_cb":
        return obc_cmd_boot_count_reset_cb()
    elif command == "obc_telem_hk_persist_get_cb":
        return obc_telem_hk_persist_get_cb()
    elif command == "obc_telem_hk_get_cb":
        return obc_telem_hk_get_cb()
    elif command == "obc_telem_hk_cmd_get_cb":
        return obc_telem_hk_cmd_get_cb()
    else:
        return "Unknown OBC Command"


def handle_eps_command(command):
    if command == "eps_cmd_get_config1_cb":
        return eps_cmd_get_config1_cb()
    elif command == "eps_cmd_set_config1_cb":
        return eps_cmd_set_config1_cb()
    elif command == "eps_cmd_get_config2_cb":
        return eps_cmd_get_config2_cb()
    elif command == "eps_cmd_set_config2_cb":
        return eps_cmd_set_config2_cb()
    elif command == "eps_cmd_get_config3_cb":
        return eps_cmd_get_config3_cb()
    elif command == "eps_cmd_set_config3_cb":
        return eps_cmd_set_config3_cb()
    elif command == "eps_cmd_set_timeout_cb":
        return eps_cmd_set_timeout_cb()
    elif command == "eps_cmd_set_heater_ctrl_cb":
        return eps_cmd_set_heater_ctrl_cb()
    elif command == "eps_cmd_reset_wdt_gnd_cb":
        return eps_cmd_reset_wdt_gnd_cb()
    elif command == "eps_cmd_set_pptmode_cb":
        return eps_cmd_set_pptmode_cb()
    elif command == "eps_cmd_set_vboost_cb":
        return eps_cmd_set_vboost_cb()
    elif command == "eps_telem_hk_get_cb":
        return eps_telem_hk_get_cb()
    elif command == "eps_telem_hk_persist_get_cb":
        return eps_telem_hk_persist_get_cb()
    else:
        return "Unknown EPS Command"


def handle_com_command(command):
    if command == "com_cmd_get_config_sys_cb":
        return com_cmd_get_config_sys_cb()
    elif command == "com_cmd_set_config_sys_cb":
        return com_cmd_set_config_sys_cb()
    elif command == "com_cmd_get_config_tx_cb":
        return com_cmd_get_config_tx_cb()
    elif command == "com_cmd_set_config_tx_cb":
        return com_cmd_set_config_tx_cb()
    elif command == "com_cmd_get_config_rx_cb":
        return com_cmd_get_config_rx_cb()
    elif command == "com_cmd_set_config_rx_cb":
        return com_cmd_set_config_rx_cb()
    elif command == "com_telem_hk_get_cb":
        return com_telem_hk_get_cb()
    elif command == "com_telem_hk_cmd_get_cb":
        return com_telem_hk_cmd_get_cb()
    else:
        return "Unknown COM Command"


def handle_cam_command(command):
    if command == "cam_cmd_snap_cb":
        return cam_cmd_snap_cb()
    elif command == "cam_cmd_store_cb":
        return cam_cmd_store_cb()
    elif command == "cam_cmd_img_list_cb":
        return cam_cmd_img_list_cb()
    elif command == "cam_cmd_img_flush_cb":
        return cam_cmd_img_flush_cb()
    elif command == "cam_cmd_focus_cb":
        return cam_cmd_focus_cb()
    elif command == "cam_cmd_recover_fs_cb":
        return cam_cmd_recover_fs_cb()
    elif command == "cam_telem_hk_get_cb":
        return cam_telem_hk_get_cb()
    elif command == "cam_telem_hk_cmd_get_cb":
        return cam_telem_hk_cmd_get_cb()
    else:
        return "Unknown CAM Command"


def handle_adcs_command(command):
    if command == "adcs_cmd_set_timeout_cb":
        return adcs_cmd_set_timeout_cb()
    elif command == "adcs_cmd_get_state_cb":
        return adcs_cmd_get_state_cb()
    elif command == "adcs_telem_hk_get_cb":
        return adcs_telem_hk_get_cb()
    elif command == "adcs_telem_hk_cmd_get_cb":
        return adcs_telem_hk_cmd_get_cb()
    else:
        return "Unknown ADCS Command"


def handle_client_connection(client_socket):
    try:
        data = client_socket.recv(1024)
        if not data:
            return

        received_data = data.decode("utf-8")
        components = received_data.split(",")
        if len(components) != 3:
            print("Invalid data format")
            return

        station_num, module_num, command = components
        print(
            f"Received: Number 10: {station_num}, Module Number: {module_num}, Command: {command}"
        )

        # Handling commands based on the module_num
        if module_num == "1":
            response = handle_obc_command(command)
        elif module_num == "4":
            response = handle_eps_command(command)
        elif module_num == "3":
            response = handle_com_command(command)
        elif module_num == "2":
            response = handle_cam_command(command)
        elif module_num == "5":
            response = handle_adcs_command(command)
        else:
            response = "Unknown module"

        client_socket.send(json.dumps(response).encode("utf-8"))
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        client_socket.close()


def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind(("localhost", 2738))
        server_socket.listen(1)
        print("Server is listening for connections...")

        while True:
            try:
                client_socket, client_address = server_socket.accept()
                print(f"Accepted connection from {client_address}")
                threading.Thread(
                    target=handle_client_connection, args=(client_socket,)
                ).start()
            except Exception as e:
                print(f"An error occurred: {e}")
                break


if __name__ == "__main__":
    start_server()
