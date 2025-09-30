# Custom Python Shell (Like CMD)

A feature-rich command-line shell implementation in Python that mimics Windows CMD functionality with support for internal commands, external programs, Python scripts, pipelines, and I/O redirection.

## 🌟 Features

### Core Functionality
- **Internal Commands**: Built-in commands like `cd`, `echo`, `set`, `time`, `color`, `cls`, `help`, and `exit`
- **External Commands**: Execute any system command or program
- **Python Script Execution**: Run `.py` files directly with automatic path resolution
- **Pipeline Support**: Chain commands using the `|` operator
- **I/O Redirection**: Use `<` for input and `>` for output redirection
- **Environment Variables**: Full support for setting and expanding environment variables with `%VAR%` syntax
- **Echo Control**: Toggle command prompt display with `echo on/off`

## 🏗️ Architecture

This project demonstrates clean object-oriented design with inheritance and polymorphism.

### Class Hierarchy

```
Command (Base Class)
├── Internal (Internal shell commands)
├── Script (Python script execution)
└── External (System commands)

InternalPipe (Custom stdout handler)
```

### Command Class (Base)
The foundation class that all command types inherit from.

**Key Responsibilities:**
- Parse command strings and extract parameters
- Handle I/O redirection (`<` and `>`)
- Manage file handles for stdin/stdout
- Provide common interface for all command types

**Key Methods:**
```python
__init__(st_prompt)           # Initialize command from string
handle_redirect()             # Parse < and > operators
open_redirects()              # Open file handles
close_redirects()             # Clean up resources
parse_redirects(command)      # Split by redirect operators
```

### Internal Class (Inherits Command)
Implements built-in shell commands without spawning external processes.

**Supported Commands:**
- `cd` - Change directory
- `echo` - Display messages or control echoing
- `set` - Manage environment variables
- `time` - Display/set system time
- `color` - Set console colors
- `cls` - Clear screen
- `help` - Show command documentation
- `exit` - Quit shell

**Key Features:**
- Output capture for pipeline support
- Environment variable expansion (`%VAR%`)
- Custom stdout redirection handling
- Comprehensive help system

**Key Methods:**
```python
is_internal(st)               # Static: Check if command is internal
run(start=True)               # Execute the internal command
capture_output_and_run()      # Capture stdout for piping
expand_vars(value)            # Expand %VAR% syntax
```

### Script Class (Inherits Command)
Handles execution of Python scripts (`.py` files).

**Key Features:**
- Automatic path resolution across multiple directories
- Parameter passing to scripts
- Full pipeline and redirection support
- Subprocess management

**Key Methods:**
```python
is_script(st)                 # Static: Check if command is .py file
run(start=True)               # Execute Python script
search_py_file_path(command)  # Find script in MY_PATH directories
```

### External Class (Inherits Command)
Executes any external system command or program.

**Key Features:**
- Shell command execution via subprocess
- Full stdin/stdout redirection
- Error handling and reporting
- Pipeline compatibility

**Key Methods:**
```python
run(start=True)               # Execute external command via shell
```

### InternalPipe Class
A custom wrapper that mimics `subprocess.Popen` for internal commands.

**Purpose:**
Allows internal commands to participate in pipelines alongside external commands by providing a compatible interface.

**Key Features:**
- Pipe-based stdout simulation
- Compatible with subprocess pipeline logic
- Zero return code for successful execution

## 🔧 Technical Highlights

### 1. **Polymorphism in Action**
All command types share the same `run()` interface, allowing uniform pipeline processing:
```python
def run_pipeline(list_of_commands):
    for i, command in enumerate(list_of_commands):
        # Works for Internal, Script, AND External commands
        command.run(start=(i == len(list_of_commands) - 1))
```

### 2. **Factory Pattern**
Dynamic command object creation based on input:
```python
def create_command(prompt):
    if Internal.is_internal(prompt):
        return Internal(prompt)
    if Script.is_script(prompt):
        return Script(prompt)
    return External(prompt)
```

### 3. **Pipeline Processing**
Elegant chaining of commands with proper stdin/stdout management:
```python
# Example: dir | findstr .py | sort
run_pipeline([External("dir"), External("findstr .py"), External("sort")])
```

### 4. **I/O Redirection**
Regex-based parsing and file handle management:
```python
# Example: echo Hello > output.txt
# Example: sort < input.txt > sorted.txt
```

## 📝 Usage Examples

### Basic Commands
```bash
cd Documents                    # Change directory
echo Hello World               # Display message
set PATH=C:\tools              # Set environment variable
time                           # Show/set time
color 0A                       # Matrix green theme
help cd                        # Get help for cd command
```

### Environment Variables
```bash
set MY_VAR=Hello               # Set variable
echo %MY_VAR%                  # Display: Hello
set MY_VAR=%PATH%;C:\tools     # Append to PATH
```

### Pipelines
```bash
dir | findstr .py              # List only .py files
echo Hello | sort              # Pipe to sort
python script.py | findstr ERROR   # Filter script output
```

### I/O Redirection
```bash
dir > files.txt                # Redirect output to file
sort < input.txt               # Read input from file
echo Data > file.txt           # Write to file
python script.py > output.txt  # Redirect script output
```

### Python Scripts
```bash
script.py                      # Run Python script
script.py arg1 arg2            # Pass arguments
script.py > output.txt         # Redirect script output
```

## ⚙️ Configuration

### Custom Search Paths
Modify the `MY_PATH` list to add directories for Python script resolution:
```python
MY_PATH = [os.getcwd(), "C:\\pythonProject2", "D:\\Shell"]
```

### Debug Mode
Enable detailed error messages:
```python
DEBUG = True
```

### Echo Control
Toggle prompt display:
```python
ECHO_ON = False  # Hides the directory prompt
```

## 🎯 Design Principles Demonstrated

1. **Inheritance**: Shared functionality in base `Command` class
2. **Encapsulation**: Each class manages its own execution logic
3. **Polymorphism**: Uniform `run()` interface across all command types
4. **Separation of Concerns**: Distinct classes for internal, script, and external commands
5. **Error Handling**: Comprehensive exception handling with custom error messages
6. **Resource Management**: Proper file handle opening/closing

## 🚀 Getting Started

1. **Run the shell:**
```bash
python shell.py
```

2. **Try some commands:**
```bash
help                    # See available commands
cd ..                   # Navigate directories
echo Hello World        # Test internal commands
dir | findstr .py       # Test pipelines
```

3. **Exit:**
```bash
exit
```

## 📋 Requirements

- Python 3.x
- Windows OS (for color and time commands)
- Standard library only (no external dependencies)

## 🤝 Contributing

This is an educational project demonstrating OOP principles. Feel free to:
- Add new internal commands
- Enhance error handling
- Improve pipeline performance
- Add cross-platform support

## 📄 License

Educational/Personal Use

---

**Author:** Nadav

*A demonstration of object-oriented design, inheritance, and system programming in Python.*
