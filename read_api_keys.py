# Open api_keys.txt and read the API keys contained therein
# Store each one to the os env
import os


# Read the API keys from the file
def read_api_keys():
    with open("api_keys.txt", "r") as file:
        lines = file.readlines()
        for line in lines:
            key, value = line.split("=")
            os.environ[key.strip()] = value.strip()
            print(f"Got API key: {key.strip()}")


if __name__ == "__main__":
    read_api_keys()
    print("Done reading API keys.")
