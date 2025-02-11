import random
from pathlib import Path
import copy

import commands
from datatypes import Track, Tag, Template, Playlist


CONFIG_PATH = Path("data/config.json")
config = commands.load_config(CONFIG_PATH)
DEFAULT_BACKUP_PATH = Path(config["DEFAULT_BACKUP_PATH"])
DEFAULT_JSON_PATH = Path(config["DEFAULT_JSON_PATH"])
DEFAULT_TRACKS_PATH = Path(config["DEFAULT_TRACKS_PATH"])
DEFAULT_TAGS_PATH = Path(config["DEFAULT_TAGS_PATH"])
DEFAULT_TEMPLATES_PATH = Path(config["DEFAULT_TEMPLATES_PATH"])
DEFAULT_PLAYLISTS_PATH = Path(config["DEFAULT_PLAYLISTS_PATH"])

"""
Functions that directly take input from the command line
Functionality won't be used in a GUI version
"""

# GENERAL COMMANDS


def exit_command(
    current_tag_list: list[Tag],
    saved_tag_list: list[Tag],
    current_template_list: list[Template],
    saved_template_list: list[Template],
    current_playlist_list: list[Playlist],
    saved_playlist_list: list[Playlist],
) -> None:
    """Command to exit the CLI program.

    This function checks if there are any unsaved changes in the tags, templates, or playlists.
    If changes are detected, the user is prompted to save them before exiting.
    The user can choose to save the changes or exit without saving.

    Args:
        current_tag_list (list[Tag]): Tag list storing the changes made since the most recent save.
        saved_tag_list (list[Tag]): Tag list storing the last saved state.
        current_template_list (list[Template]): Template list storing the changes made since the most recent save.
        saved_template_list (list[Template]): Template list storing the last saved state.
        current_playlist_list (list[Playlist]): Playlist list storing the changes made since the most recent save.
        saved_playlist_list (list[Playlist]): Playlist list storing the last saved state.
    """
    if commands.changes_made_to_data(
        current_tag_list,
        saved_tag_list,
        current_template_list,
        saved_template_list,
        current_playlist_list,
        saved_playlist_list,
    ):
        while True:
            save_changes = input(
                "Would you like to save your changes before exiting? (y/n) "
            )
            if save_changes in ("y", "n"):
                if save_changes == "y":
                    save_tags_command("save tags", current_tag_list, saved_tag_list)
                    save_templates_command(
                        "save templates", current_template_list, saved_template_list
                    )
                    save_playlists_command(
                        "save playlists", current_playlist_list, saved_playlist_list
                    )
                    break
                if save_changes == "n":
                    break
            else:
                print("Invalid input. Please enter 'y' or 'n'.")
    print("Exiting the program.")


def help_command() -> None:
    """Displays all available commands in the CLI."""
    help_message = """
    Spotify Toolbox CLI v1.0.1 - Command List

    GENERAL COMMANDS:
    exit | quit | q                - Exit the program
    help | commands                - Display this help message
    backup [filename]              - Backup all current data
    load | l                       - Reload tracks, tags, templates, and playlists
    save | s                       - Save tags, templates, and playlists

    TRACK COMMANDS:
    fetch tracks                   - Fetch tracks from Spotify
    load tracks [filename]         - Load tracks from a file
    display tracks                 - Display all loaded tracks

    TAG COMMANDS:
    load tags [filename]           - Load tags from a file
    save tags [filename]           - Save tags to a file
    create tag [tag_name]          - Create a new tag
    remove tag [tag_name]          - Remove a specific tag
    remove tags                    - Remove all tags
    add to tag [tag_name] [track_id]   - Add a track to a tag
    remove from tag [tag_name] [track_id] - Remove a track from a tag
    clear tag [tag_name]           - Remove all tracks from a tag
    display tag [tag_name]         - Show tracks in a tag
    display tags                   - Show all tags
    generate tags [method]         - Automatically generate tags, currently supports 'artist' and 'duration'

    TEMPLATE COMMANDS:
    load templates [filename]      - Load templates from a file
    save templates [filename]      - Save templates to a file
    create template [template_name] - Create a new playlist template
    remove template [template_name] - Remove a specific template
    add to template [template_name] [track_id|tag_name] - Add a track or tag to a template
    remove from template [template_name] [track_id|tag_name] - Remove a track or tag from a template
    display template [template_name] - Show the contents of a template
    display templates              - Show all templates

    PLAYLIST COMMANDS:
    load playlists [filename]      - Load playlists from a file
    save playlists [filename]      - Save playlists to a file
    create playlists [playlist_name] - Create a new playlist
    remove playlists [playlist_name] - Remove a specific playlist
    generate playlist [template_name] - Generate a playlist from a template
    upload playlist [playlist_name] - Upload a playlist to Spotify
    """
    print(help_message)


