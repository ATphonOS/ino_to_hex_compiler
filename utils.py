import platform

def get_system_key():
    system = platform.system()
    machine = platform.machine().lower()

    system_map = {
        "Windows": lambda m: "Windows_64bit" if "64" in m or "amd64" in m else "Windows_32bit",
        "Linux": lambda m: (
            "Linux_ARM64" if "arm" in m and "64" in m else
            "Linux_ARM" if "arm" in m else
            "Linux_64bit" if "64" in m or "x86_64" in m else "Linux_32bit"
        ),
        "Darwin": lambda m: (
            "Darwin_ARM64" if "arm64" in m else
            "Darwin_x86_64" if "x86_64" in m else
            "Darwin_64bit"
        )
    }

    mapper = system_map.get(system)
    if mapper:
        return mapper(machine)
    raise ValueError(f"Unsupported system: {system}")