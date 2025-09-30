__author__ = "Nadav"

import os, sys, re
from io import StringIO
from subprocess import *
from datetime import datetime

internal_commands = ["cd", "exit", "help", "time", "set", "color", "echo", "cls"]
MY_PATH = [os.getcwd(), "C:\\pythonProject2", "D:\\Shell"]
ECHO_ON = True
DEBUG = False


class Command:
    """ Command Class """

    def __init__(self, st_prompt):
        self.og_prompt = st_prompt.strip()

        st_prompt = self.og_prompt.split()
        self.command = st_prompt[0]
        self.stdout = PIPE
        self.stdin = PIPE
        self.has_redirect_stdin = False
        self.has_redirect_stdout = False

        if len(st_prompt) > 1:
            self.handle_redirect()
        else:
            self.parameters = []

    def __repr__(self):
        """Return string representation of command object."""

        return f"COMMAND [{self.command}, {self.parameters}, {self.stdin}, {self.stdout}]"

    def handle_redirect(self):
        """Parse and handle input/output redirection operators (< and >)."""

        idx_to_not_join = []
        split_lst = Command.parse_redirects(self.og_prompt)
        try:
            for i, item in enumerate(split_lst):
                if item == ">":
                    self.stdout = split_lst[i + 1]
                    self.has_redirect_stdout = True
                    idx_to_not_join.append(i)
                    idx_to_not_join.append(i + 1)

                if item == "<":
                    self.stdin = split_lst[i + 1]
                    self.has_redirect_stdin = True
                    idx_to_not_join.append(i)
                    idx_to_not_join.append(i + 1)

            self.parameters = [item for i, item in enumerate(split_lst) if i not in idx_to_not_join]
            self.parameters = (" ".join(self.parameters)).split()
            self.parameters = [item for item in self.parameters if item != self.command]

        except Exception as e:
            raise Exception(f"The syntax of the command is incorrect. {e}")

    @staticmethod
    def parse_redirects(command):
        """ Split string command by < or > """
        parts = re.split(r'([<>])', command)
        lst = [p.strip() for p in parts]
        if ">>" in "".join(lst) or "<<" in "".join(lst) or '' in lst:
            raise Exception("The syntax of the command is incorrect.")
        return lst

    def open_redirects(self):
        """Open files for input/output redirection."""

        if self.has_redirect_stdin:
            self.stdin = open(self.stdin, "r")

        if self.has_redirect_stdout:
            self.stdout = open(self.stdout, "w")

    def close_redirects(self):
        """Close files used for input/output redirection."""

        if self.has_redirect_stdin:
            self.stdin.close()

        if self.has_redirect_stdout:
            self.stdout.close()


