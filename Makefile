# Makefile for version-bump

# Variables
APP_NAME = version-bump
SRC_DIR = version_bump
MAIN_FILE = $(SRC_DIR)/main.py
DIST_DIR = dist

.PHONY: all clean build install

# Default target
all: build

# Build the standalone binary
build:
	@echo "Building standalone binary..."
	poetry run pyinstaller --onefile --name $(APP_NAME) --hidden-import=click $(MAIN_FILE)
	@echo "Binary created in $(DIST_DIR)/$(APP_NAME)."

# Install the binary to the user directory
install: build
	@echo "Installing binary to ~/.local/bin..."
	mkdir -p ~/.local/bin
	cp $(DIST_DIR)/$(APP_NAME) ~/.local/bin/
	@echo "Installation complete. Ensure ~/.local/bin is in your PATH."

# Clean up build artifacts
clean:
	@echo "Cleaning up build artifacts..."
	rm -rf build $(DIST_DIR) $(APP_NAME).spec
	@echo "Clean up complete."
