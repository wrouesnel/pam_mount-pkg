# pam_mount repackaging

Build and patch pam_mount with the `ignoresource` [patch](https://codeberg.org/jengelh/pam_mount/pulls/5).

This repository currently builds a Fedora 42 repository for x86_64.

## Usage

```
[pam_mount-pkg]
name=Updated pam_mount packages
baseurl=https://blog.wrouesnel.com/pam_mount-pkg
enabled=1
countme=1
metadata_expire=7d
repo_gpgcheck=0
type=rpm
gpgcheck=0
skip_if_unavailable=False
```

## How It Works

This repository is solely a GitHub actions repository. The `build.py` script handles building a new package with
`fedpkg` and then releases it as a Github asset. The repository is then built as Github Pages.