class Internal(Command):
    """ Class For Internals Commands"""

    def __init__(self, st):
        super().__init__(st)
        self.command = self.command.lower()

        self.internal_dict = {"cd": self.handle_cd, "exit": self.perform_exit,
                              "set": self.perform_set, "color": self.handle_color,
                              "time": self.perform_time, "cls": self.perform_cls,
                              "echo": self.perform_echo, "help": self.perform_help}

    @staticmethod
    def is_internal(st):
        """Check if command string is an internal shell command."""

        lst = st.split()
        return lst[0].lower() in internal_commands

    def run(self, start=True):
        """Execute internal command with output capture and redirection handling."""

        self.open_redirects()

        input_data = ""
        if self.stdin and self.stdin != PIPE:
            if hasattr(self.stdin, 'read'):
                input_data = self.stdin.read()

        # redirect
        if self.has_redirect_stdout and self.stdout != PIPE:
            self.handle_internal_redirect(input_data)
            return

        if self.stdout != PIPE or not start:
            output_text = self.capture_output_and_run()
            if start:
                print(output_text)
            self.close_redirects()
            return

        self.internal_dict[self.command]()
        self.p = InternalPipe("")
        self.close_redirects()

    def capture_output_and_run(self):
        """Capture stdout from internal command execution for piping."""

        old_stdout = sys.stdout
        captured_output = StringIO()
        sys.stdout = captured_output

        try:
            self.internal_dict[self.command]()
        except Exception as e:
            print_error_type(str(e))
        finally:
            sys.stdout = old_stdout

        output_text = captured_output.getvalue()
        self.p = InternalPipe(output_text)
        return output_text

    def handle_internal_redirect(self, input_data):
        """Handle file output redirection for internal commands."""

        old_stdout = sys.stdout
        sys.stdout = self.stdout
        try:
            if input_data and self.command == 'echo':  # can use stdin
                self.internal_dict[self.command](input_data)
            else:
                self.internal_dict[self.command]()
        finally:
            sys.stdout = old_stdout

        self.p = InternalPipe("")
        self.close_redirects()
        return

    def handle_cd(self):
        """Change or display current working directory."""

        if not self.parameters:
            print(os.getcwd())
            return

        new_path = os.getcwd() + "\\" + "".join(self.parameters)
        try:
            os.chdir(new_path)
            return
        except:
            try:
                os.chdir("".join(self.parameters))
            except:
                raise Exception("The system cannot find the path specified.\n")

    def handle_color(self):
        """Set console foreground and background colors."""
        if not self.parameters:
            os.system("color 7") # back to og
        try:
            os.system(f"color {''.join(self.parameters)}")
        except:  # i dont think the except is needed!
            print("Colors Available From 0 - 7. The Number Must Be an Integer!\n")

    def perform_exit(self):
        """Exit the shell program."""

        sys.exit(0)

    def perform_set(self):
        """Display or set environment variables."""

        if not self.parameters:
            env_dict = os.environ.copy()
            for key, val in env_dict.items():
                print(f'{key}={val}')
            print()
            return

        if len(self.parameters) > 2:
            raise Exception("set command can have 1 parameter maximum.")
        self.check_param()

    def check_param(self):
        """Parse and validate SET command parameters."""

        param = self.parameters[0]
        if '=' not in param:
            Internal.handle_get_set_param(param)
            return

        lst = param.split('=', maxsplit=1)
        if len(lst) > 2:
            raise Exception("The syntax of the command is incorrect.")

        key, value = lst
        key = key.strip()
        if not key:
            raise Exception("Environment variable name missing.")

        value = Internal.expand_vars(value.strip())
        os.environ[key] = value
        print(f"{key}={value}")

    @staticmethod
    def handle_get_set_param(param):
        """Get and display environment variables matching pattern."""

        var_name = param.upper()
        try:
            env_dict = os.environ.copy()
            for key, val in env_dict.items():
                if key.upper().startswith(var_name):
                    print(f'{key}={val}')
        except KeyError:
            raise Exception(f'Environment variable {var_name} not defined.')
        return

    @staticmethod
    def expand_vars(value):
        """Get %VAR% value."""

        pattern = r"%([A-Za-z0-9_]+)%"  # match %VAR%
        matches = re.findall(pattern, value)

        for var in matches:
            env_val = os.environ.get(var.upper(), "")
            value = value.replace(f"%{var}%", env_val)

        return value

    def perform_time(self):
        """Display or set system time."""

        if not self.parameters:
            try:
                now = datetime.now()
                print(f'Current time is: {now.strftime("%H:%M:%S")}.{now.microsecond // 10000:02}', flush=True)
                new_time = input("Enter the new time: ")
                if new_time == '':
                    return
                os.system(f"time {new_time}")

            except Exception as e:
                print_error_type(str(e))
            return
        if len(self.parameters) != 1:
            raise Exception("time command shall be used with 0 or 1 parameters only.\n")
        os.system(f"time {self.parameters[0]}")

    def perform_echo(self, input_data=""):
        """Display messages or control command echoing."""

        global ECHO_ON

        # echo the input_data
        if input_data and not self.parameters:
            expanded = Internal.expand_vars(input_data.strip())
            print(expanded)
            return

        if not self.parameters:
            print(f"ECHO is {'on' if ECHO_ON else 'off'}.")
            return

        arg = " ".join(self.parameters).strip()

        if arg.lower() == "on":
            ECHO_ON = True
            return

        if arg.lower() == "off":
            ECHO_ON = False
            return

        if arg in (".", ":", "[", ",", ";", "/"):
            print()
            return

        expanded = Internal.expand_vars(arg)
        print(expanded)

    def perform_cls(self):
        """Clear the console screen."""

        if self.parameters:
            raise Exception("cls command takes no parameters.")

        os.system('cls')

    def perform_help(self):
        """Display help information for shell commands."""

        if not self.parameters:
            # Show general help with all internal commands
            print("For more information on a specific command, type HELP command-name")
            print("CD             Displays the name of or changes the current directory.")
            print("CLS            Clears the screen.")
            print("COLOR          Sets the default console foreground and background colors.")
            print("ECHO           Displays messages, or turns command echoing on or off.")
            print("EXIT           Quits the Shell program.")
            print("HELP           Provides Help information for Windows commands.")
            print("SET            Displays, sets, or removes Windows environment variables.")
            print("TIME           Displays or sets the system time.")
            return

        # Get the first parameter only (help command behavior)
        command = self.parameters[0].lower()

        if command == "cd":
            print("Displays the name of or changes the current directory.")
            print("")
            print("CD [drive:][path]")
            print("CD [..]")
            print("")
            print("  ..   Specifies that you want to change to the parent directory.")
            print("")
            print("Type CD drive: to display the current directory in the specified drive.")
            print("Type CD without parameters to display the current drive and directory.")

        elif command == "cls":
            print("Clears the screen.")
            print("")
            print("CLS")

        elif command == "color":
            print("Sets the default console foreground and background colors.")
            print("")
            print("COLOR [attr]")
            print("")
            print("  attr        Specifies color attribute of console output")
            print("")
            print("Color attributes are specified by TWO hex digits -- the first")
            print("corresponds to the background; the second the foreground.  Each digit")
            print("can be any of the following values:")
            print("")
            print("    0 = Black       8 = Gray")
            print("    1 = Blue        9 = Light Blue")
            print("    2 = Green       A = Light Green")
            print("    3 = Aqua        B = Light Aqua")
            print("    4 = Red         C = Light Red")
            print("    5 = Purple      D = Light Purple")
            print("    6 = Yellow      E = Light Yellow")
            print("    7 = White       F = Bright White")
            print("")
            print("If no argument is given, this command restores the color to what it was")
            print("when CMD.EXE started.")

        elif command == "echo":
            print("Displays messages, or turns command echoing on or off.")
            print("")
            print("  ECHO [ON | OFF]")
            print("  ECHO [message]")
            print("")
            print("Type ECHO without parameters to display the current echo setting.")
            print("ECHO ON means presenting the Current Working Directory prompt. ECHO off hides it.")

        elif command == "exit":
            print("Quits the Shell program.")


        elif command == "help":
            print("Provides Help information for Windows commands.")
            print("")
            print("HELP [command]")
            print("")
            print("    command - displays help information on that command.")

        elif command == "set":
            print("Displays or sets Windows environment variables.")
            print("")
            print("SET [variable=[string]]")
            print("")
            print("  variable  Specifies the environment-variable name.")
            print("  string    Specifies a series of characters to assign to the variable.")
            print("  The use of %environment-variable% will get the value of the variable.")
            print("")
            print("Type SET without parameters to display the current environment variables.")

        elif command == "time":
            print("Displays or sets the system time.")
            print("")
            print("TIME [time]")
            print("")
            print("Type TIME with no parameters to display the current time setting and a prompt")
            print("for a new one.  Press ENTER to keep the same time.")
            print("")
            print("For changing the time of the PC, Run the shell As Administrator.")

        else:
            print(f"This command is not supported by the help utility.")
            return


