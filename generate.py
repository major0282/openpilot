#!/usr/bin/env python3

import ast
import logging
import os
import pprint

logging.basicConfig(level=logging.INFO, format="%(message)s")

base_branches = ["master-ci", "release3"]


def parse_cars(branch):
    """
    Parse the file with ast for a class named "CAR" and get a list of all the cars.
    We are looking for the values in quotes.

    Exerpt:

    class CAR:
      # Hyundai
      ELANTRA = "HYUNDAI ELANTRA 2017"
      ELANTRA_2021 = "HYUNDAI ELANTRA 2021"
      ELANTRA_HEV_2021 = "HYUNDAI ELANTRA HYBRID 2021"
      HYUNDAI_GENESIS = "HYUNDAI GENESIS 2015-2016"
      IONIQ = "HYUNDAI IONIQ HYBRID 2017-2019"

    `cars` should be an array of strings like this:

    [
      "HYUNDAI ELANTRA 2017",
      "HYUNDAI ELANTRA 2021",
      "HYUNDAI ELANTRA HYBRID 2021",
      "HYUNDAI GENESIS 2015-2016",
      "HYUNDAI IONIQ HYBRID 2017-2019"
      ...
    ]
    """
    # Checkout branch
    os.system(f"cd comma_openpilot && git checkout --force {branch}")

    paths = ["comma_openpilot/selfdrive/car/hyundai/values.py"]

    cars = []

    for path in paths:
        with open(path, "r") as f:
            tree = ast.parse(f.read())
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef) and node.name == "CAR":
                    for c in node.body:
                        if isinstance(c, ast.Assign):
                            cars.append(c.value.s)

    # Log the cars
    logging.info("Found %d cars in %s", len(cars), branch)

    return cars


def prepare_op_repo():
    """
    Prepare the openpilot repo with master-ci and release3 branches
    """
    # Try to clone the repo to comma_openpilot.
    # If it fails, it means it already exists, so we can just pull
    # the latest changes.
    logging.info("Setting up openpilot repo. Ignore errors if it already exists.")

    os.system(
        "git clone -b master-ci https://github.com/commaai/openpilot.git comma_openpilot"
    )
    # Make sure that comma_openpilot is usiing that as the origin.
    os.system(
        "cd comma_openpilot && git remote set-url origin https://github.com/commaai/openpilot.git"
    )
    os.system("cd comma_openpilot && git fetch origin")
    os.system(
        "cd comma_openpilot && git checkout release3 && git reset --hard origin/release3"
    )
    os.system(
        "cd comma_openpilot && git checkout master-ci && git reset --hard origin/master-ci"
    )

    logging.info("Done setting up openpilot repo.")


def generate_branch(base, car):
    """
    Make a new branch for the car with a hardcoded fingerprint
    """
    branch_name = f"{base}-{car.replace(' ', '_').replace('&', 'AND').lower()}"
    logging.info("Generating branch %s", branch_name)
    # Delete branch if it already exists
    os.system(f"cd comma_openpilot && git branch -D {branch_name}")
    # Make branch off of base branch
    os.system(
        f"cd comma_openpilot && git checkout {base} && git checkout -b {branch_name}"
    )
    # Make sure base branch is clean
    os.system(f"cd comma_openpilot && git reset --hard origin/{base}")
    # Append 'export FINGERPRINT="car name"' to the end of launch_env.sh
    os.system(f"echo 'export FINGERPRINT=\"{car}\"' >> comma_openpilot/launch_env.sh")
    # Commit the changes
    os.system(
        f"cd comma_openpilot && git add launch_env.sh && GIT_AUTHOR_DATE='Fri Jul 29 00:00:00 2023 -0700' GIT_COMMITTER_DATE='Fri Jul 29 00:00:00 2023 -0700' git commit -m 'Hardcode fingerprint for {car}'"
    )
    return branch_name


def main(push=True):
    prepare_op_repo()

    base_cars = {}
    for base in base_branches:
        base_cars[base] = parse_cars(base)

    base_cars_base_branches = {}
    for base in base_branches:
        base_cars_base_branches[base] = {}
        for car in base_cars[base]:
            branch = generate_branch(base, car)
            base_cars_base_branches[base][car] = branch
    logging.info("Done generating branches")

    # Log base_cars_base_branches
    logging.info("base_cars_base_branches:")
    logging.info(pprint.pformat(base_cars_base_branches))

    if push:
        # Run the command to push to origin all the branches
        # Copy .git/config from this git repo to comma_openpilot repo
        # This might make GitHub Actions work
        os.system("cp .git/config comma_openpilot/.git/config")
        logging.info("Pushing branches to origin")
        os.system("cd comma_openpilot && git push origin --force --all")

if __name__ == "__main__":
    # Check if args has dry run, if so, don't push
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "--dry-run":
        main(push=False)
    else:
        main()
