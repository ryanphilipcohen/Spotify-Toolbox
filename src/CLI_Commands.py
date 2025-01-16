import Commands
from Datatypes import *
import random
from pathlib import Path
import json

CONFIG_PATH = Path("data/config.json")
with open(CONFIG_PATH, "r") as file:
    config = json.load(file)
DEFAULT_JSON_PATH = config["DEFAULT_JSON_PATH"]
DEFAULT_TRACKS_PATH = config["DEFAULT_TRACKS_PATH"]
DEFAULT_TAGS_PATH = config["DEFAULT_TAGS_PATH"]
DEFAULT_TEMPLATES_PATH = config["DEFAULT_TEMPLATES_PATH"]
DEFAULT_PLAYLISTS_PATH = config["DEFAULT_PLAYLISTS_PATH"]

'''
Functions that directly take input from the command line
Functionality won't be used in a GUI version
'''

# GENERAL COMMANDS

def exit_command():
    print("Exiting the program.")

def help_command():
    pass

# TRACK COMMANDS

def fetch_tracks_command():
    fetch_time = Commands.fetch_tracks_from_API()
    print(f"Fetch time: {fetch_time}")

def load_tracks_command(command: str, track_list: list[Track]):
    if command != "load tracks":
        # user is trying to open a specific file
        json_path = command.removeprefix("load tracks ")
        if json_path and Path(json_path).exists():
            if Commands.check_file_for_json_with_key(json_path, "tracks"):
                new_tracks = Commands.load_tracks_json(json_path)
        else:
            print("The given file does not exist.")
            return
    else:
        # user is trying to open the default tracks file
        if DEFAULT_TRACKS_PATH and Path(DEFAULT_TRACKS_PATH).exists():
            if Commands.check_file_for_json_with_key(DEFAULT_TRACKS_PATH, "tracks"):
                new_tracks = Commands.load_tracks_json()
        else:
            print("The default tracks file does not exist, creating now...")
            Commands.create_json("tracks", DEFAULT_JSON_PATH)
            new_tracks = Commands.load_tracks_json()

    track_list.clear()
    track_list.extend(new_tracks)
    print(f"Number of tracks loaded: {len(track_list)}")

def display_tracks_command(track_list: list[Track]):
    print(track_list)

# TAG COMMANDS

def load_tags_command(command: str, tag_list: list[Tag]):
    if command != "load tags":
        json_path = command.removeprefix("load tags ")
        if json_path and Path(json_path).exists():
            if Commands.check_file_for_json_with_key(json_path, "tags"):
                new_tags = Commands.load_tags_json(json_path)
        else:
            print("The given file does not exist.")
            return
    else:
        if DEFAULT_TAGS_PATH and Path(DEFAULT_TAGS_PATH).exists():
            if Commands.check_file_for_json_with_key(DEFAULT_TAGS_PATH, "tags"):
                new_tags = Commands.load_tags_json()
        else:
            print("The default tags file does not exist, creating now...")
            Commands.create_json("tags", DEFAULT_JSON_PATH)
            new_tags = Commands.load_tags_json()

    tag_list[:] = Commands.remove_duplicate_ids(tag_list + new_tags)
    print(f"Number of tags loaded: {len(tag_list)}")
    

def save_tags_command(command: str, tag_list: list[Tag]):
    if command != "save tags":
        json_path = command.removeprefix("save tags")
        Commands.save_tags_json(tag_list, json_path)
    else:
        Commands.save_tags_json(tag_list)
    print(f"Number of tags saved: {len(tag_list)}")

def create_tag_command(command: str, tag_list: list[Tag]):
    tag_name = command.removeprefix("create tag ")
    tag_list.append(Tag(tag_name))

def remove_tag_command(command: str, tag_list: list[Tag]):
    tag_name = command.removeprefix("remove tag ")
    tag_to_remove = find_tag_to_add(tag_name, tag_list)
    if tag_to_remove:
        tag_list.remove(tag_to_remove)

def add_to_tag_command(command: str, track_list: list[Track], tag_list: list[Tag]):
    tag_name = command.removeprefix("add to tag ")
    tag_to_add_to = find_tag_to_add(tag_name, tag_list)
    
    if not tag_to_add_to:
        return

    # Debugging line to inspect the tag being used
    print(f"Adding track to tag: {tag_to_add_to.name}")

    track_name = input("Name of track: ")
    track_to_add = find_track_to_add(track_list, track_name)

    if track_to_add:
        tag_to_add_to.tracks.append(track_to_add)
        print(f"Added {track_to_add.name} by {track_to_add.artist} to the tag {tag_to_add_to.name}.")
    else:
        print(f"No track found with the name '{track_name}'.")