class InternalPipe:
    """custom Popen object for Internals"""

    def __init__(self, output_text):
        self.returncode = 0

        if output_text:
            read, write = os.pipe()
            os.write(write, output_text.encode('utf-8'))
            os.close(write)

            self.stdout = os.fdopen(read, 'rb')  # as file object
        else:
            self.stdout = None

    def wait(self):
        return 0


class Script(Command):
    def __init__(self, st):
        super().__init__(st)
        self.p = None

    @staticmethod
    def is_script(st):
        """Check if command is a Python script."""

        lst = st.split()
        return lst[0].lower().endswith(".py")

    def run(self, start=True):
        """Execute Python script with parameter passing and output handling."""

        try:
            self.open_redirects()

            path = Script.search_py_file_path(self.command)

            self.p = Popen(args=["python", path] + self.parameters,
                           stdin=self.stdin, stdout=self.stdout, stderr=self.stdout,text=True)
            if start:
                output, error = self.p.communicate()  #timeout=20

                if error is not None or error:
                    print(make_output_text_only(error))
                if output is not None or output:
                    print(make_output_text_only(output))

                if self.p.returncode != 0:
                    print_error_type(error)

            self.close_redirects()

        except Exception as e:
            if DEBUG:
                print(f"Unable to run {self.command} with {self.parameters}. {e}", flush=True)

    @staticmethod
    def search_py_file_path(command):
        """Search for Python script file in predefined paths."""

        for path in MY_PATH:
            try:
                if command in os.listdir(path):
                    return f"{path}\\{command}"
            except:
                continue

        return command  # let subprocess find it