def backup_command(
    command: str,
    current_track_list: list[Track],
    current_tag_list: list[Tag],
    current_template_list: list[Template],
    current_playlist_list: list[Playlist],
) -> None:
    """Command to backup the current state of the data.

    Args:
        command (str): Command entered by the user, containing the path to save the backup to.
        current_track_list (list[Track]): Track list storing the changes made since the most recent save.
        current_tag_list (list[Tag]): Tag list storing the changes made since the most recent save.
        current_template_list (list[Template]): Template list storing the changes made since the most recent save.
        current_playlist_list (list[Playlist]): Playlist list storing the changes made since the most recent save.
    """
    if command != "backup":
        json_path = command.removeprefix("backup ")
        commands.backup(
            current_track_list,
            current_tag_list,
            current_template_list,
            current_playlist_list,
            json_path,
        )
    else:
        commands.backup(
            current_track_list,
            current_tag_list,
            current_template_list,
            current_playlist_list,
        )


# TRACK COMMANDS


def fetch_tracks_command() -> None:
    """Command to fetch tracks from the Spotify API and update the track list.

    Prints the time taken to fetch the tracks from the API.
    """
    fetch_time = commands.fetch_tracks_from_API()
    print(f"Fetch time: {fetch_time}")


def load_tracks_command(command: str, track_list: list[Track]) -> None:
    """Command to load tracks from a JSON file into the track list.

    If the command is 'load tracks', the default tracks file is loaded.

    Args:
        command (str): Command entered by the user, containing the path to load the tracks from.
        track_list (list[Track]): Track list to load the tracks into.
    """
    new_tracks = []
    if command != "load tracks":
        # user is trying to open a specific file
        json_path = command.removeprefix("load tracks ")
        if json_path and Path(json_path).exists():
            if commands.check_file_for_json_with_key(json_path, "tracks"):
                new_tracks = commands.load_tracks_json(json_path)
        else:
            print("The given file does not exist.")
            return
    else:
        # user is trying to open the default tracks file
        if DEFAULT_TRACKS_PATH and Path(DEFAULT_TRACKS_PATH).exists():
            if commands.check_file_for_json_with_key(DEFAULT_TRACKS_PATH, "tracks"):
                new_tracks = commands.load_tracks_json()
        else:
            print("The default tracks file does not exist, creating now...")
            commands.create_json("tracks", DEFAULT_JSON_PATH)
            new_tracks = commands.load_tracks_json()

    track_list.clear()
    track_list.extend(new_tracks)
    print(f"Number of tracks loaded: {len(track_list)}")


def display_tracks_command(track_list: list[Track]) -> None:
    """Command to display the tracks in the track list.

    Args:
        track_list (list[Track]): The list of tracks to display.
    """
    print(track_list)


# TAG COMMANDS


def load_tags_command(command: str, tag_list: list[Tag]) -> None:
    """Command to load tags from a JSON file into the tag list.

    Args:
        command (str): The command entered by the user, containing the path to load the tags from.
        tag_list (list[Tag]): Tag list to load the tags into.
    """
    new_tags = []
    if command != "load tags":
        json_path = command.removeprefix("load tags ")
        if json_path and Path(json_path).exists():
            if commands.check_file_for_json_with_key(json_path, "tags"):
                new_tags = commands.load_tags_json(json_path)
        else:
            print("The given file does not exist.")
            return
    else:
        if DEFAULT_TAGS_PATH and Path(DEFAULT_TAGS_PATH).exists():
            if commands.check_file_for_json_with_key(DEFAULT_TAGS_PATH, "tags"):
                new_tags = commands.load_tags_json()
        else:
            print("The default tags file does not exist, creating now...")
            commands.create_json("tags", DEFAULT_JSON_PATH)
            new_tags = commands.load_tags_json()

    tag_list[:] = commands.remove_duplicate_ids(tag_list + new_tags)
    print(f"Number of tags loaded: {len(tag_list)}")


