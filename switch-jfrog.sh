#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECTS_DIR="$SCRIPT_DIR/.jfrog/projects"
CONFIGS_DIR="$PROJECTS_DIR/configs"
SYMLINK_PATH="$PROJECTS_DIR/npm.yaml"

GREEN='\033[0;32m'
YELLOW='\033[0;33m'
RED='\033[0;31m'
BOLD='\033[1m'
RESET='\033[0m'

usage() {
    cat <<EOF
Usage: $(basename "$0") <command> [args]

Commands:
  list            Show available JFrog npm configs
  use <name>      Switch to a named config
  save <name>     Run jf npm-config and save the result as a named config

Examples:
  $(basename "$0") list
  $(basename "$0") use dematic
  $(basename "$0") save acme-corp
EOF
    exit 1
}

get_active() {
    if [ -L "$SYMLINK_PATH" ]; then
        basename "$(readlink "$SYMLINK_PATH")" .yaml
    else
        echo ""
    fi
}

cmd_list() {
    if [ ! -d "$CONFIGS_DIR" ] || [ -z "$(ls -A "$CONFIGS_DIR"/*.yaml 2>/dev/null)" ]; then
        echo "No configs found in $CONFIGS_DIR"
        exit 1
    fi

    local active
    active="$(get_active)"

    echo -e "${BOLD}Available JFrog npm configs:${RESET}"
    for f in "$CONFIGS_DIR"/*.yaml; do
        local name
        name="$(basename "$f" .yaml)"
        if [ "$name" = "$active" ]; then
            echo -e "  ${GREEN}* $name${RESET}  (active)"
        else
            echo "    $name"
        fi
    done
}

cmd_use() {
    local name="$1"
    local target="$CONFIGS_DIR/$name.yaml"

    if [ ! -f "$target" ]; then
        echo -e "${RED}Error:${RESET} Config '$name' not found."
        echo "Available configs:"
        cmd_list
        exit 1
    fi

    rm -f "$SYMLINK_PATH"
    ln -sf "configs/$name.yaml" "$SYMLINK_PATH"
    echo -e "Switched to ${GREEN}${BOLD}$name${RESET}"
}

cmd_save() {
    local name="$1"
    local target="$CONFIGS_DIR/$name.yaml"

    mkdir -p "$CONFIGS_DIR"

    # If npm.yaml is a symlink, remove it so jf npm-config can write a regular file
    if [ -L "$SYMLINK_PATH" ]; then
        rm -f "$SYMLINK_PATH"
    fi

    echo -e "${YELLOW}Running jf npm-config...${RESET}"
    (cd "$SCRIPT_DIR" && jf npm-config --global=false)

    if [ ! -f "$SYMLINK_PATH" ]; then
        echo -e "${RED}Error:${RESET} jf npm-config did not produce $SYMLINK_PATH"
        exit 1
    fi

    mv "$SYMLINK_PATH" "$target"
    ln -sf "configs/$name.yaml" "$SYMLINK_PATH"
    echo -e "Saved and switched to ${GREEN}${BOLD}$name${RESET}"
}

if [ $# -lt 1 ]; then
    usage
fi

case "$1" in
    list)
        cmd_list
        ;;
    use)
        [ $# -lt 2 ] && { echo -e "${RED}Error:${RESET} 'use' requires a config name."; usage; }
        cmd_use "$2"
        ;;
    save)
        [ $# -lt 2 ] && { echo -e "${RED}Error:${RESET} 'save' requires a config name."; usage; }
        cmd_save "$2"
        ;;
    *)
        echo -e "${RED}Unknown command:${RESET} $1"
        usage
        ;;
esac