def remove_from_tag_command(command: str, tag_list: list[Tag]):
    tag_name = command.removeprefix("remove from tag ")
    tag_to_remove_from = find_tag_to_add(tag_name, tag_list)
    if not tag_to_remove_from:
        return

    if not tag_to_remove_from.tracks:
        print("This tag has no tracks.")
        return

    print("Tracks in this tag:")
    for i, track in enumerate(tag_to_remove_from.tracks, 1):
        print(f"{i}: {track.name} by {track.artist} (ID: {track.id})")

    while True:
        try:
            chosen_index = int(input("Which index corresponds to the track to remove? ")) - 1
            if 0 <= chosen_index < len(tag_to_remove_from.tracks):
                removed_track = tag_to_remove_from.tracks.pop(chosen_index)
                print(f"Removed {removed_track.name} by {removed_track.artist} from the tag.")
                break
            else:
                print("Invalid chosen index. Please select a valid index.")
        except ValueError:
            print("Please enter a valid number.")

def display_tag_command(command: str, tag_list: list[Tag]):
    tag_name = command.removeprefix("display tag ")
    tag_to_display = find_tag_to_add(tag_name, tag_list)
    if tag_to_display:
        print(tag_to_display)

def display_tags_command(tag_list: list[Tag]):
    for tag in tag_list:
        print(tag)

# TEMPLATE COMMANDS

def load_templates_command(command: str, template_list: list[Template]):
    if command != "load templates":
        json_path = command.removeprefix("load templates ")
        if json_path and Path(json_path).exists():
            if Commands.check_file_for_json_with_key(json_path, "templates"):
                new_templates = Commands.load_templates_json(json_path)
        else:
            print("The given file does not exist.")
            return
    else:
        if DEFAULT_TEMPLATES_PATH and Path(DEFAULT_TEMPLATES_PATH).exists():
            if Commands.check_file_for_json_with_key(DEFAULT_TEMPLATES_PATH, "templates"):
                new_templates = Commands.load_templates_json()
        else:
            print("The default templates file does not exist, creating now...")
            Commands.create_json("templates", DEFAULT_JSON_PATH)
            new_templates = Commands.load_templates_json()

    template_list[:] = Commands.remove_duplicate_ids(template_list + new_templates)
    print(f"Number of templates loaded: {len(template_list)}")

def save_templates_command(command: str, template_list: list[Template]):
    if command != "save templates":
        json_path = command.removeprefix("save templates")
        Commands.save_templates_json(template_list, json_path)
    else:
        Commands.save_templates_json(template_list)
    print(f"Number of templates saved: {len(template_list)}")

def create_template_command(command: str, template_list: list[Template]):
    template_name = command.removeprefix("create template ")
    template_list.append(Template(template_name, []))

def remove_template_command(command: str, template_list: list[Template]):
    template_name = command.removeprefix("remove template ")

    template_to_remove = find_tag_to_add(template_name, template_list)  # Using same logic as tags for simplicity
    if template_to_remove:
        template_list.remove(template_to_remove)
        print(f"Removed template: {template_name}")

