let
  # pin nixpkgs to a specific version, so that we're not relying on the system version
  pkgs = import (builtins.fetchGit {
    name = "nixpkgs-unstable";
    url = "https://github.com/nixos/nixpkgs/";
    # `git ls-remote https://github.com/nixos/nixpkgs nixos-unstable`
    ref = "refs/heads/nixpkgs-unstable";
    rev = "bd4dffcdb7c577d74745bd1eff6230172bd176d5";
  }) {};

  # Use svenklemm's fork of pglast, which adds support for SET, COMMIT, ROLLBACK, CALL
  pglast = pkgs.python310Packages.buildPythonPackage rec {
    name = "pglast";
    version = "v3.10";

    src = pkgs.fetchFromGitHub {
      owner = "lelit";
      repo = "${name}";
      rev = "${version}";
      fetchSubmodules = true;
      sha256 = "sha256-lBAhdqLTt7x/NYYfgcMm/qk04r4YuLDeWYmI8WaMZm8=";
    };
  };

  py310 = pkgs.python310;
  py-with-packages = py310.withPackages (p: with p; [
    pglast
    p.black
    p.tox
    p.setuptools
    p.build
    p.twine
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