class External(Command):
    def __init__(self, st):
        super().__init__(st)
        self.p = None

    def run(self, start=True):
        """Execute external commands"""

        try:
            self.open_redirects()

            cmd_line = " ".join([self.command] + self.parameters)

            self.p = Popen(cmd_line, stdin=self.stdin, stdout=self.stdout,
                           shell=True, stderr=self.stdout, text=True)
            if start:
                output, error = self.p.communicate()  # timeout=20

                if error is not None or error:
                    print(make_output_text_only(error))
                if output is not None or output:
                    print(make_output_text_only(output))

                if self.p.returncode != 0:
                    print_error_type(error)

            self.close_redirects()

        except Exception as e:
            if DEBUG:
                print(f"Unable to run {self.command} with {self.parameters}. {e}", flush=True)


def create_command(prompt):
    """Create appropriate command object based on prompt type."""

    if prompt.strip("") == "":
        return None
    if Internal.is_internal(prompt):
        return Internal(prompt)
    if Script.is_script(prompt):
        return Script(prompt)
    return External(prompt)


def split_command(prompt):
    """Parse command by pipe."""

    if prompt.strip("") == "":
        return None, False
    prompt = prompt.split('|')
    if len(prompt) == 1:
        return create_command(''.join(prompt)), False

    lst_of_cmd = [create_command(item) for item in prompt]
    if None in lst_of_cmd:
        raise Exception("The syntax of the command is incorrect.")
    return lst_of_cmd, True


def make_output_text_only(output):
    """Convert binary output to readable text format."""
    if type(output) is str:
        return output

    to_return = ""
    if type(output) is bytes:
        for byte in output:
            if 32 <= byte <= 126 or byte in [ord(item) for item in ['\n', '\t', '\r']]:
                to_return += chr(byte)
            else:
                to_return += '.'
    return to_return


def run_pipeline(list_of_commands):
    """Execute command pipeline with proper input/output chaining."""

    # cmd1 | cmd2 | cmd3
    for i, command in enumerate(list_of_commands):
        if i == 0:
            command.stdin = None
            command.stdout = PIPE
        elif i == len(list_of_commands) - 1:
            command.stdin = list_of_commands[i - 1].p.stdout
            if not command.has_redirect_stdout:
                command.stdout = None
        else:
            command.stdin = list_of_commands[i - 1].p.stdout
            command.stdout = PIPE

        command.run(start=(i == len(list_of_commands) - 1))

    # close all except the last
    for cmd in list_of_commands[:-1]:
        if cmd.p.stdout:
            cmd.p.stdout.close()

    list_of_commands[-1].p.wait()


def print_error_type(stderr):
    """Check stderr for common error messages."""

    if "No such file or directory" in stderr or "not recognized" in stderr or "cannot find" in stderr:
        raise FileNotFoundError(stderr)
    elif "Permission denied" in stderr:
        raise PermissionError(stderr)
    else:
        raise Exception(stderr)


def get_starting_prompt_st():
    """Generate shell prompt string with user and directory info."""

    if not ECHO_ON:
        return ""

    cwd = os.getcwd()
    username = os.getlogin()
    return f"{username} ~ {os.environ['USERDOMAIN']} ~ {cwd}> "


if __name__ == "__main__":
    while True:
        try:
            starting_prompt = get_starting_prompt_st()

            st = input(starting_prompt)
            obj_command, has_pipe = split_command(st)
            if obj_command is None:
                continue
            if has_pipe:
                run_pipeline(obj_command)
            else:
                obj_command.run()

        except KeyboardInterrupt:
            print("\n CTRL+C has INTERRUPTED the process.\n")
        except FileNotFoundError as e:
            print("The system cannot find the file specified.\n")
            if DEBUG:
                print(f"{e}\n")
        except PermissionError as e:
            print("Permission denied.\n")
            if DEBUG:
                print(f"{e}\n")
        except ValueError as e:
            print("Error with value(s).\n")
            if DEBUG:
                print(f"{e}\n")
        except Exception as e:
            print(f"General Error. {e}\n")
