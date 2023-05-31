import os


def flatten(lst):
    return [y for x in lst for y in x]


def detect_version_control_system(folder_path: str) -> str:
    """
    Function to check the type of VCS
    Returns the type of VCS or UNKNOWN
    """
    # Check for Git repository
    git_dir = os.path.join(folder_path, ".git")
    if os.path.isdir(git_dir):
        return "GIT"

    # Check for SVN repository
    svn_dir = os.path.join(folder_path, ".svn")
    if os.path.isdir(svn_dir):
        return "SVN"

    # Check for Mercurial repository
    hg_dir = os.path.join(folder_path, ".hg")
    if os.path.isdir(hg_dir):
        return "MERCURIAL"

    return "UNKNOWN"