def save_tags_command(
    command: str, current_tag_list: list[Tag], saved_tag_list: list[Tag]
) -> None:
    """Command to save the current tag list to a JSON file.

    Args:
        command (str): Command entered by the user, containing the path to save the tags to.
        current_tag_list (list[Tag]): Tag list storing the changes made since the most recent save.
        saved_tag_list (list[Tag]): Tag list storing the last saved state.
    """
    if command != "save tags":
        json_path = command.removeprefix("save tags ")
        commands.save_tags_json(current_tag_list, json_path)
    else:
        commands.save_tags_json(current_tag_list)

    saved_tag_list[:] = copy.deepcopy(current_tag_list)

    print(f"Number of tags saved: {len(saved_tag_list)}")


def create_tag_command(command: str, tag_list: list[Tag]) -> None:
    """Command to create a new tag and add it to the tag list.

    Args:
        command (str): Command entered by the user, containing the name of the tag to create.
        tag_list (list[Tag]): Tag list to add the new tag to.
    """
    tag_name = command.removeprefix("create tag ")
    tag_list.append(Tag(tag_name))


def remove_tag_command(command: str, tag_list: list[Tag]) -> None:
    """Command to remove a tag from the tag list.

    Args:
        command (str): Command entered by the user, containing the name of the tag to remove.
        tag_list (list[Tag]): Tag list to remove the tag from.
    """
    tag_name = command.removeprefix("remove tag ")
    tag_to_remove = find_tag_to_add(tag_name, tag_list)
    if tag_to_remove:
        tag_list.remove(tag_to_remove)


def add_to_tag_command(
    command: str, track_list: list[Track], tag_list: list[Tag]
) -> None:
    """Command to add a track to a tag.

    Args:
        command (str): Command entered by the user, containing the name of the tag to add to.
        track_list (list[Track]): The list of tracks to add to the tag.
        tag_list (list[Tag]): The list of tags to add the track to.
    """
    tag_name = command.removeprefix("add to tag ")
    tag_to_add_to = find_tag_to_add(tag_name, tag_list)

    if not tag_to_add_to:
        return

    print(f"Adding track to tag: {tag_to_add_to.name}")

    track_name = input("Name of track: ")
    track_to_add = find_track_to_add(track_name, track_list)

    if track_to_add:
        tag_to_add_to.tracks.append(track_to_add)
        print(
            f"Added {track_to_add.name} by {track_to_add.artist} to the tag {tag_to_add_to.name}."
        )
    else:
        print(f"No track found with the name '{track_name}'.")


def remove_from_tag_command(command: str, tag_list: list[Tag]) -> None:
    """Command to remove a track from a tag.

    Args:
        command (str): Command entered by the user, containing the name of the tag to remove from.
        tag_list (list[Tag]): The list of tags to remove the track from.
    """
    tag_name = command.removeprefix("remove from tag ")
    tag_to_remove_from = find_tag_to_add(tag_name, tag_list)
    if not tag_to_remove_from:
        return

    if not tag_to_remove_from.tracks:
        print("This tag has no tracks.")
        return

    print("Tracks in this tag:")
    for i, track in enumerate(tag_to_remove_from.tracks, 1):
        print(f"{i}: {track.name} by {track.artist} (ID: {track.track_id})")

    while True:
        try:
            chosen_index = (
                int(input("Which index corresponds to the track to remove? ")) - 1
            )
            if 0 <= chosen_index < len(tag_to_remove_from.tracks):
                removed_track = tag_to_remove_from.tracks.pop(chosen_index)
                print(
                    f"Removed {removed_track.name} by {removed_track.artist} from the tag."
                )
                break
            else:
                print("Invalid chosen index. Please select a valid index.")
        except ValueError:
            print("Please enter a valid number.")


def clear_tag_command(command: str, tag_list: list[Tag]) -> None:
    """Command to clear all tracks from a tag.

    Args:
        command (str): Command entered by the user, containing the name of the tag to clear.
        tag_list (list[Tag]): The list of tags to clear the tracks from.
    """
    tag_name = command.removeprefix("clear tag ")
    tag_to_clear = find_tag_to_add(tag_name, tag_list)
    if tag_to_clear:
        tag_to_clear.tracks.clear()
        print(f"Cleared all tracks from tag {tag_to_clear.name}.")


def remove_tags_command(tag_list: list[Tag]) -> None:
    """Command to remove all tags from the tag list.

    Args:
        tag_list (list[Tag]): The list of tags to remove.
    """
    tag_list.clear()
    print("Removed all tracks from all tags.")


