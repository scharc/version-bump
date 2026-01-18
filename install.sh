#!/usr/bin/env bash
set -e

echo "Installing version-bump..."

# Check if pipx is available
if ! command -v pipx &> /dev/null; then
    echo "pipx not found. Installing pipx..."
    pip install --user pipx
    pipx ensurepath
fi

# Build the package
echo "Building package..."
poetry build -q

# Install with pipx
echo "Installing with pipx..."
pipx install dist/*.whl --force

# Setup shell completion
echo "Setting up shell completion..."
SHELL_NAME=$(basename "$SHELL")

case "$SHELL_NAME" in
    bash)
        mkdir -p ~/.local/share/bash-completion/completions
        _VERSION_BUMP_COMPLETE=bash_source version-bump > ~/.local/share/bash-completion/completions/version-bump
        echo "Bash completion installed."
        ;;
    zsh)
        mkdir -p ~/.zfunc
        _VERSION_BUMP_COMPLETE=zsh_source version-bump > ~/.zfunc/_version-bump
        echo "Zsh completion installed. Add 'fpath+=~/.zfunc' to ~/.zshrc before compinit."
        ;;
    fish)
        mkdir -p ~/.config/fish/completions
        _VERSION_BUMP_COMPLETE=fish_source version-bump > ~/.config/fish/completions/version-bump.fish
        echo "Fish completion installed."
        ;;
    *)
        echo "Unknown shell: $SHELL_NAME. Skipping completion setup."
        ;;
esac

echo ""
echo "Done! Run 'version-bump --help' to get started."
