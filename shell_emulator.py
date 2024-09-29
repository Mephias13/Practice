import os
import tarfile
import argparse


def parse_args():
    parser = argparse.ArgumentParser(description="Shell Emulator")
    parser.add_argument("--user", required=True, help="Username for shell prompt")
    parser.add_argument("--vfs", required=True, help="Path to the tar archive of virtual file system")
    parser.add_argument("--script", required=False, help="Path to a startup script with commands")
    return parser.parse_args()


def load_vfs(tar_path):
    vfs = {}
    try:
        with tarfile.open(tar_path, "r") as tar:
            for member in tar.getmembers():
                if member.isfile() or member.isdir():
                    vfs[member.name] = tar.extractfile(member).read().decode() if member.isfile() else None
    except FileNotFoundError:
        print(f"Error: Virtual filesystem archive not found: {tar_path}")
        exit(1)
    return vfs


def ls(vfs, current_dir):
    for f in vfs:
        relpath = os.path.relpath(f, current_dir)
        if not relpath.startswith("..") and "/" not in relpath:
            print(os.path.basename(f))


def cd(current_dir, target_dir, vfs):
    if target_dir == "/":
        return "/"
    elif target_dir == "..":
        new_dir = "/".join(current_dir.lstrip("/").split("/")[:-1])
        if not new_dir:
            return "/"
        else:
            return "/" + new_dir

    new_dir = current_dir.rstrip("/") + "/" + target_dir
    tar_path = new_dir.lstrip("/")

    if any(f == tar_path or f.startswith(tar_path + "/") for f in vfs):
        return new_dir
    else:
        print("Directory not found.")
        return current_dir


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def echo(text):
    print(text)


def exit_shell():
    print("Exiting shell...")
    exit()


def execute_command(command, current_dir, vfs):
    parts = command.split()
    if not parts:
        return current_dir
    cmd = parts[0]

    if cmd == "ls":
        ls(vfs, current_dir)
    elif cmd == "cd":
        if len(parts) > 1:
            current_dir = cd(current_dir, parts[1], vfs)
        else:
            print("Usage: cd <directory>")
    elif cmd == "clear":
        clear()
    elif cmd == "echo":
        echo(" ".join(parts[1:]))
    elif cmd == "exit":
        exit_shell()
    else:
        print(f"Unknown command: {cmd}")
    return current_dir


def shell_loop(user, vfs):
    current_dir = "/"
    while True:
        command = input(f"{user}@vfs:{current_dir}$ ")
        current_dir = execute_command(command, current_dir, vfs)


def run_script(script_path, vfs):
    try:
        with open(script_path, 'r') as script:
            current_dir = "/"
            for command in script:
                current_dir = execute_command(command.strip(), current_dir, vfs)
    except FileNotFoundError:
        print(f"Error: Startup script not found: {script_path}")



if __name__ == "__main__":
    args = parse_args()
    vfs = load_vfs(args.vfs)

    if args.script:
        run_script(args.script, vfs)

    shell_loop(args.user, vfs)