def display_tag_command(command: str, tag_list: list[Tag]) -> None:
    """Command to display a tag, printing it to the command line interface.

    Args:
        command (str): Command entered by the user, containing the name of the tag to display.
        tag_list (list[Tag]): The list of tags to search for the tag in.
    """
    tag_name = command.removeprefix("display tag ")
    tag_to_display = find_tag_to_add(tag_name, tag_list)
    if tag_to_display:
        print(tag_to_display)


def display_tags_command(tag_list: list[Tag]) -> None:
    """Command to display all tags in the tag list.

    Args:
        tag_list (list[Tag]): The list of tags to display.
    """
    for tag in tag_list:
        print(tag.name)


def generate_tags_command(
    command: str, track_list: list[Track], tag_list: list[Tag]
) -> None:
    """Command to generate tags based on track attributes.

    Supports generating tags based on the artist and duration.

    Args:
        command (str): Command entered by the user, containing the type of tag generation.
        track_list (list[Track]): The list of tracks to generate tags from.
        tag_list (list[Tag]): The list of tags to add the generated tags to.
    """
    new_tags = []

    tag_name = command.removeprefix("generate tags ")
    if tag_name in ("artist", "duration"):
        if tag_name == "artist":
            new_tags = commands.generate_tags_by_artist(track_list)
        elif tag_name == "duration":
            new_tags = commands.generate_tags_by_duration(track_list)
    else:
        print("Invalid tag generation type. Please enter 'artist' or 'duration'.")
        return

    # Due to auto-generated tags having a new ID each time, they won't remove unless manually done by name
    auto_tags = [tag for tag in tag_list if tag.creator == "auto"]
    user_tags = [tag for tag in tag_list if tag.creator == "user"]
    new_tags[:] = commands.remove_duplicate_names(auto_tags + new_tags)
    for new_tag in new_tags:
        print(new_tag.name)

    tag_list[:] = commands.remove_duplicate_ids(user_tags + new_tags)
    print(f"Number of tags generated: {len(new_tags)}")


# TEMPLATE COMMANDS


def load_templates_command(command: str, template_list: list[Template]) -> None:
    """Command to load templates from a JSON file into the template list.

    Args:
        command (str): The command entered by the user, containing the path to load the templates from.
        template_list (list[Template]): Template list to load the templates into.
    """
    new_templates = []

    if command != "load templates":
        json_path = command.removeprefix("load templates ")
        if json_path and Path(json_path).exists():
            if commands.check_file_for_json_with_key(json_path, "templates"):
                new_templates = commands.load_templates_json(json_path)
        else:
            print("The given file does not exist.")
            return
    else:
        if DEFAULT_TEMPLATES_PATH and Path(DEFAULT_TEMPLATES_PATH).exists():
            if commands.check_file_for_json_with_key(
                DEFAULT_TEMPLATES_PATH, "templates"
            ):
                new_templates = commands.load_templates_json()
        else:
            print("The default templates file does not exist, creating now...")
            commands.create_json("templates", DEFAULT_JSON_PATH)
            new_templates = commands.load_templates_json()

    template_list[:] = commands.remove_duplicate_ids(template_list + new_templates)
    print(f"Number of templates loaded: {len(template_list)}")


def save_templates_command(
    command: str,
    current_template_list: list[Template],
    saved_template_list: list[Template],
) -> None:
    """Command to save the current template list to a JSON file.

    Args:
        command (str): Command entered by the user, containing the path to save the templates to.
        current_template_list (list[Template]): Template list storing the changes made since the most recent save.
        saved_template_list (list[Template]): Template list storing the last saved state.
    """
    if command != "save templates":
        json_path = command.removeprefix("save templates ")
        commands.save_templates_json(current_template_list, json_path)
    else:
        commands.save_templates_json(current_template_list)

    saved_template_list[:] = copy.deepcopy(current_template_list)

    print(f"Number of templates saved: {len(saved_template_list)}")


def create_template_command(command: str, template_list: list[Template]) -> None:
    """Command to create a new template and add it to the template list.

    Args:
        command (str): Command entered by the user, containing the name of the template to create.
        template_list (list[Template]): Template list to add the new template to.
    """
    template_name = command.removeprefix("create template ")
    template_list.append(Template(template_name, []))