def add_to_template_command(command: str, track_list: list[Track], tag_list: list[Tag], template_list: list[Template]):
    template_name = command.removeprefix("add to template ")
    template_to_add_to = find_template_to_add(template_name, template_list)  # Reusing logic for simplicity

    if not template_to_add_to:
        print(f"Template '{template_name}' not found.")
        return

    while True:
        type_to_add = input("Are you adding a track or a tag? ").lower()
        if type_to_add in ["track", "tag"]:
            break
        print("Invalid input. Please enter 'track' or 'tag'.")

    if type_to_add == "track":
        track_name = input("Name of Track: ")
        track_to_add = find_track_to_add(track_list, track_name)

        if track_to_add:
            item_to_add = track_to_add
            item_type = "track"
        else:
            print("Track not found.")
            return
    else:
        tag_name = input("Name of Tag: ")
        tag_to_add = find_tag_to_add(tag_name, tag_list)

        if tag_to_add:
            item_to_add = tag_to_add
            item_type = "tag"
        else:
            print("Tag not found.")
            return

    # Check if the template is empty at index 0
    if not template_to_add_to.contents or not template_to_add_to.contents[0]:
        print(f"Template '{template_name}' is empty or has no items at index 0. Adding item directly at index 0 with probability 1.0.")
        item_dict = {
            "item": item_to_add,
            "probability": 1.0,
            "type": item_type
        }

        if not template_to_add_to.contents:
            template_to_add_to.contents.append([])  # Ensure the contents list exists

        template_to_add_to.contents[0].append(item_dict)
    else:
        # Existing logic for specifying where to add the item
        print("Current items in the template:")
        for i, index_items in enumerate(template_to_add_to.contents):
            items_str = ", ".join(
                f"{item['item'].name} ({item['probability']})" for item in index_items
            )
            print(f"Position {i + 1}: {items_str}")

        while True:
            position = input("Would you like to add it 'before', 'after', or 'same' as a position? ").lower()
            if position in ["before", "after", "same"]:
                break
            print("Invalid input. Please enter 'before', 'after', or 'same'.")

        # Safely get the index for position
        while True:
            try:
                index_to_add = int(input("Enter the position to add the item: ")) - 1
                if index_to_add >= 0:
                    break
                else:
                    print("Invalid index. Please enter a valid positive index.")
            except ValueError:
                print("Please enter a valid number for the position.")

        item_dict = {
            "item": item_to_add,
            "probability": None,  # Placeholder until set
            "type": item_type
        }

        if position == "same":
            if index_to_add < len(template_to_add_to.contents):
                existing_items = template_to_add_to.contents[index_to_add]
                if not existing_items:  # If the index is empty, set probability to 1.0
                    item_dict["probability"] = 1.0
                else:
                    adjust_probabilities(existing_items, item_dict)
                existing_items.append(item_dict)
            else:
                # Index doesn't exist; create it and add item
                item_dict["probability"] = 1.0
                while len(template_to_add_to.contents) <= index_to_add:
                    template_to_add_to.contents.append([])  # Ensure the index exists
                template_to_add_to.contents[index_to_add].append(item_dict)
        else:
            # Handle "before" and "after"
            item_dict["probability"] = 1.0
            new_index = index_to_add if position == "before" else index_to_add + 1
            while len(template_to_add_to.contents) < new_index:
                template_to_add_to.contents.append([])  # Ensure the index exists
            template_to_add_to.contents.insert(new_index, [item_dict])

    print(f"Added {item_to_add.name} to template {template_to_add_to.name}.")

def remove_from_template_command(command: str, template_list: list[Template]):
    template_name = command.removeprefix("remove from template ")
    template_to_remove_from = find_tag_to_add(template_name, template_list)  # Reusing logic for simplicity

    if template_to_remove_from:
        print("Current items in the template:")
        for i, index_items in enumerate(template_to_remove_from.contents):
            items_str = ", ".join(
                f"{item['item'].name} ({item['probability']})" for item in index_items
            )
            print(f"Position {i + 1}: {items_str}")

        # Safely get the index to remove
        while True:
            try:
                index_to_remove = int(input("Enter the position of the item to remove: ")) - 1
                if 0 <= index_to_remove < len(template_to_remove_from.contents):
                    break
                else:
                    print("Invalid position. Please enter a valid position.")
            except ValueError:
                print("Please enter a valid number for the position.")

        if len(template_to_remove_from.contents[index_to_remove]) > 1:
            print("Multiple items exist at this position. Please select the one to remove:")
            for idx, item in enumerate(template_to_remove_from.contents[index_to_remove]):
                print(f"{idx + 1}: {item['item'].name} (probability: {item['probability']})")

            # Safely get the item index to remove
            while True:
                try:
                    item_idx = int(input("Enter the number corresponding to the item to remove: ")) - 1
                    if 0 <= item_idx < len(template_to_remove_from.contents[index_to_remove]):
                        break
                    else:
                        print("Invalid item number. Please select a valid number.")
                except ValueError:
                    print("Please enter a valid number for the item to remove.")

            removed_item = template_to_remove_from.contents[index_to_remove].pop(item_idx)
            print(f"Removed {removed_item['item'].name} from template {template_to_remove_from.name}.")
        else:
            removed_item = template_to_remove_from.contents.pop(index_to_remove)
            print(f"Removed {removed_item[0]['item'].name} from template {template_to_remove_from.name}.")

        # If the position is now empty after removing an item, delete the position
        if index_to_remove < len(template_to_remove_from.contents) and not template_to_remove_from.contents[index_to_remove]:
            del template_to_remove_from.contents[index_to_remove]

        print("Updated template contents:")
        for i, index_items in enumerate(template_to_remove_from.contents):
            items_str = ", ".join(
                f"{item['item'].name} ({item['probability']})" for item in index_items
            )
            print(f"Position {i + 1}: {items_str}")

def display_template_command(command: str, template_list: list[Template]):
    template_name = command.removeprefix("display template ")
    template_to_display = find_template_to_add(template_name, template_list)
    if template_to_display:
        print(template_to_display)

