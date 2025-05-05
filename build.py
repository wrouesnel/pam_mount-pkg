
#!/usr/bin/env python3

import os
import subprocess
import re
import shutil

subprocess.run(["dnf", "install", "-y", "fedpkg", "dnf-plugins-core"])


subprocess.run(["fedpkg", "co", "--anonymous", "pam_mount"])

os.chdir("pam_mount")

subprocess.run(["dnf", "builddep", "-y", "pam_mount.spec"])
subprocess.run(["fedpkg", "sources"])

print("Editing the spec file")

with open("pam_mount.spec", "rt") as f:
    lines = f.read().split("\n")

output_lines = []
for line in lines:
    if line.startswith("Release:"):
        m = re.match(r"Release:(\s+)(\d+)(.*)", line)
        release_num = int(m.group(2)) + 1
        output_lines.append(f"Release:{m.group(1)}{release_num}{m.group(3)}.wrouesnel")
    elif line.startswith("Patch0:"):
        output_lines.append(line)
        m = re.match(r"^Patch0:(\s+)",line)

        # Add the new patch
        output_lines.append("# Add ignoresource option to handle bind mounts")
        output_lines.append(f"Patch1:{m.group(1)}0001-add-ignoresource-option.patch")
    elif line.startswith("%patch -P0"):
        output_lines.append(line)
        output_lines.append("%patch -P1 -p1 -b.Add-ignoresource-option")
    else:
        output_lines.append(line)

with open("pam_mount.spec", "wt") as f:
    f.write("\n".join(output_lines))

shutil.copy("../0001-add-ignoresource-option.patch", "0001-add-ignoresource-option.patch")

subprocess.run(["fedpkg", "prep"])
subprocess.run(["fedpkg", "--release", "f42", "local"])

os.chdir("..")