def remove_template_command(command: str, template_list: list[Template]) -> None:
    """Command to remove a template from the template list.

    Args:
        command (str): Command entered by the user, containing the name of the template to remove.
        template_list (list[Template]): Template list to remove the template from.
    """
    template_name = command.removeprefix("remove template ")

    template_to_remove = find_tag_to_add(template_name, template_list)
    if template_to_remove:
        template_list.remove(template_to_remove)
        print(f"Removed template: {template_name}")


def add_to_template_command(
    command: str,
    track_list: list[Track],
    tag_list: list[Tag],
    template_list: list[Template],
) -> None:
    """Command to add to a template.

    Supports adding a track or tag to a template.
    Additions to template can be added before or after a position, or at the same position.
    Items added to the same position will have their probabilities adjusted to fit the new item.

    Args:
        command (str): Command entered by the user, containing the name of the template to add to.
        track_list (list[Track]): The list of tracks to add a track from to the template.
        tag_list (list[Tag]): The list of tags to add add a tag from to the template.
        template_list (list[Template]): The list of templates to add the item to.
    """
    template_name = command.removeprefix("add to template ")
    template_to_add_to = find_template_to_add(template_name, template_list)

    if not template_to_add_to:
        print(f"Template '{template_name}' not found.")
        return

    while True:
        type_to_add = input("Are you adding a track or a tag? ").lower()
        if type_to_add in ("track", "tag"):
            break
        print("Invalid input. Please enter 'track' or 'tag'.")

    if type_to_add == "track":
        track_name = input("Name of Track: ")
        track_to_add = find_track_to_add(track_name, track_list)

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
        print(
            f"Template '{template_name}' is empty or has no items at index 0. Adding item directly at index 0 with probability 1.0."
        )
        item_dict = {"item": item_to_add, "probability": 1.0, "type": item_type}

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
            position = input(
                "Would you like to add it 'before', 'after', or 'same' as a position? "
            ).lower()
            if position in ("before", "after", "same"):
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
            "type": item_type,
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


def remove_from_template_command(command: str, template_list: list[Template]) -> None:
    """Command to remove an item from a template.

    Asks the user to select the position of item to remove from the template.

    Args:
        command (str): Command entered by the user, containing the name of the template to remove from.
        template_list (list[Template]): The list of templates to remove the item from.
    """
    template_name = command.removeprefix("remove from template ")
    template_to_remove_from = find_tag_to_add(template_name, template_list)

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
                index_to_remove = (
                    int(input("Enter the position of the item to remove: ")) - 1
                )
                if 0 <= index_to_remove < len(template_to_remove_from.contents):
                    break
                print("Invalid position. Please enter a valid position.")
            except ValueError:
                print("Please enter a valid number for the position.")

        if len(template_to_remove_from.contents[index_to_remove]) > 1:
            print(
                "Multiple items exist at this position. Please select the one to remove:"
            )
            for idx, item in enumerate(
                template_to_remove_from.contents[index_to_remove]
            ):
                print(
                    f"{idx + 1}: {item['item'].name} (probability: {item['probability']})"
                )

            # Safely get the item index to remove
            while True:
                try:
                    item_idx = (
                        int(
                            input(
                                "Enter the number corresponding to the item to remove: "
                            )
                        )
                        - 1
                    )
                    if (
                        0
                        <= item_idx
                        < len(template_to_remove_from.contents[index_to_remove])
                    ):
                        break
                    print("Invalid item number. Please select a valid number.")
                except ValueError:
                    print("Please enter a valid number for the item to remove.")

            removed_item = template_to_remove_from.contents[index_to_remove].pop(
                item_idx
            )
            print(
                f"Removed {removed_item['item'].name} from template {template_to_remove_from.name}."
            )
        else:
            removed_item = template_to_remove_from.contents.pop(index_to_remove)
            print(
                f"Removed {removed_item[0]['item'].name} from template {template_to_remove_from.name}."
            )

        # If the position is now empty after removing an item, delete the position
        if (
            index_to_remove < len(template_to_remove_from.contents)
            and not template_to_remove_from.contents[index_to_remove]
        ):
            del template_to_remove_from.contents[index_to_remove]

        print("Updated template contents:")
        for i, index_items in enumerate(template_to_remove_from.contents):
            items_str = ", ".join(
                f"{item['item'].name} ({item['probability']})" for item in index_items
            )
            print(f"Position {i + 1}: {items_str}")


