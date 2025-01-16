import os

def create_env_file():
    env_path = ".env"
    if not os.path.exists(env_path):
        with open(env_path, 'w') as env_file:
            env_file.write("""CLIENT_ID = 
CLIENT_SECRET = """)
        print(f"{env_path} file has been created. Please update it with your API key.")
    else:
        print(f"{env_path} already exists.")

if __name__ == "__main__":
    create_env_file()