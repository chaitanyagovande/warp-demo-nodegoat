import requests
import json
import sys
import os
import yaml

# Ensure correct usage
if len(sys.argv) < 3:
    print("Usage: python yarn_curation_audit.py <ARTIFACTORY_BASE_URL> <ACCESS_TOKEN>")
    sys.exit(1)

ARTIFACTORY_BASE_URL = sys.argv[1]
ACCESS_TOKEN = sys.argv[2]
PACKAGE_LOCK_FILE = "package-lock.json"
PNPM_LOCK_FILE = "pnpm-lock.yaml"

def fetch_dependencies_from_package_lock():
    """
    Reads dependencies from the package-lock.json file.
    """
    dependencies = []

    if not os.path.exists(PACKAGE_LOCK_FILE):
        print(f"Error: {PACKAGE_LOCK_FILE} not found. Please ensure it exists.")
        sys.exit(1)

    try:
        with open(PACKAGE_LOCK_FILE, 'r') as f:
            lock_data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from {PACKAGE_LOCK_FILE}: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading {PACKAGE_LOCK_FILE}: {e}")
        sys.exit(1)

    def recurse_dependencies(deps):
        for name, info in deps.items():
            version = info.get("version")
            if name and version:
                dependencies.append({"name": name, "version": version})
            if "dependencies" in info:
                recurse_dependencies(info["dependencies"])

    if "dependencies" in lock_data:
        recurse_dependencies(lock_data["dependencies"])
    else:
        print(f"Warning: 'dependencies' key not found in {PACKAGE_LOCK_FILE}. Check the file structure.")

    return dependencies

def fetch_dependencies_from_pnpm_lock():
    """
    Reads dependencies from the pnpm-lock.yaml file.
    """
    dependencies = []

    if not os.path.exists(PNPM_LOCK_FILE):
        print(f"Error: {PNPM_LOCK_FILE} not found. Please ensure it exists.")
        sys.exit(1)

    try:
        with open(PNPM_LOCK_FILE, 'r') as f:
            lock_data = yaml.safe_load(f)
    except yaml.YAMLError as e:
        print(f"Error decoding YAML from {PNPM_LOCK_FILE}: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading {PNPM_LOCK_FILE}: {e}")
        sys.exit(1)

    if "packages" in lock_data:
        for key, info in lock_data["packages"].items():
            if key.startswith("/"):
                parts = key.split("/")
                if len(parts) == 3:
                    name = parts[1]
                    version = parts[2]
                    if name and version:
                        dependencies.append({"name": name, "version": version})
    else:
        print(f"Warning: 'packages' key not found in {PNPM_LOCK_FILE}. Check the file structure.")

    return dependencies

def check_artifactory(package_name, package_version):
    """
    Checks if a package exists in Artifactory.
    """
    package_url = f"{ARTIFACTORY_BASE_URL}/{package_name}/-/{package_name}-{package_version}.tgz"
    headers = {'Authorization': f'Bearer {ACCESS_TOKEN}'}

    try:
        response = requests.get(package_url, headers=headers, allow_redirects=False)

        if response.status_code == 200:
            print(f"{package_name} {package_version} ✅ Available in Artifactory")
        elif response.status_code == 403:
            print(f"{package_name} {package_version} ❌ Blocked (403 Forbidden)")
            if response.text.strip():
                print(f"Error Message: {response.text}")
        elif response.status_code == 404:
            print(f"{package_name} {package_version} ❌ Not Found (404)")
        else:
            print(f"{package_name} {package_version} ⚠️ Unexpected Response: {response.status_code}")
            if response.text.strip():
                print(f"Error Message: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"{package_name} {package_version} ❌ Request Failed")
        print(f"Exception: {e}")

if __name__ == "__main__":
    # You can switch between the following depending on your lock file:
    #dependencies = fetch_dependencies_from_package_lock()
    dependencies = fetch_dependencies_from_pnpm_lock()

    if not dependencies:
        print("No dependencies found to audit.")
        sys.exit(0)

    for dep in dependencies:
        check_artifactory(dep["name"], dep["version"])