def display_template_command(command: str, template_list: list[Template]) -> None:
    """Command to display a template.

    Displays information about the template, and the items within the template.

    Args:
        command (str): Command entered by the user, containing the name of the template to display.
        template_list (list[Template]): The list of templates to search for the template in.
    """
    template_name = command.removeprefix("display template ")
    template_to_display = find_template_to_add(template_name, template_list)
    if template_to_display:
        print(template_to_display)


def display_templates_command(template_list: list[Template]) -> None:
    """Command to display all templates in the template list.

    Args:
        template_list (list[Template]): The list of templates to display.
    """
    for template in template_list:
        print(template)


# PLAYLIST COMMANDS


def load_playlists_command(command: str, playlist_list: list[Playlist]) -> None:
    """Command to load playlists from a JSON file into the playlist list.

    Args:
        command (str): Command entered by the user, containing the path to load the playlists from.
        playlist_list (list[Playlist]): Playlist list to load the playlists into.
    """
    new_playlists = []

    if command != "load playlists":
        json_path = command.removeprefix("load playlists ")
        if json_path and Path(json_path).exists():
            if commands.check_file_for_json_with_key(json_path, "playlists"):
                new_playlists = commands.load_playlists_json(json_path)
        else:
            print("The given file does not exist.")
            return
    else:
        if DEFAULT_PLAYLISTS_PATH and Path(DEFAULT_PLAYLISTS_PATH).exists():
            if commands.check_file_for_json_with_key(
                DEFAULT_PLAYLISTS_PATH, "playlists"
            ):
                new_playlists = commands.load_playlists_json()
        else:
            print("The default playlists file does not exist, creating now...")
            commands.create_json("playlists", DEFAULT_JSON_PATH)
            new_playlists = commands.load_playlists_json()

    playlist_list[:] = commands.remove_duplicate_ids(playlist_list + new_playlists)
    print(f"Number of playlists loaded: {len(playlist_list)}")


def save_playlists_command(
    command: str,
    current_playlist_list: list[Playlist],
    saved_playlist_list: list[Playlist],
) -> None:
    """Command to save the current playlist list to a JSON file.

    Args:
        command (str): Command entered by the user, containing the path to save the playlists to.
        current_playlist_list (list[Playlist]): Playlist list storing the changes made since the most recent
        saved_playlist_list (list[Playlist]): Playlist list storing the last saved state.
    """
    if command != "save playlists":
        json_path = command.removeprefix("save playlists ")
        commands.save_playlists_json(current_playlist_list, json_path)
    else:
        commands.save_playlists_json(current_playlist_list)

    saved_playlist_list[:] = copy.deepcopy(current_playlist_list)

    print(f"Number of playlists saved: {len(saved_playlist_list)}")


def create_playlist_command(command: str, playlist_list: list[Playlist]) -> None:
    """Command to create a new playlist and add it to the playlist list.

    Args:
        command (str): Command entered by the user, containing the name of the playlist to create.
        playlist_list (list[Playlist]): Playlist list to add the new playlist to.
    """
    playlist_name = command.removeprefix("create playlist ")
    playlist_list.append(Playlist(playlist_name))


def remove_playlist_command(command: str, playlist_list: list[Playlist]) -> None:
    """Command to remove a playlist from the playlist list.

    Args:
        command (str): Command entered by the user, containing the name of the playlist to remove.
        playlist_list (list[Playlist]): Playlist list to remove the playlist from.
    """
    playlist_name = command.removeprefix("remove playlist ")
    playlist_to_remove = find_playlist_to_add(playlist_name, playlist_list)
    if playlist_to_remove:
        playlist_list.remove(playlist_to_remove)


