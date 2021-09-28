import os
import re
import shutil
from datetime import date

from packaging.version import parse as vp

from update_assets import update_redoc, update_swagger_ui

PACKAGE = 'drf_spectacular_sidecar'


def update_file(file, func):
    file_tmp = file + '.tmp'
    with open(file) as fh_in, open(file_tmp, "w") as fh_out:
        for line in fh_in.readlines():
            fh_out.write(func(line))
    shutil.move(file_tmp, file)


def run_or_fail(cmd):
    assert not os.system(cmd), f"failed: '{cmd}'"


def main():
    old_redoc_version, new_redoc_version = update_redoc()
    old_swagger_ui_version, new_swagger_ui_version = update_swagger_ui()

    if not new_redoc_version and not new_swagger_ui_version:
        print('no updates available')
        return

    with open(f"{PACKAGE}/__init__.py") as fh:
        old_version = re.search(r"__version__ = '([\d.]+)'\n", fh.read()).group(1)

    today = date.today()
    new_version = f'{today.year}.{today.month}.{today.day}'
    assert vp(old_version) < vp(new_version), 'sidecar version must be newer'

    update_file(
        file=f"{PACKAGE}/__init__.py",
        func=lambda l: l.replace(old_version, new_version)
    )
    if new_redoc_version:
        update_file(
            file="README.rst",
            func=lambda l: l.replace(old_redoc_version, new_redoc_version)
        )
    if new_swagger_ui_version:
        update_file(
            file="README.rst",
            func=lambda l: l.replace(old_swagger_ui_version, new_swagger_ui_version),
        )

    if os.environ.get("CI"):
        run_or_fail("git config user.name github-actions")
        run_or_fail("git config user.email github-actions@github.com")

    # update repo
    run_or_fail("git add .")
    run_or_fail(f"git commit -m 'version bump {new_version}'")
    run_or_fail(f"git tag -a '{new_version}' -m 'version {new_version}'")
    run_or_fail("git push --follow-tags")
    # build
    run_or_fail("python setup.py sdist bdist_wheel")
    run_or_fail("twine check dist/*")
    run_or_fail("twine upload dist/*")
    # cleanup
    shutil.rmtree('dist')
    shutil.rmtree('build')
    shutil.rmtree(f'{PACKAGE}.egg-info')


if __name__ == '__main__':
    main()
