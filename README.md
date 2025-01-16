# Spotify Toolbox

**Spotify Toolbox** gives users more control over their Spotify library, allowing users to create tags to further organize their music collection, as well as creating playlist templates with more customization than Spotify's own playlists. To learn more about this project's goals and capabilities, refer to the `overview.md` file located in the `docs` folder.

**Disclaimer:** Spotify Toolbox requires the user to have a **Spotify Premium** account in order to access all features.


## Table of Contents
- [Installation](#installation)
- [Spotify API Access](#spotify-api-access)
- [Usage](#usage)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/ryanphilipcohen/Spotify-Toolbox.git
   ```

2. Navigate into the project directory:
   ```bash
   cd Spotify-Toolbox
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Spotify API access
This program interacts with the spotify API, which requires API keys. To obtain the keys, follow these steps:

1. Visit **https://developer.spotify.com/dashboard** and log into your Spotify account.

2. Click on **Create an App**.

3. Fill out the required details for your application, then click **Create**.

4. Create a .env file, either by running the following command:

    ```bash
    python src/Scripts/create_env_file.py
    ```
    
    or by manually creating the .env with the following format:
    
    ```env
    CLIENT_ID =
    CLIENT_SECRET =
    ```

5. Copy your **Client ID** and **Client Secret** from the Spotify developer dashboard to the corresponding values in the .env file. Example:
    ```env
    CLIENT_ID = "1234"
    CLIENT_SECRET = "5678"
    ```

6. Save the .env file

## Usage

1. Run the main.py file:

    ```bash
    python src/main.py
    ```

    Alternatively, in an IDE, navigate to main.py and run the file.

2. Enter the command **fetch tracks** to get a list of your liked songs from spotify onto your local device.:
    
    ```
    Enter Command: fetch tracks
    ```

3. Enter the command **load** to load your tracks, and other saved data to be used by the program:
    ```
    Enter Command: load
    ```
    

4. Enter the command **help** for a list of all possible commands and info on how to use them:
    ```
    Enter Command: help
    ```

5. When finished with using the program, enter the command **save** to save your tags, templates, and playlists.
    ```
    Enter Command: save
    ```

6. Exit the program using the **quit** command.
    ```
    Enter Command: quit
    ```