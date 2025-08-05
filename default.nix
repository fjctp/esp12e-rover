# Run Beyond All Reason (BAR) using AppImage.
# Note: it takes a minute to start for the first time. You may see a blank screen.

let
  # Pin nixpkgs.
  nixpkgs = fetchTarball "https://github.com/NixOS/nixpkgs/tarball/nixos-25.05";
  pkgs = import nixpkgs { config = {}; overlays = []; };
in
pkgs.mkShellNoCC {
  name = "arduino-dev";
  packages = with pkgs; [
    arduino-ide
    python312 # for esp12e
    python312Packages.keyboard
  ];

  shellHook = ''
    alias control_robot='sudo PYTHONPATH=$PYTHONPATH ${pkgs.python312}/bin/python3 scripts/udp_client.py'
  '';
}
