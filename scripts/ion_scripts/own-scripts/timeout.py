import subprocess

# Command arguments
args = [
    '/usr/bin/ion/lite-client/lite-client',
    '--global-config', '/usr/bin/ion/global.config.json',
    '--verbosity', '0',
    '--cmd', 'getconfig 12'
]

# Increase timeout to number of seconds
timeout = 20

# Add debugging output
print(f"Running command: {args}")

# Run the command
try:
    process = subprocess.run(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout)
    print("Command output:", process.stdout.decode())
    print("Command errors:", process.stderr.decode())
except subprocess.TimeoutExpired as e:
    print(f"Error: Command '{e.cmd}' timed out after {e.timeout} seconds")
except subprocess.CalledProcessError as e:
    print(f"Error: Command '{e.cmd}' failed with return code {e.returncode}")
    print(f"Output: {e.output.decode()}")
    print(f"Errors: {e.stderr.decode()}")
