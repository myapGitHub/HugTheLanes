import sys


vehicle_conditions = {
    "tire_pressure": 32,  # PSI
    "gas_level": 50,  # Percentage
    "light_levels": 50, # Percentage
    "tire_grip": 80,  # Percentage from original
    "damage": "None", # Damage to car
    "battery_level": 75,  # Percentage
    "engine_condition": "Good", # Condition of engine
    "oil_condition": "Change Needed", # Oil condition
    "mirror_condition": "Clear", # Mirror clarity
    "camera_condition": "Operational", # Camera condition
    "ventilation_system": "Functional", # Vent system functionality
    "speaker_condition": "Clear", # Clear or static
    "brake_condition": "Good", # Brake functionality
    "suspension_condition": "Okay" # Condition of suspension
}

software_update = False

hardware_update = False


def login(): # Check credentials for login
    max_attempts=3
    username = "username"
    password = "password"
    attempt_count = 0
    while attempt_count < max_attempts:
        userInput = input("Enter username: ")
        pwdInput = input("Enter password: ")
        if userInput == username and pwdInput == password:
            print("Login successful")
            return True
        else:
            print("Incorrect credentials")
            attempt_count += 1
    print("Too many incorrect attempts. Exiting...")
    return False

def menu_selection(): # Ask for selected menu
    menu_options = ["Software Updates", "Hardware Updates", "Monitor Menu"]
    while True:
        state = input("Please select from the following menus: Software Updates, Hardware Updates, Monitor Menu: ")
        if state in menu_options:
            return state
        print("Please select a valid option")

def monitor_menu(): # Return all values of vehicle conditions
    return vehicle_conditions

def software_updates(): # Return bool value of software_update
    return software_update

def hardware_updates(): # Return bool value of hardware_update
    return hardware_update

def main():
    
    if login():
        selected_menu = menu_selection()
        print(f"You have selected {selected_menu}")

    if selected_menu == "Software Updates":
        if software_updates():
            #handle software update
            print("Proceeding with software update")
        else: 
            print("No software update available")
        # handle software update options, return true if there are updates, false if not
    elif selected_menu == "Hardware Updates":
        if hardware_updates():
            print("Please proceed to update hardware")
        else: 
            print("No hardware update needed")
        # handle Hardware update options, return true if there are updates, false if not
    else:
        monitor_menu()
        # handle monitor menu
        

if __name__ == "__main__":
    main()
