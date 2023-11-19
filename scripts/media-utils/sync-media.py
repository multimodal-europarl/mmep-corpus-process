#!/usr/bin/env python3
"""
Sync media from remote server or local disk to the mmep-corpus.

This program uses rsync to move `.mp4` files and ffmpeg to extract audio tract from the original VODUnit `.mp4`:
    - make sure rsync and ffmpeg is installed and on the system $PATH.
"""
from datetime import datetime
import argparse, json, os, shutil, subprocess, sys




here = os.path.dirname(__file__)
now = datetime.now().strftime("%Y%m%d-%H%M%S")
config_file_path = f"{here}/_sync-media.config"
media_path_base = "mmep-corpus/audio-video/"
transcription_path_base = "mmep-corpus/transcribed-audio/"




def read_config():
    with open(config_file_path, 'r') as inf:
        return json.load(inf)




def write_config(config):
    with open(config_file_path, 'w+') as outf:
        json.dump(config, outf, ensure_ascii=False, indent=4)




def update_config(args):
    if os.path.exists(config_file_path):
        D = read_config()
        D["default_media_location"] = args.src_loc
    else:
        D = {"default_media_location": args.src_loc, "sessions": {}}
    write_config(D)




def get_month_dir(f):
    month = f.split('_')[1][:6]
    directory = f[:-4]
    return month, directory




def sync_media(args):
    config = read_config()
    if args.src_loc:
        loc = args.src_loc
    else:
        loc = config['default_media_location']
    if not os.path.exists(f"{media_path_base}tmp"):
        os.mkdir(f"{media_path_base}tmp")
    rsync = ["rsync", "-vrut", f"--files-from={args.infile}", loc, f"{media_path_base}tmp"]
    subprocess.call(rsync)
    session_files = []
    for f in os.listdir(f"{media_path_base}tmp"):
        month, directory = get_month_dir(f)
        if not os.path.exists(f"{media_path_base}{month}/{directory}"):
            os.mkdir(f"{media_path_base}{month}/{directory}")
        if os.path.exists(f"{media_path_base}{month}/{directory}/{f}"):
            os.remove(f"{media_path_base}tmp/{f}")
        else:
            shutil.move(f"{media_path_base}tmp/{f}", f"{media_path_base}{month}/{directory}/{f}")
        # I couldn't figure out how to do the next line with ffmpeg-python
        subprocess.call([
            f"{here}/unpack-audio.sh", f"{media_path_base}{month}/{directory}", f[:-4]
        ]) # more generally usable if not calling a shell script
        media_files = os.listdir(f"{media_path_base}{month}/{directory}")
        for media_file in media_files:
            session_files.append(f"{media_path_base}{month}/{directory}/{media_file}")
    config["sessions"][args.session_name] = session_files
    write_config(config)




def unsync_media(args):
    config = read_config()
    if args.session_name in config["sessions"]:
        for media_file in config["sessions"][args.session_name]:
            dirname = os.path.dirname(media_file)
            if os.path.exists(dirname):
                shutil.rmtree(dirname)
        del config["sessions"][args.session_name]
        write_config(config)
    else:
        print(f"Session --{args.session_name}-- doesn't exist.")




def list_sessions(args):
    config = read_config()
    if args.session_name:
        if args.session_name in config["sessions"]:
            print(args.session_name)
            [print(f"    {_}") for _ in config["sessions"][args.session_name]]
        else:
            print(f"Session --{args.session_name}-- doesn't exist.")
    else:
        for k, v in config["sessions"].items():
            print(k)
            if args.verbose_list:
                [print(f"    {_}") for _ in v]




def main(args):
    print(args.command, args)
    if args.command == "config":
        update_config(args)
    elif args.command == "sync":
        sync_media(args)
    elif args.command == "unsync":
        unsync_media(args)
    elif args.command == "list":
        list_sessions(args)




if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = __doc__)
    subparsers = parser.add_subparsers(help='Three sub-programs, select one.', dest="command")

    # CONFIG
    config = subparsers.add_parser("config", help="Set default configuration arguments for this script")
    config.add_argument("-s", "--src-loc",
                        required=True, type=str,
                        help="Default source location of media. If location is remote, give the whole user+path as an arg, e.g. `user@remote.host:/path/to/media/ (note the trailing slash). If your remote uses a non standard port, set this in the ssh config and use the hostname set there in this argument"
                        )

    # SYNC
    sync = subparsers.add_parser("sync", help="Get media from the src location and expand audio tracks,")
    sync.add_argument("-i", "--infile",
                      required=True, type=str,
                      help="File containing a list of `.mp4` files to sync -- one file per line, only the file name, no path info."
                    )
    sync.add_argument("-n", "--session-name",
                        default=f"{now}_sesison", type=str,
                        help="Give your sync session a name so it can be removed later. N.b. files in multiple session will be deleted on unsync of any of those sessions."
                        )
    sync.add_argument("-s", "--src-loc", type=str,
                      help="One-off source location of media. If location is remote, give the whole user+path as an arg, e.g. `user@remote.host:/path/to/media"
                    )

    # UNSYNC
    unsync = subparsers.add_parser("unsync", help="Remove media, a named sync.")
    unsync.add_argument("-n", "--session-name", type=str,
                        help="Remove media files associated with session name."
                        )

    # LIST
    sessions = subparsers.add_parser("list", help="List sessions and files.")
    sessions.add_argument("-l", "--list-sessions", action="store_true", help="List all named sessions.")
    sessions.add_argument("-v", "--verbose-list", action="store_true", help="List all sessoins and associated media files")
    sessions.add_argument("-n", "--session-name", type=str,
                        help="List associated media files of a named session."
                        )

    args = parser.parse_args()
    if args.command != "config":
        if not os.path.exists(config_file_path):
            print(f"Cannot find config file at {config_file_path}. Did you run `config`?")
            sys.exit()
        else:
            main(args)
    else:
        main(args)
