"""
Implements a reusable console print facility for simple command-line scripts.

Other implementations can easily wrap Python's standard logger/warning modules,
but this one does not because those are overkill for *simple* STDOUT/STDERR
printing (that must support squelching).

Requires an object on init which has the following properties:
  quiet:  <Boolean> suppresses all output except ConsolePrinter::error() and
          ::critical().
  verbose:  <Boolean> allows output from ConsolePrinter::verbose().
  debug:  <Boolean> allows output from ConsolePrinter::debug().

Copyright 2018, 2019, 2020 William W. Kimball, Jr. MBA MSIS
"""
import sys


class ConsolePrinter:
    """
    Generally-useful console messager.

    Writes INFO, VERBOSE, WARN, and DEBUG messages to STDOUT as well as ERROR
    messages to STDERR with multi-lne formatting.
    """

    def __init__(self, args):
        """
        Instantiate a ConsolePrinter.

        Positional Parameters:
        1. args (object) An object representing log level settings with these
           properties:
            - debug (Boolean) true = write debugging informational messages
            - verbose (Boolean) true = write verbose informational messages
            - quiet (Boolean) true = write only error messages

        Returns:  N/A

        Raises:  N/A
        """
        self.args = args

    def info(self, message):
        """
        Write an informational message to STDOUT unless quiet mode is active.

        Positional Parameters:
        1. message (str) The message to print

        Returns:  N/A

        Raises:  N/A
        """
        if not self.args.quiet:
            print(message)

    def verbose(self, message):
        """
        Write a verbose message to STDOUT.

        Writes only when verbose mode is active unless quiet mode is active.

        Positional Parameters:
        1. message (str) The message to print

        Returns:  N/A

        Raises:  N/A
        """
        if not self.args.quiet and (self.args.verbose or self.args.debug):
            print(message)

    def warning(self, message):
        """
        Write a warning message to STDOUT unless quiet mode is active.

        Positional Parameters:
        1. message (str) The message to print

        Returns:  N/A

        Raises:  N/A
        """
        if not self.args.quiet:
            print("WARNING:  " + str(message).replace("\n", "\nWARNING:  "))

    def error(self, message, exit_code=None):
        """
        Write a recoverable error message to STDERR.

        Optionally terminates the program, exiting with a specific error code.

        Positional Parameters:
        1. message (str) The message to print
        2. exit_code (int) The exit code to terminate the program with;
           default=None

        Returns:  N/A

        Raises:  N/A
        """
        print(
            "ERROR:  " + str(message).replace("\n", "\nERROR:  "),
            file=sys.stderr
        )
        print("Please try --help for more information.")
        sys.stdout.flush()

        # Optionally terminate program execution with a specified exit code
        if exit_code is not None:
            self.debug("Terminating with exit code, {}.".format(exit_code))
            sys.exit(exit_code)

    def critical(self, message, exit_code=1):
        """
        Write a critical, nonrecoverable failure message to STDERR and abend.

        Terminates the program, exiting with a specific error code.

        Positional Parameters:
        1. message (str) The message to print
        2. exit_code (int) The exit code to terminate the program with;
           default=1

        Returns:  N/A

        Raises:  N/A
        """
        print(
            "CRITICAL:  " + str(message).replace("\n", "\nCRITICAL:  "),
            file=sys.stderr
        )
        sys.stdout.flush()

        # Terminate program execution with a specified exit code
        self.debug("Terminating with exit code, {}.".format(exit_code))
        sys.exit(exit_code)

    def debug(self, message):
        """
        Write a debug message to STDOUT unless quiet mode is active.

        Dumps all key-value pairs of a dictionary or all elements of a list,
        when the message is either.

        Positional Parameters:
        1. message (str) The message to print

        Returns:  N/A

        Raises:  N/A
        """
        if self.args.debug and not self.args.quiet:
            if isinstance(message, list):
                for i, ele in enumerate(message):
                    attr = ""
                    if hasattr(ele, "anchor") and ele.anchor.value is not None:
                        attr = "; &" + ele.anchor.value
                    eattr = (str(ele) + attr).replace("\n", "\nDEBUG:  ")
                    print("DEBUG:  [{}]={} {}".format(i, eattr, type(ele)))
            elif isinstance(message, dict):
                for key, val in message.items():
                    key_anchor = (
                        key.anchor.value if hasattr(key, "anchor") else None
                    )
                    val_anchor = (
                        val.anchor.value if hasattr(val, "anchor") else None
                    )
                    line_out = "DEBUG:  [" + str(key)
                    if key_anchor:
                        line_out += "; &" + str(key_anchor)
                    line_out += "]=>" + str(val).replace("\n", "\nDEBUG:  ")
                    if val_anchor:
                        line_out += "; &" + str(val_anchor)
                    print(line_out)
            else:
                attr = ""
                if (
                        hasattr(message, "anchor")
                        and message.anchor.value is not None
                ):
                    attr = "; &" + message.anchor.value
                mattr = (str(message) + attr).replace("\n", "\nDEBUG:  ")
                print("DEBUG:  " + str(mattr))
