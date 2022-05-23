# Demo: Teachable Machine with Python

## Development with Nix

To drop into a shell:

	nix develop
	
To run a python file quick:

	nix develop -c python src/run.py

	nix run
	
Launch this repo in vscode with the path set correctly:

	nix develop -c code .
	
Format python files:

	nix develop -c black .
	
Format nix files:

	nix develop -c nixpkgs-fmt .
	
## Building

To build the package:

	nix build

To create a venv for PyCharm:
	nix build .#venv -o venv