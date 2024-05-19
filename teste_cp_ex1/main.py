import json
import os

CONFIG_FILE = "config.json"

def read_configurations():

    try:
        with open(CONFIG_FILE, "r") as arquive:
            data = json.load(arquive)
            print("Configurations:")
            print(json.dumps(data, indent=4))
    except FileNotFoundError:
        print("Config.json file not found.")
    except json.JSONDecodeError:
        print("Error to read config.json! Please verify if your JSON file is valid.")


def save_configurations():

    server_name = input("Enter the server name: ")
    server_ip = input("Enter the server IP: ")
    server_password = input("Enter the server password: ")

    data = {
        "server_name": server_name,
        "server_ip": server_ip,
        "server_password": server_password,
    }

    try:
        with open(CONFIG_FILE, "w") as arquive:
            json.dump(data, arquive, indent=4)
        print("Successfully saved information!")
        print("Configurations:")
        print(json.dumps(data, indent=4))
    except Exception as e:
        print(f"Error when saving information to file: {e}")


def main():

    while True:
        print("\nAvailable options:")
        print("1 - Read configuration")
        print("2 - Write configuration")
        print("3 - Exit")

        option = input("Select the desired option: ")

        if option == "1":
            read_configurations()
        elif option == "2":
            save_configurations()
        elif option == "3":
            break
        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    main()