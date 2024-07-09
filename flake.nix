{
  description = "A flake to build a Pelican static site";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }: flake-utils.lib.eachDefaultSystem (system:
    let
      pkgs = import nixpkgs { inherit system; };
    in {
      devShell = pkgs.mkShell {
        buildInputs = [
          pkgs.python310
          pkgs.python310Packages.pelican
          pkgs.python310Packages.markdown
        ];
      };

      defaultPackage = pkgs.writeShellScriptBin "build-site" ''
        export PATH=$PATH:${pkgs.python310Packages.pelican}/bin
        pelican content -o output -s pelicanconf.py
      '';
    });
}