def display_templates_command(template_list: list[Template]):
    for template in template_list:
        print(template)

# PLAYLIST COMMANDS

def load_playlists_command(command: str, playlist_list: list[Playlist]):
    if command != "load playlists":
        json_path = command.removeprefix("load playlists ")
        if json_path and Path(json_path).exists():
            if Commands.check_file_for_json_with_key(json_path, "playlists"):
                new_playlists = Commands.load_playlists_json(json_path)
        else:
            print("The given file does not exist.")
            return
    else:
        if DEFAULT_PLAYLISTS_PATH and Path(DEFAULT_PLAYLISTS_PATH).exists():
            if Commands.check_file_for_json_with_key(DEFAULT_PLAYLISTS_PATH, "playlists"):
                new_playlists = Commands.load_playlists_json()
        else:
            print("The default playlists file does not exist, creating now...")
            Commands.create_json("playlists", DEFAULT_JSON_PATH)
            new_playlists = Commands.load_playlists_json()

    playlist_list[:] = Commands.remove_duplicate_ids(playlist_list + new_playlists)
    print(f"Number of playlists loaded: {len(playlist_list)}")

def save_playlists_command(command: str, playlist_list: list[Playlist]):
    if command != "save playlists":
        json_path = command.removeprefix("save playlists")
        Commands.save_playlists_json(playlist_list, json_path)
    else:
        Commands.save_playlists_json(playlist_list)
    print(f"Number of playlists saved: {len(playlist_list)}")

def create_playlist_command(command: str, playlist_list: list[Playlist]):
    playlist_name = command.removeprefix("create playlist ")
    playlist_list.append(Playlist(playlist_name))

def remove_playlist_command(command: str, playlist_list: list[Playlist]):
    playlist_name = command.removeprefix("remove playlist ")
    playlist_to_remove = find_playlist_to_add(playlist_name, playlist_list)
    if playlist_to_remove:
        playlist_list.remove(playlist_to_remove)

def generate_playlist_from_template_command(command: str, tag_list: list[Tag], template_list: list[Template], playlist_list: list[Playlist]):
    playlist_name = command.removeprefix("generate playlist ")

    if len(template_list) > 0:
        print("Generate from which template?")
        for idx, template in enumerate(template_list):
            print(f"{idx + 1}: {template.name}")
        
        # Safely get the template index
        while True:
            try:
                chosen_index = int(input("Enter the number corresponding to the template: ")) - 1
                if 0 <= chosen_index < len(template_list):
                    template_to_generate_from = template_list[chosen_index]
                    break
                else:
                    print("Invalid index. Please enter a valid index corresponding to the template.")
            except ValueError:
                print("Please enter a valid number for the template index.")

        playlist_tracks = []
        tag_selection_sets = {tag.name: set() for tag in tag_list}  # Tracks the selected tracks per tag

        for position_items in template_to_generate_from.contents:
            selected_item = None
            probability_sum = sum(item['probability'] for item in position_items)

            if probability_sum > 0:
                random_value = random.uniform(0, probability_sum)
                cumulative_probability = 0.0
                tries = 0
                max_tries = 100  # Prevents an infinite loop if something goes wrong

                while tries < max_tries:
                    tries += 1
                    for item in position_items:
                        cumulative_probability += item['probability']
                        if random_value <= cumulative_probability:
                            selected_item = item['item']
                            break

                    # Prevent duplicates if the item is already added
                    if isinstance(selected_item, Track) and selected_item not in playlist_tracks:
                        playlist_tracks.append(selected_item)
                        print(f"Added track: {selected_item.name} by {selected_item.artist} to the playlist.")
                        break

                    elif isinstance(selected_item, Tag):
                        # Avoid selecting the same track from a tag
                        available_tracks = [
                            track for track in selected_item.tracks 
                            if track not in tag_selection_sets[selected_item.name]
                        ]
                        
                        if available_tracks:
                            selected_track = random.choice(available_tracks)
                            playlist_tracks.append(selected_track)
                            tag_selection_sets[selected_item.name].add(selected_track)
                            print(f"Added track: {selected_track.name} from tag {selected_item.name} to the playlist.")
                            break
                        else:
                            # Reset chosen tracks and retry
                            print(f"All tracks from tag {selected_item.name} have been chosen. Resetting and continuing.")
                            tag_selection_sets[selected_item.name].clear()

                else:
                    print(f"Max tries reached. No item was selected from position.")

        print(f"Generated playlist '{playlist_name}' with {len(playlist_tracks)} tracks.")
        playlist_list.append(Playlist(playlist_name, playlist_tracks))

    else:
        print("No templates available to generate from.")

