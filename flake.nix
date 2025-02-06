{
  description = "PyTorch, TorchVision, Transformers, and Gradio environment with venv";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs { inherit system; };
        python = pkgs.python312;
        pythonPackages = pkgs.python312Packages; # Corrected line
        venvDir = ./venv;
      in
      {
        devShell = pkgs.mkShell {
          buildInputs = [
            python
            pythonPackages.torch-bin
            pythonPackages.torchvision-bin
            pythonPackages.transformers
            pythonPackages.gradio
          ];

          shellHook = ''
            echo "blip env"
          '';
        };
      });
}

