# nix-flake-poetry-example


## Development

To drop into a shell:

	nix develop
	
To run a python file quick:

	nix develop -c python etaml/__init__.py

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

Results will be placed in `./result`. Run a wrapper script with:

	nix build .#etaml && ./result/bin/run.py

Create data:

	nix build .#data && cat result/data.txt

## See also
https://josephsdavid.github.io/nix.html
https://github.com/nix-community/nix-data-science/blob/master/overlays.nix