{
  description = "Sergei Volkov - Personal Landing Page (taranarmo.github.io)";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs { inherit system; };
        pythonEnv = pkgs.python3.withPackages (ps: with ps; [
          markdown
          pyyaml
          jinja2
        ]);

        # Static site build derivation
        site = pkgs.stdenv.mkDerivation {
          name = "taranarmo-github-io";
          src = ./.;
          buildInputs = [ pythonEnv ];
          phases = [ "unpackPhase" "buildPhase" ];
          buildPhase = ''
            mkdir -p $out
            python3 scripts/build.py --out-dir $out
          '';
        };

        # Local development & preview server
        devServer = pkgs.writeShellScriptBin "serve" ''
          set -e
          echo "🔨 Compiling landing page from Markdown..."
          ${pythonEnv}/bin/python3 scripts/build.py
          PORT="''${PORT:-8080}"
          echo "🌐 Starting local web server on http://localhost:$PORT"
          echo "📂 Serving root directory (including ./cv/)"
          echo "Press Ctrl+C to stop."
          ${pythonEnv}/bin/python3 -m http.server "$PORT"
        '';

        # Build-only runner
        builderApp = pkgs.writeShellScriptBin "build-site" ''
          set -e
          echo "🔨 Compiling landing page to repository root..."
          ${pythonEnv}/bin/python3 scripts/build.py
        '';
      in {
        packages = {
          default = site;
          site = site;
        };

        apps = {
          default = {
            type = "app";
            program = "${devServer}/bin/serve";
          };
          serve = {
            type = "app";
            program = "${devServer}/bin/serve";
          };
          build = {
            type = "app";
            program = "${builderApp}/bin/build-site";
          };
        };

        devShells.default = pkgs.mkShell {
          buildInputs = [
            pythonEnv
          ];
        };
      }
    );
}
