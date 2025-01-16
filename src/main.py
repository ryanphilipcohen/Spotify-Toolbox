from Datatypes import *
import CLI_Commands, Commands

def main():
    print("Spotify Toolbox CLI v1.0")

    track_list = []
    tag_list = []
    template_list = []
    playlist_list = []

    while True:
        print()
        command = input("Enter Command: ").strip().lower()

        # GENERAL COMMANDS

        if command == "exit" or command == "quit" or command == "q":
            CLI_Commands.exit_command()
            break

        elif command == "help" or command == "commands":
            CLI_Commands.help_command()

        elif command == "load" or command == "l":
            CLI_Commands.load_tracks_command("load tracks", track_list)
            CLI_Commands.load_tags_command("load tags", tag_list)
            CLI_Commands.load_templates_command("load templates", template_list)
            CLI_Commands.load_playlists_command("load playlists", playlist_list)

        elif command == "save" or command == "s":
            CLI_Commands.save_tags_command("save tags", tag_list)
            CLI_Commands.save_templates_command("save templates", template_list)
            CLI_Commands.save_playlists_command("save playlists", playlist_list)

        # TRACK COMMANDS

        elif command == "fetch tracks":
            CLI_Commands.fetch_tracks_command()

        elif command.startswith("load tracks"):
            CLI_Commands.load_tracks_command(command, track_list)

        elif command == "display tracks" or command == "print tracks":
            CLI_Commands.display_tracks_command(track_list)

        # TAG COMMANDS

        elif command.startswith("load tags"):
            CLI_Commands.load_tags_command(command, tag_list)

        elif command.startswith("save tags"):
            CLI_Commands.save_tags_command(command, tag_list)

        elif command.startswith("create tag "):
            CLI_Commands.create_tag_command(command, tag_list)

        elif command.startswith("remove tag "):
            CLI_Commands.remove_tag_command(command, tag_list) 

        elif command.startswith("add to tag "):
            CLI_Commands.add_to_tag_command(command, track_list, tag_list)

        elif command.startswith("remove from tag "):
            CLI_Commands.remove_from_tag_command(command, tag_list)

        elif command.startswith("display tag "):
            CLI_Commands.display_tag_command(command, tag_list)
        
        elif command.startswith("display tags"):
            CLI_Commands.display_tags_command(tag_list)

        # TEMPLATE COMMANDS

        elif command.startswith("load templates"):
            CLI_Commands.load_templates_command(command, template_list)

        elif command.startswith("save templates"):
            CLI_Commands.save_templates_command(command, template_list)

        elif command.startswith("create template "):
            CLI_Commands.create_template_command(command, template_list)

        elif command.startswith("remove template "):
            CLI_Commands.remove_template_command(command, template_list)

        elif command.startswith("add to template "):
            CLI_Commands.add_to_template_command(command, track_list, tag_list, template_list)

        elif command.startswith("remove from template "):
            CLI_Commands.remove_from_template_command(command, template_list)

        elif command.startswith("display template "):
            CLI_Commands.display_template_command(command, template_list)
        
        elif command.startswith("display templates"):
            CLI_Commands.display_templates_command(template_list)

        # PLAYLIST COMMANDS

        elif command.startswith("load playlists"):
            CLI_Commands.load_playlists_command(command, playlist_list)

        elif command.startswith("save playlists"):
            CLI_Commands.save_playlists_command(command, playlist_list)

        elif command.startswith("create playlists "):
            CLI_Commands.create_playlist_command(command, playlist_list)

        elif command.startswith("remove playlists "):
            CLI_Commands.remove_playlist_command(command, playlist_list)

        elif command.startswith("generate playlist "):
            CLI_Commands.generate_playlist_from_template_command(command, tag_list, template_list, playlist_list)

        elif command.startswith("upload playlist "):
            CLI_Commands.upload_playlist_command(command, playlist_list)

        
        else:
            print("Unknown Command.")

if __name__ == "__main__":
    main()