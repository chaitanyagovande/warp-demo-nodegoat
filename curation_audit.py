import requests
import json
import sys
import os

# Ensure correct usage
if len(sys.argv) < 3:
    print("Usage: python yarn_curation_audit.py <ARTIFACTORY_BASE_URL> <ACCESS_TOKEN>")
    sys.exit(1)

ARTIFACTORY_BASE_URL = sys.argv[1]
ACCESS_TOKEN = sys.argv[2]
PACKAGE_LOCK_FILE = "package-lock.json"

def fetch_dependencies():
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

def check_artifactory(package_name, package_version):
    """
    Checks if a package exists in Artifactory.
    """
    package_url = f"{ARTIFACTORY_BASE_URL}/{package_name}/-/{package_name}-{package_version}.tgz"
    headers = {'Authorization': f'Bearer {ACCESS_TOKEN}'}

    try:
        response = requests.head(package_url, headers=headers, allow_redirects=False)

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


#        if response.status_code == 403:
#            print(f"{package_name} {package_version} ❌ Blocked (403 Forbidden)")
#            if response.text.strip():
#                print(f"Error Message: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"{package_name} {package_version} ❌ Request Failed")
        print(f"Exception: {e}")

if __name__ == "__main__":
    dependencies = fetch_dependencies()
    if not dependencies:
        print("No dependencies found to audit.")
        sys.exit(0)

    for dep in dependencies:
        check_artifactory(dep["name"], dep["version"])
