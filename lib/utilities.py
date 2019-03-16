import yaml


def load_config(*, file_path="./config.yml", profile="default"):
    """ Load config file"""
    with open(file_path, "r") as file:
        return yaml.load(file, Loader=yaml.Loader).get(profile, {})
