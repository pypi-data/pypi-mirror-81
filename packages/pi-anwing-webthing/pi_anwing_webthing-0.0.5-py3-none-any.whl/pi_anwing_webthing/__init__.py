import os
import logging
import argparse
from pi_anwing_webthing.anwing_thing import run_server
from pi_anwing_webthing.unit import register, deregister, printlog

PACKAGENAME = 'pi_anwing_webthing'
ENTRY_POINT = "anwing"
DESCRIPTION = "A web connected patio awnings controller on Raspberry Pi"



def main():
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser.add_argument('--command', metavar='command', required=True, type=str, help='the command. Supported commands are: listen (run the webthing service), register (register and starts the webthing service as a systemd unit, deregister (deregisters the systemd unit), log (prints the log)')
    parser.add_argument('--port', metavar='port', required=True, type=int, help='the port of the webthing serivce')
    parser.add_argument('--filename', metavar='filename', required=True, type=str,  help='the config filename')
    args = parser.parse_args()

    if args.command == 'listen':
        print("running " + PACKAGENAME + " on port " + str(args.port) + " with config " + args.filename)
        run_server(int(args.port), args.filename, DESCRIPTION)
    elif args.command == 'register':
        print("register " + PACKAGENAME + " on port " + str(args.port) + " with config " + args.filename)
        register(PACKAGENAME, ENTRY_POINT, int(args.port), args.filename)
    elif args.command == 'deregister':
        deregister(PACKAGENAME, int(args.port))
    elif args.command == 'log':
        printlog(PACKAGENAME, int(args.port))
    else:
        print("usage " + ENTRY_POINT + " --help")


if __name__ == '__main__':
    log_level = os.environ.get("LOGLEVEL", "INFO")
    logging.basicConfig(format='%(asctime)s %(name)-20s: %(levelname)-8s %(message)s', level=log_level, datefmt='%Y-%m-%d %H:%M:%S')
    main()

