import argparse
import os
import sys


description = """
Test used disk space on / and fail if below a certain value.
"""


def get_used_disk_space_GiB():
    r = os.statvfs('/')
    return r.f_bavail * r.f_frsize / 1024**3


if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser(description=description)
    arg_parser.add_argument(
        '--min', type=float, default='10.0',
        help='minimum available space in GiB (default: 10.0)'
    )

    args = arg_parser.parse_args()

    used_space = get_used_disk_space_GiB()
    print("Free space: {:.1f} GiB".format(used_space))

    if used_space >= args.min:
        sys.exit(0)
    else:
        print("Error: free disk space is below {:.1f} GiB".format(args.min))
        sys.exit(1)
