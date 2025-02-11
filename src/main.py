import copy

import cli_commands


def main():
    """Runs the main loop, which takes in user input and executes commands in the command line interface."""
    print("Spotify Toolbox CLI v1.0.1")

    current_track_list = []
    current_tag_list = []
    current_template_list = []
    current_playlist_list = []

    saved_tag_list = []
    saved_template_list = []
    saved_playlist_list = []

    cli_commands.load_tracks_command("load tracks", current_track_list)
    cli_commands.load_tags_command("load tags", current_tag_list)
    cli_commands.load_templates_command("load templates", current_template_list)
    cli_commands.load_playlists_command("load playlists", current_playlist_list)

    saved_tag_list = copy.deepcopy(current_tag_list)
    saved_template_list = copy.deepcopy(current_template_list)
    saved_playlist_list = copy.deepcopy(current_playlist_list)

    while True:
        print()
        command = input("Enter Command: ").strip()

        # GENERAL COMMANDS

        if command in ("exit", "quit", "q"):
            cli_commands.exit_command(
                current_tag_list,
                saved_tag_list,
                current_template_list,
                saved_template_list,
                current_playlist_list,
                saved_playlist_list,
            )
            break

        if command in ("help", "commands"):
            cli_commands.help_command()

        elif command.startswith("backup"):
            cli_commands.backup_command(
                command,
                current_track_list,
                current_tag_list,
                current_template_list,
                current_playlist_list,
            )

        elif command in ("load", "l"):
            cli_commands.load_tracks_command("load tracks", current_track_list)
            cli_commands.load_tags_command("load tags", current_tag_list)
            cli_commands.load_templates_command("load templates", current_template_list)
            cli_commands.load_playlists_command("load playlists", current_playlist_list)

        elif command in ("save", "s"):
            cli_commands.save_tags_command(
                "save tags", current_tag_list, saved_tag_list
            )
            cli_commands.save_templates_command(
                "save templates", current_template_list, saved_template_list
            )
            cli_commands.save_playlists_command(
                "save playlists", current_playlist_list, saved_playlist_list
            )

        # TRACK COMMANDS

        elif command == "fetch tracks":
            cli_commands.fetch_tracks_command()

        elif command.startswith("load tracks"):
            cli_commands.load_tracks_command(command, current_track_list)

        elif command == "display tracks":
            cli_commands.display_tracks_command(current_track_list)

        # TAG COMMANDS

        elif command.startswith("load tags"):
            cli_commands.load_tags_command(command, current_tag_list)

        elif command.startswith("save tags"):
            cli_commands.save_tags_command(command, current_tag_list, saved_tag_list)

        elif command.startswith("create tag "):
            cli_commands.create_tag_command(command, current_tag_list)

        elif command.startswith("remove tag "):
            cli_commands.remove_tag_command(command, current_tag_list)

        elif command == "remove tags":
            cli_commands.remove_tags_command(current_tag_list)

        elif command.startswith("add to tag "):
            cli_commands.add_to_tag_command(
                command, current_track_list, current_tag_list
            )

        elif command.startswith("remove from tag "):
            cli_commands.remove_from_tag_command(command, current_tag_list)

        elif command.startswith("clear tag "):
            cli_commands.clear_tag_command(command, current_tag_list)

        elif command.startswith("display tag "):
            cli_commands.display_tag_command(command, current_tag_list)

        elif command.startswith("display tags"):
            cli_commands.display_tags_command(current_tag_list)

        elif command.startswith("generate tags"):
            cli_commands.generate_tags_command(
                command, current_track_list, current_tag_list
            )

        # TEMPLATE COMMANDS

        elif command.startswith("load templates"):
            cli_commands.load_templates_command(command, current_template_list)

        elif command.startswith("save templates"):
            cli_commands.save_templates_command(
                command, current_template_list, saved_template_list
            )

        elif command.startswith("create template "):
            cli_commands.create_template_command(command, current_template_list)

        elif command.startswith("remove template "):
            cli_commands.remove_template_command(command, current_template_list)

        elif command.startswith("add to template "):
            cli_commands.add_to_template_command(
                command, current_track_list, current_tag_list, current_template_list
            )

        elif command.startswith("remove from template "):
            cli_commands.remove_from_template_command(command, current_template_list)

        elif command.startswith("display template "):
            cli_commands.display_template_command(command, current_template_list)

        elif command.startswith("display templates"):
            cli_commands.display_templates_command(current_template_list)

        # PLAYLIST COMMANDS

        elif command.startswith("load playlists"):
            cli_commands.load_playlists_command(command, current_playlist_list)

        elif command.startswith("save playlists"):
            cli_commands.save_playlists_command(
                command, current_playlist_list, saved_playlist_list
            )

        elif command.startswith("create playlists "):
            cli_commands.create_playlist_command(command, current_playlist_list)

        elif command.startswith("remove playlists "):
            cli_commands.remove_playlist_command(command, current_playlist_list)

        elif command.startswith("generate playlist "):
            cli_commands.generate_playlist_from_template_command(
                command, current_tag_list, current_template_list, current_playlist_list
            )

        elif command.startswith("upload playlist "):
            cli_commands.upload_playlist_command(command, current_playlist_list)

        else:
            print("Unknown Command.")


if __name__ == "__main__":
    main()
