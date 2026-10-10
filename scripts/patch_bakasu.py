#!/usr/bin/env python3
import os
import re

kconfig_path = "KernelSU/kernel/Kconfig"
if os.path.exists(kconfig_path):
    with open(kconfig_path, "r") as f:
        content = f.read()
    content = re.sub(r'config KSU_SUSFS\n\s+bool "SUSFS Inline Hook"[\s\S]*?endchoice', 'endchoice', content)
    replacement = """endchoice

config KSU_SUSFS
\tbool "SUSFS Support"
\tdepends on KSU && THREAD_INFO_IN_TASK && 64BIT
\tdefault y
\thelp
\t  Patch and Enable SUSFS to kernel with KernelSU.
\t  SuSFS Officially support kernel 5.10+
\t  This KSU driver support it for 4.3+ in KSU side, 
\t  But the kernel side susfs compatibility MUST completed by yourself.
"""
    if 'config KSU_SUSFS\n\tbool "SUSFS Support"' not in content:
        content = content.replace("endchoice", replacement, 1)
    with open(kconfig_path, "w") as f:
        f.write(content)
    print("Successfully patched KernelSU/kernel/Kconfig")

kbuild_path = "KernelSU/kernel/Kbuild"
if os.path.exists(kbuild_path):
    with open(kbuild_path, "r") as f:
        content = f.read()

    if "susfs_compat.mk" not in content:
        content = content.replace(
            "ifdef CONFIG_KSU_SUSFS",
            "ifdef CONFIG_KSU_SUSFS\n  include $(KSU_SRC)/tools/susfs_compat.mk",
            1
        )

    if "CONFIG_KSU_FULL_NAME_FORMAT :=" not in content:
        target = "# call subst to process placeholders"
        fallback = "ifeq ($(CONFIG_KSU_FULL_NAME_FORMAT),)\nCONFIG_KSU_FULL_NAME_FORMAT := %TAG_NAME%-%COMMIT_SHA%@%REPO_NAME%\nendif\n"
        content = content.replace(target, fallback + target, 1)

    with open(kbuild_path, "w") as f:
        f.write(content)
    print("Successfully patched KernelSU/kernel/Kbuild")
