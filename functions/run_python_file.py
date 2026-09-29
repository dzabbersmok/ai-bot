import os
import subprocess

def run_python_file(working_directory: str, file_path: str, args: list[str] | None = None) -> str:
    try:
        if file_path[-3:] != ".py":
            return f'Error: "{file_path}" is not a Python file'

        working_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
        # Will be True or False
        valid_target_file = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs
        if not valid_target_file:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(target_file):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        command = ["python", target_file]
        if args and len(args) > 0:
            command.extend(args)

        completed_process = subprocess.run(command, cwd=working_dir_abs, capture_output=True, text=True, timeout=30)
        output = ""
        if completed_process.returncode != 0:
            output += f"Process exited with code {completed_process.returncode}\n"
        if len(completed_process.stdout) == 0 and len(completed_process.stderr) == 0:
            output += f"No output produced\n"
        else:
            output += f"STDOUT: {completed_process.stdout}\n"
            output += f"STDERR: {completed_process.stderr}\n"

        return output
    except Exception as e:
        return f"Error: executing Python file: {e}"

print(run_python_file("calculator", "lorem.txt"))
