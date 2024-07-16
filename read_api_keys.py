# Open api_keys.txt and read the API keys contained therein
# Store each one to the os env
import os


# Read the API keys from the file
def read_api_keys():
    keys_found = []
    with open("api_keys.txt", "r") as file:
        lines = file.readlines()
        for line in lines:
            key, value = line.split("=")
            os.environ[key.strip()] = value.strip()
            print(f"Got API key: {key.strip()}")
            keys_found.append(key.strip())
    expected_keys = ["OPENAI_API_KEY", "STABILITY_KEY"]
    for key in expected_keys:
        if key not in keys_found:
            print("!" * 50)
            print(f"WARNING! Expected key `{key}` not found in api_keys.txt")
            print("!" * 50)


if __name__ == "__main__":
    read_api_keys()
    print("Done reading API keys.")
