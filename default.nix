{ lib, pkgs, wrapQtAppsHook }:

let
  python =
    let
      packageOverrides = self:
        super: {
          opencv4 = super.opencv4.override {
            enableGtk2 = true;
            gtk2 = pkgs.gtk2;
            #enableFfmpeg = true; #here is how to add ffmpeg and other compilation flags
            #ffmpeg_3 = pkgs.ffmpeg-full;
          };
        };
    in
    pkgs.python39.override { inherit packageOverrides; self = python; };

  runPackages = with python.pkgs;[
    python
    attrs
    numpy
    opencv4
    hypothesis
    pytest
    tensorflow
    keras
  ];

  devPackages = with python.pkgs;[
    tkinter
    pyqt5
    pylint
    flake8
    black
  ] ++ runPackages;
in
{
  package = python.pkgs.buildPythonPackage {
    pname = "python-dev";
    version = "1.0";
    checkInputs = [ python.pkgs.pytest ];
    checkPhase = "pytest";
    propagatedBuildInputs = runPackages;
    src = ./.;
    nativeBuildInputs = [ wrapQtAppsHook ];
    postFixup = ''wrapQtApp $out/bin/run.py "''${qtWrapperArgs[@]}"'';
  };

  devShell = pkgs.mkShell {
    name = "python-shell";
    buildInputs = [ pkgs.qt5.qtwayland ] ++ devPackages;
    # QT_QPA_PLATFORM_PLUGIN_PATH = "${pkgs.qt5.qtbase.bin}/lib/qt-${pkgs.qt5.qtbase.version}/plugins";
  };
}

