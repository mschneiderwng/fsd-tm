{
  description = "eta-ml flake";

  inputs = {
    nixpkgs.url = github:nixos/nixpkgs/nixos-unstable;
    flake-utils.url = github:numtide/flake-utils;
  };

  outputs = { self, nixpkgs, flake-utils }: (
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs {
          inherit system overlays;
          config = { allowUnfree = true; };
        };

        overlay = (final: prev: {
          main = final.libsForQt5.callPackage ./. { };
        });
      in
      rec {
        apps.main = {
          type = "app";
          program = "${pkgs.main.package}/bin/run.py";
        };

        devShell = pkgs.mkShell {
          name = "python-shell";
          buildInputs = pkgs.main.devShell.buildInputs;
          QT_QPA_PLATFORM_PLUGIN_PATH = "${pkgs.qt5.qtbase.bin}/lib/qt-${pkgs.qt5.qtbase.version}/plugins";
        };

        packages = {
          main = pkgs.main.package;
          venv = pkgs.python3.withPackages (ps: [ ps.numpy packages.main ]);
        };
        defaultPackage = packages.venv;
      }));
}