def generate_playlist_from_template_command(
    command: str,
    tag_list: list[Tag],
    template_list: list[Template],
    playlist_list: list[Playlist],
) -> None:
    """Command to generate a playlist from a template.

    Converts from a template, containing positions with items and probabilities, to a playlist.
    Keeps track of which tracks have been selected from each tag to prevent duplicates until all tracks have been chosen.

    Args:
        command (str): Command entered by the user, containing the name of the playlist to generate.
        tag_list (list[Tag]): Tag list, used to track which tracks have been selected from each tag.
        template_list (list[Template]): Template list, used to generate the playlist.
        playlist_list (list[Playlist]): Playlist list to add the generated playlist to.
    """
    playlist_name = command.removeprefix("generate playlist ")

    if len(template_list) > 0:
        print("Generate from which template?")
        for idx, template in enumerate(template_list):
            print(f"{idx + 1}: {template.name}")

        # Safely get the template index
        while True:
            try:
                chosen_index = (
                    int(input("Enter the number corresponding to the template: ")) - 1
                )
                if 0 <= chosen_index < len(template_list):
                    template_to_generate_from = template_list[chosen_index]
                    break
                else:
                    print(
                        "Invalid index. Please enter a valid index corresponding to the template."
                    )
            except ValueError:
                print("Please enter a valid number for the template index.")

        playlist_tracks = []
        tag_selection_sets = {
            tag.name: set() for tag in tag_list
        }  # Tracks the selected tracks per tag

        for position_items in template_to_generate_from.contents:
            selected_item = None
            probability_sum = sum(item["probability"] for item in position_items)

            if probability_sum > 0:
                random_value = random.uniform(0, probability_sum)
                cumulative_probability = 0.0
                tries = 0
                max_tries = 100  # Prevents an infinite loop if something goes wrong

                while tries < max_tries:
                    tries += 1
                    for item in position_items:
                        cumulative_probability += item["probability"]
                        if random_value <= cumulative_probability:
                            selected_item = item["item"]
                            break

                    # Prevent duplicates if the item is already added
                    if (
                        isinstance(selected_item, Track)
                        and selected_item not in playlist_tracks
                    ):
                        playlist_tracks.append(selected_item)
                        print(
                            f"Added track: {selected_item.name} by {selected_item.artist} to the playlist."
                        )
                        break

                    if isinstance(selected_item, Tag):
                        # Avoid selecting the same track from a tag
                        available_tracks = [
                            track
                            for track in selected_item.tracks
                            if track not in tag_selection_sets[selected_item.name]
                        ]

                        if available_tracks:
                            selected_track = random.choice(available_tracks)
                            playlist_tracks.append(selected_track)
                            tag_selection_sets[selected_item.name].add(selected_track)
                            print(
                                f"Added track: {selected_track.name} from tag {selected_item.name} to the playlist."
                            )
                            break
                        # Reset chosen tracks and retry
                        print(
                            f"All tracks from tag {selected_item.name} have been chosen. Resetting and continuing."
                        )
                        tag_selection_sets[selected_item.name].clear()

                else:
                    print("Max tries reached. No item was selected from position.")

        print(
            f"Generated playlist '{playlist_name}' with {len(playlist_tracks)} tracks."
        )
        playlist_list.append(Playlist(playlist_name, tracks=playlist_tracks))

    else:
        print("No templates available to generate from.")


def upload_playlist_command(command: str, playlist_list: list[Playlist]) -> None:
    """Command to upload a playlist to Spotify.

    Args:
        command (str): Command entered by the user, containing the name of the playlist to upload.
        playlist_list (list[Playlist]): Playlist list containing the playlist to upload the playlist from.
    """
    playlist_name = command.removeprefix("upload playlist ")
    playlist = find_playlist_to_add(playlist_name, playlist_list)
    commands.upload_playlist_to_spotify(playlist)


# HELPER FUNCTIONS


def find_track_to_add(track_name: str, track_list: list[Track]) -> Track:
    """Finds a track in the track list based on the track name.

    Args:
        track_name (str): The name of the track to search for.
        track_list (list[Track]): The list of tracks to search for the track in.

    Returns:
        Track: The track found in the track list, or None if no track was found.
    """
    num_of_tracks = commands.find_num_of_items_with_attribute(
        track_list, "name", track_name
    )

    if num_of_tracks == 0:
        return None
    if num_of_tracks == 1:
        return commands.find_items_from_attribute(track_list, "name", track_name)[0]
    possible_tracks = commands.find_items_from_attribute(track_list, "name", track_name)
    print("Multiple tracks found with this name:")
    for i, track in enumerate(possible_tracks, 1):
        print(f"{i}: {track.name} by {track.artist} (ID: {track.track_id})")

    while True:
        try:
            chosen_index = (
                int(input("Which index corresponds to the correct track? ")) - 1
            )
            if 0 <= chosen_index < len(possible_tracks):
                return possible_tracks[chosen_index]
            else:
                print("Invalid chosen index. Please select a valid index.")
        except ValueError:
            print("Please enter a valid number.")