def upload_playlist_command(command: str, playlist_list: list[Playlist]):
    playlist_name = command.removeprefix("upload playlist ")
    playlist = find_playlist_to_add(playlist_name, playlist_list)
    Commands.upload_playlist_to_spotify(playlist)

# HELPER FUNCTIONS

def find_track_to_add(track_list: list[Track], track_name: str):
    num_of_tracks = Commands.find_num_of_items_with_attribute(track_list, "name", track_name)

    if num_of_tracks == 0:
        return None
    elif num_of_tracks == 1:
        return Commands.find_items_from_attribute(track_list, "name", track_name)[0]
    else:
        possible_tracks = Commands.find_items_from_attribute(track_list, "name", track_name)
        print("Multiple tracks found with this name:")
        for i, track in enumerate(possible_tracks, 1):
            print(f"{i}: {track.name} by {track.artist} (ID: {track.id})")

        while True:
            try:
                chosen_index = int(input("Which index corresponds to the correct track? ")) - 1
                if 0 <= chosen_index < len(possible_tracks):
                    return possible_tracks[chosen_index]
                else:
                    print("Invalid chosen index. Please select a valid index.")
            except ValueError:
                print("Please enter a valid number.")

def find_tag_to_add(tag_name: str, tag_list: list[Tag]):
    num_of_tags = Commands.find_num_of_items_with_attribute(tag_list, "name", tag_name)

    if num_of_tags == 0:
        print(f"No tag with the name '{tag_name}' found.")
        return None
    elif num_of_tags == 1:
        return Commands.find_items_from_attribute(tag_list, "name", tag_name)[0]
    else:
        possible_tags = Commands.find_items_from_attribute(tag_list, "name", tag_name)
        print("Multiple tags found with this name:")
        for i, tag in enumerate(possible_tags, 1):
            print(f"{i}: {tag.name} (ID: {tag.id})")

        while True:
            try:
                chosen_index = int(input("Which index corresponds to the correct tag? ")) - 1
                if 0 <= chosen_index < len(possible_tags):
                    return possible_tags[chosen_index]
                else:
                    print("Invalid chosen index. Please select a valid number.")
            except ValueError:
                print("Invalid input. Please enter a number.")

def find_template_to_add(template_name: str, template_list: list[Template]):
    num_of_templates = Commands.find_num_of_items_with_attribute(template_list, "name", template_name)

    if num_of_templates == 0:
        print(f"No template with the name '{template_name}' found.")
        return None
    elif num_of_templates == 1:
        return Commands.find_items_from_attribute(template_list, "name", template_name)[0]
    else:
        possible_templates = Commands.find_items_from_attribute(template_list, "name", template_name)
        print("Multiple templates found with this name:")
        for i, template in enumerate(possible_templates, 1):
            print(f"{i}: {template.name} (ID: {template.id})")

        while True:
            try:
                chosen_index = int(input("Which index corresponds to the correct template? ")) - 1
                if 0 <= chosen_index < len(possible_templates):
                    return possible_templates[chosen_index]
                else:
                    print("Invalid chosen index. Please select a valid number.")
            except ValueError:
                print("Invalid input. Please enter a number.")

def find_playlist_to_add(playlist_name: str, playlist_list: list[Playlist]):
    num_of_playlists = Commands.find_num_of_items_with_attribute(playlist_list, "name", playlist_name)

    if num_of_playlists == 0:
        print(f"No playlist with the name '{playlist_name}' found.")
        return None
    elif num_of_playlists == 1:
        return Commands.find_items_from_attribute(playlist_list, "name", playlist_name)[0]
    else:
        possible_playlists = Commands.find_items_from_attribute(playlist_list, "name", playlist_name)
        print("Multiple playlists found with this name:")
        for i, playlist in enumerate(possible_playlists, 1):
            print(f"{i + 1}: {playlist.name} (ID: {playlist.id})")

        while True:
            try:
                chosen_index = int(input("Which index corresponds to the correct playlist? ")) - 1
                if 0 <= chosen_index < len(possible_playlists):
                    return possible_playlists[chosen_index]
                else:
                    print("Invalid chosen index. Please select a valid number.")
            except ValueError:
                print("Invalid input. Please enter a number.")

def adjust_probabilities(existing_items: list[dict], new_item: dict) -> None:
    new_probability = new_item["probability"]
    total_existing_probability = sum(item["probability"] for item in existing_items)
    scaling_factor = (1.0 - new_probability) / total_existing_probability if total_existing_probability > 0 else 0

    for item in existing_items:
        item["probability"] *= scaling_factor

    existing_items.append(new_item)