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
    version = "01853619c0ecc4fe531bb0cdbe1207cd090dcc71";

    src = pkgs.fetchFromGitHub {
      owner = "svenklemm";
      repo = "${name}";
      rev = "${version}";
      fetchSubmodules = true;
      sha256 = "sha256-TVlF9BIj3M6ojItuIY7g9oOPfPJ2bfS1utRtqlk0IlU";
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
