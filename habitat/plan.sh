HAB_BLDR_CHANNEL=unstable

pkg_name=bkmrk
pkg_origin=bkmrk
# TODO: set pkg_version to bumpversion
# pkg_version="0.1.0"
pkg_version="master"
pkg_maintainer="Victor Yap <mail.bkmrk@gmail.com>"
pkg_license=("MIT")
pkg_filename="${pkg_name}-${pkg_version}.tar.bz2"
pkg_deps=(core/python)
pkg_build_deps=(core/git core/cacerts core/python core/which)
pkg_bin_dirs=(bin)
pkg_exports=(
  [port]=server.port
)
pkg_exposes=(port)
# pkg_description="Some description."
# pkg_upstream_url="http://example.com/project-name"

do_download() {
  export GIT_SSL_CAINFO="$(pkg_path_for core/cacerts)/ssl/certs/cacert.pem"
  rm -rf bkmrk
  git clone https://github.com/vicyap/bkmrk
  pushd bkmrk
  git checkout $pkg_version
  popd
  tar -cjvf $HAB_CACHE_SRC_PATH/${pkg_filename} \
      --transform "s,^./bkmrk,bkmrk-${pkg_version}," ./bkmrk \
      --exclude bkmrk/.git
  pkg_shasum=$(trim $(sha256sum $HAB_CACHE_SRC_PATH/${pkg_filename} | cut -d " " -f 1))
}

do_build() {
  return 0
}

do_install() {
  pushd "${pkg_prefix}"
  rm -rf bkmrk
  git clone https://github.com/vicyap/bkmrk
  pushd bkmrk
  git checkout $pkg_version
  pip install pipenv
  export LC_ALL="en_US.utf8"
  export LANG="en_US.utf8"
  export PIPENV_VENV_IN_PROJECT=1
  pipenv install
  popd
  popd
}
