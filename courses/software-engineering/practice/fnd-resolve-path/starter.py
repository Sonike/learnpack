def resolve(cwd: str, path: str) -> str:
    """Return the absolute, clean version of path, as seen from the folder cwd."""
    # TODO: if path starts with "/", start with parts = []; otherwise split cwd into its folder names
    # TODO: for each piece of path.split("/"):
    #         skip "" and "."
    #         ".." -> remove the last part (if there is one)
    #         anything else -> append it
    # TODO: join the parts back with "/" and put a "/" in front
    return cwd


if __name__ == "__main__":
    print(resolve("/home/ada", "projects/app"))      # /home/ada/projects/app
    print(resolve("/home/ada/projects", "../data"))  # /home/ada/data
    print(resolve("/home/ada", "/etc//hosts/"))      # /etc/hosts
    print(resolve("/", "../.."))                     # /
