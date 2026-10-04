import argparse
import subprocess
import sys

def main():
    parser = argparse.ArgumentParser(description="Directly fork and clone a GitHub repository without sparse-checkout.")
    parser.add_argument("repo", help="The repository to fork and clone (e.g. owner/repo)")
    args = parser.parse_args()

    repo = args.repo
    print(f"[*] Forking and cloning {repo} directly...")

    try:
        # Use gh repo fork with --clone flag to fork and clone natively
        subprocess.run(["gh", "repo", "fork", repo, "--clone"], check=True)
        print(f"[+] Successfully forked and cloned {repo}.")
    except subprocess.CalledProcessError as e:
        print(f"[-] Error: Failed to fork and clone {repo}. Ensure you are authenticated with 'gh auth login'.")
        sys.exit(e.returncode)

if __name__ == "__main__":
    main()
