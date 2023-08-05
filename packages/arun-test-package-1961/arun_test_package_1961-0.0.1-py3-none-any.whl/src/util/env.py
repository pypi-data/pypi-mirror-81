import os


def get_env_value(name: str) -> str:
    value = os.environ[name]
    if not value:
        raise ValueError(f"Expected to find an environment variable named {name}, but didn't")
    return value


def get_repo_name() -> str:
    return get_env_value("GITHUB_REPOSITORY")


def get_github_token() -> str:
    return get_env_value("READ_PR_TOKEN")
