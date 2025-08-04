# Run Beyond All Reason (BAR) using AppImage.
# Note: it takes a minute to start for the first time. You may see a blank screen.

let
  # Pin nixpkgs.
  nixpkgs = fetchTarball "https://github.com/NixOS/nixpkgs/tarball/nixos-25.05";
  pkgs = import nixpkgs { config = {}; overlays = []; };
in
pkgs.mkShellNoCC {
  name = "bar";
  packages = with pkgs; [
    arduino-ide
    python3 # for esp12e
  ];
}
