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
    version = "1d567ac31b83785d2ef38602203213d360182b1e";

    src = pkgs.fetchFromGitHub {
      owner = "svenklemm";
      repo = "${name}";
      rev = "${version}";
      fetchSubmodules = true;
      sha256 = "sha256-9ika8Nb8fB9xwigqS49AIBiW4vCpVQxbzPcg2/7iY3c";
    };
  };

  py310 = pkgs.python310;
  py-with-packages = py310.withPackages (p: with p; [
    pglast
    p.black
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
