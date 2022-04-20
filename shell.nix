let
  # pin nixpkgs to a specific version, so that we're not relying on the system version
  pkgs = import (builtins.fetchGit {
    name = "nixpkgs-21.11";
    url = "https://github.com/nixos/nixpkgs/";
    # `git ls-remote https://github.com/nixos/nixpkgs nixos-unstable`
    ref = "refs/tags/21.11";
    rev = "506445d88e183bce80e47fc612c710eb592045ed";
  }) {};

  # Use svenklemm's fork of pglast, which adds support for SET, COMMIT, ROLLBACK, CALL
  pglast = pkgs.python310Packages.buildPythonPackage rec {
    name = "pglast";
    version = "af4b9b1c4c3011e82f9bdec357136fa779a22e79";

    src = pkgs.fetchFromGitHub {
      owner = "svenklemm";
      repo = "${name}";
      rev = "${version}";
      fetchSubmodules = true;
      sha256 = "sha256-fxGQOwr/MyA48F0qHbhsfb/KCusq/T7GgUwCFNW6Mvg";
    };
  };

  py310 = pkgs.python310;
  py-with-packages = py310.withPackages (p: with p; [
    pglast
    p.pytest
    p.pytest-snapshot
  ]);

in
pkgs.mkShell {
  buildInputs = [
    py-with-packages
  ];
  shellHook = ''
    export PYTHONPATH=${py-with-packages}/${py-with-packages.sitePackages}
  '';
}
