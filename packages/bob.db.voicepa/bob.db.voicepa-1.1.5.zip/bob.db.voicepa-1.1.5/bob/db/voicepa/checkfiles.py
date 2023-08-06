#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Pavel Korshunov <pavel.korshunov@idiap.ch>
# Thu 6 Oct 21:43:22 2016

"""Checks for installed files.
"""

import os
import sys


# Driver API
# ==========

def checkfiles(args):
    """Checks existence files based on your criteria"""

    from .query import Database
    db = Database()

    r = db.objects(
        protocol=args.protocol,
        attack_data=args.attackdata,
        groups=args.group,
        cls=args.cls,
        recording_devices=args.device,
        sessions=args.sessions,
        attack_devices=args.attackdevice,
        clients=args.client,
        asv_devices=args.asv_device,
        environments=args.environment,
    )

    # go through all files, check if they are available on the filesystem
    good = []
    bad = []
    for f in r:
        if os.path.exists(f.make_path(args.directory, args.extension)):
            good.append(f)
        else:
            bad.append(f)

    # report
    output = sys.stdout
    if args.selftest:
        from bob.db.base.utils import null
        output = null()

    if bad:
        for f in bad:
            output.write('Cannot find file "%s"\n' % (f.make_path(args.directory, args.extension),))
        output.write('%d files (out of %d) were not found in "%s"\n' % (len(bad), len(r), args.directory))
    else:
        output.write('All specified files were successfully found in "%s"\n' % args.directory)
    return 0


def add_command(subparsers):
    """Add specific subcommands that the action "checkfiles" can use"""

    from argparse import SUPPRESS

    parser = subparsers.add_parser('checkfiles', help=checkfiles.__doc__)

    from .query import Database

    db = Database()

    if not db.is_valid():
        protocols = ('waiting', 'for', 'database', 'creation')
        clients = tuple()
    else:
        protocols = [k.name for k in db.protocols()]
        clients = [k.id for k in db.clients()]

    parser.add_argument('-d', '--directory', dest="directory", default='',
                        help="if given, this path will be prepended to every entry checked (defaults to '%(default)s')")
    parser.add_argument('-e', '--extension', dest="extension", default='.wav',
                        help="if given, this extension will be appended to every entry checked (defaults to '%(default)s')")
    parser.add_argument('-c', '--class', dest="cls", default=('real', 'attack'),
                        help="if given, limits the check to a particular subset of the data that corresponds to "
                             "the given class (defaults to '%(default)s')",
                        choices=('real', 'attack', 'enroll', 'probe'))
    parser.add_argument('-g', '--group', dest="group", default=db.groups(),
                        help="if given, this value will limit the check to those files belonging to a particular "
                             "protocol group, e.g., train, dev, and eval. (defaults to '%(default)s')",
                        choices=db.groups())
    parser.add_argument('-s', '--attackdata', dest="attackdata", default=None,
                        help="if given, this value will limit the check to those files using this type of attack "
                             "support, e.g., replay_attack or voice_conversion. (defaults to '%(default)s')",
                        choices=db.attack_datas())
    parser.add_argument('-x', '--protocol', dest="protocol", default='grandtest',
                        help="if given, this value will limit the check to those files for a given protocol. "
                             "(defaults to '%(default)s')",
                        choices=protocols)
    parser.add_argument('-v', '--device', dest="device", default=None,
                        help="if given, this value will limit the check to the samples that were originally recorded "
                             "with the specified device. (defaults to '%(default)s')",
                        choices=db.devices())
    parser.add_argument('-A', '--asv-device', dest="asv_device", default=None,
                        help="if given, this value will limit the check to the attacks intended for the specified "
                             "ASV device. (defaults to '%(default)s')",
                        choices=db.asv_devices())
    parser.add_argument('-E', '--environment', dest="environment", default=None,
                        help="if given, this value will limit the check to the specified environment where attacks "
                             "were recorded (defaults to '%(default)s')",
                        choices=db.environments())
    parser.add_argument('-n', '--session', dest="sessions", default=None,
                        help="if given, this value will limit the check to those samples recorded during specific "
                             "session. (defaults to '%(default)s')",
                        choices=db.sessions())
    parser.add_argument('-k', '--attackdevice', dest="attackdevice", default=None,
                        help="if given, this value will limit the check to the attacks by the specified devices. "
                             "(defaults to '%(default)s')",
                        choices=db.attack_devices())
    parser.add_argument('-C', '--client', dest="client", default=None, type=int,
                        help="if given, limits the dump to a particular client (defaults to '%(default)s')",
                        choices=clients)
    parser.add_argument('--self-test', dest="selftest", default=False,
                        action='store_true', help=SUPPRESS)

    parser.set_defaults(func=checkfiles)  # action