def find_tag_to_add(tag_name: str, tag_list: list[Tag]) -> Tag:
    """Finds a tag in the tag list based on the tag name.

    Args:
        tag_name (str): The name of the tag to search for.
        tag_list (list[Tag]): The list of tags to search for the tag in.

    Returns:
        Tag: The tag found in the tag list, or None if no tag was found.
    """
    num_of_tags = commands.find_num_of_items_with_attribute(tag_list, "name", tag_name)

    if num_of_tags == 0:
        print(f"No tag with the name '{tag_name}' found.")
        return None
    if num_of_tags == 1:
        return commands.find_items_from_attribute(tag_list, "name", tag_name)[0]
    else:
        possible_tags = commands.find_items_from_attribute(tag_list, "name", tag_name)
        print("Multiple tags found with this name:")
        for i, tag in enumerate(possible_tags, 1):
            print(f"{i}: {tag.name} (ID: {tag.id})")

        while True:
            try:
                chosen_index = (
                    int(input("Which index corresponds to the correct tag? ")) - 1
                )
                if 0 <= chosen_index < len(possible_tags):
                    return possible_tags[chosen_index]
                else:
                    print("Invalid chosen index. Please select a valid number.")
            except ValueError:
                print("Invalid input. Please enter a number.")


def find_template_to_add(template_name: str, template_list: list[Template]) -> Template:
    """Finds a template in the template list based on the template name.

    Args:
        template_name (str): The name of the template to search for.
        template_list (list[Template]): The list of templates to search for the template in.

    Returns:
        Template: The template found in the template list, or None if no template was found.
    """
    num_of_templates = commands.find_num_of_items_with_attribute(
        template_list, "name", template_name
    )

    if num_of_templates == 0:
        print(f"No template with the name '{template_name}' found.")
        return None
    if num_of_templates == 1:
        return commands.find_items_from_attribute(template_list, "name", template_name)[
            0
        ]
    else:
        possible_templates = commands.find_items_from_attribute(
            template_list, "name", template_name
        )
        print("Multiple templates found with this name:")
        for i, template in enumerate(possible_templates, 1):
            print(f"{i}: {template.name} (ID: {template.id})")

        while True:
            try:
                chosen_index = (
                    int(input("Which index corresponds to the correct template? ")) - 1
                )
                if 0 <= chosen_index < len(possible_templates):
                    return possible_templates[chosen_index]
                print("Invalid chosen index. Please select a valid number.")
            except ValueError:
                print("Invalid input. Please enter a number.")


def find_playlist_to_add(playlist_name: str, playlist_list: list[Playlist]) -> Playlist:
    """Finds a playlist in the playlist list based on the playlist name.

    Args:
        playlist_name (str): The name of the playlist to search for.
        playlist_list (list[Playlist]): The list of playlists to search for the playlist in.

    Returns:
        Playlist: The playlist found in the playlist list, or None if no playlist was found.
    """
    num_of_playlists = commands.find_num_of_items_with_attribute(
        playlist_list, "name", playlist_name
    )

    if num_of_playlists == 0:
        print(f"No playlist with the name '{playlist_name}' found.")
        return None
    if num_of_playlists == 1:
        return commands.find_items_from_attribute(playlist_list, "name", playlist_name)[
            0
        ]
    else:
        possible_playlists = commands.find_items_from_attribute(
            playlist_list, "name", playlist_name
        )
        print("Multiple playlists found with this name:")
        for i, playlist in enumerate(possible_playlists, 1):
            print(f"{i + 1}: {playlist.name} (ID: {playlist.id})")

        while True:
            try:
                chosen_index = (
                    int(input("Which index corresponds to the correct playlist? ")) - 1
                )
                if 0 <= chosen_index < len(possible_playlists):
                    return possible_playlists[chosen_index]
                else:
                    print("Invalid chosen index. Please select a valid number.")
            except ValueError:
                print("Invalid input. Please enter a number.")


def adjust_probabilities(existing_items: list[dict], new_item: dict) -> None:
    """Adjusts probabilities of existing items at the same index in a template to fit a new item.

    Args:
        existing_items (list[dict]): List of items at the same index in the template.
        new_item (dict): New item to add to the template.
    """
    new_probability = new_item["probability"]
    total_existing_probability = sum(item["probability"] for item in existing_items)
    scaling_factor = (
        (1.0 - new_probability) / total_existing_probability
        if total_existing_probability > 0
        else 0
    )

    for item in existing_items:
        item["probability"] *= scaling_factor

    existing_items.append(new_item)
