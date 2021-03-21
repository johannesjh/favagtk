import sys

from fava_gtk import Application


def main():
    """
    Starts FavaGtk.
    Note: This method is referenced in setup.cfg as entry point.
    """
    application = Application()
    exit_status = application.run(sys.argv)
    sys.exit(exit_status)


if __name__ == "__main__":
    # Start FavaGtk:
    main()
