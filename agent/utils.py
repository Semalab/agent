import subprocess


def flatten(lst):
    return [y for x in lst for y in x]

def run_logged(args, *runargs, log_dir, **kwargs):
    with open(log_dir / (args[0] + ".log"), "a") as log_file:
        log_file.write(f"--- Running {str(args)}\n")

        if "capture_output" in kwargs or "stdout" in kwargs:
            kwargs["stderr"] = log_file
        else:
            kwargs["stderr"] = subprocess.STDOUT
            kwargs["stdout"] = log_file
        
        proc = subprocess.run(args, *runargs, **kwargs)
        log_file.write(f"--- Process {args[0]} exited with code {proc.returncode}\n")
        return proc
