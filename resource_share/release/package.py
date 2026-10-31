"""Package the exact user-tested DLL. No compilation or game-directory mutation."""
import hashlib
import json
import pathlib
import re
import subprocess
import zipfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
RELEASE = ROOT / "release"
CONFIG = json.loads((RELEASE / "release.json").read_text(encoding="utf-8"))
OUT = ROOT / "build" / "release" / CONFIG["tag"]
OUT.mkdir(parents=True, exist_ok=True)

def digest(data):
    return hashlib.sha256(data).hexdigest().upper()

def read(path):
    return path.read_bytes()

def json_bytes(value):
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")

dll = read(ROOT / "build/native/main.dll")
assert digest(dll) == CONFIG["dll_sha256"], "Only the exact user-tested DLL may be released"
assert dll[:2] == b"MZ", "Not a PE binary"
# Refuse packaging modified native sources under the tested binary's provenance.
for name in ("dllmain.cpp", "minhook_adapter.hpp", "build.py", "dependencies.json"):
    source = "resource_share/native/" + name
    expected = subprocess.check_output(["git", "show", CONFIG["native_source_commit"] + ":" + source], cwd=ROOT.parent)
    current = read(ROOT / "native" / name).replace(b"\r\n", b"\n")
    assert current == expected.replace(b"\r\n", b"\n"), "Native source differs from tested build: " + name

runtime = {
    "dlls/main.dll": dll,
    "Scripts/main.lua": read(ROOT / "Scripts/main.lua"),
    "config.txt": read(ROOT / "config.txt"),
    "LICENSE": read(ROOT / "native/reference/LICENSE"),
    "MINHOOK-LICENSE.txt": read(ROOT / "native/MINHOOK-LICENSE.txt"),
    "NOTICE.md": read(ROOT / "NOTICE.md"),
}
for license_file in sorted((RELEASE / "licenses").iterdir()):
    assert license_file.is_file()
    runtime["licenses/" + license_file.name] = read(license_file)
launcher = runtime["Scripts/main.lua"].decode("utf-8")
assert CONFIG["version"] in launcher and "RegisterHook" not in launcher
assert set(CONFIG["runtime_targets"]) == {p.split("/")[0] for p in runtime}
info = json.loads((RELEASE / "Info.json").read_text(encoding="utf-8"))
assert re.fullmatch(r"[A-Za-z0-9]+", info["PackageName"])
assert info["PackageName"] == "ziyuan" and info["Version"] == CONFIG["version"]
assert info["Dependencies"] == ["UE4SSExperimentalPW"] and info["MinRevision"] == 102999
assert info["InstallRule"] == [{"Type": "Lua", "Targets": ["./" + p for p in CONFIG["runtime_targets"]]}]
assert "WorkshopId" not in info and "Thumbnail" not in info

docs = {p: read(RELEASE / p) for p in ("README.zh-CN.md", "README.en.md", "CHANGELOG.md")}
version = CONFIG["version"]
manual_name = f"ResourceShare-{version}-Palworld-1.0.5-Win64.zip"
uploader_name = f"ResourceShare-{version}-ModUploader.zip"
prefix = "Mods/NativeMods/UE4SS/Mods/ziyuan/"
packages = {
    manual_name: {**{prefix + p: data for p, data in runtime.items()}, **docs},
    uploader_name: {**runtime, **docs, "Info.json": json_bytes(info)},
}
manifest = {
    **CONFIG,
    "packaging_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT.parent, text=True).strip(),
    "runtime_files_sha256": {p: digest(data) for p, data in sorted(runtime.items())},
    "package_payloads_sha256": {name: {p: digest(data) for p, data in sorted(files.items())} for name, files in packages.items()},
    "note": "Payload maps exclude the embedded manifest itself. Outer ZIP hashes are in SHA256SUMS.txt.",
}
manifest_data = json_bytes(manifest)
(OUT / "release-manifest.json").write_bytes(manifest_data)
for name, files in packages.items():
    files["release-manifest.json"] = manifest_data
    with zipfile.ZipFile(OUT / name, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for path, data in sorted(files.items()):
            assert not path.startswith("/") and ".." not in pathlib.PurePosixPath(path).parts
            assert path not in ("InstallManifest.json", ".workshop.json", "mods.txt")
            entry = zipfile.ZipInfo(path, date_time=(2026, 10, 31, 0, 0, 0))
            entry.compress_type = zipfile.ZIP_DEFLATED
            entry.external_attr = 0o100644 << 16
            archive.writestr(entry, data)
    # Check every byte after ZIP round-trip, not only the presence of filenames.
    with zipfile.ZipFile(OUT / name) as archive:
        assert archive.testzip() is None
        assert set(archive.namelist()) == set(files)
        for path, data in files.items():
            assert archive.read(path) == data, path
    print(name, (OUT / name).stat().st_size, "bytes; all", len(files), "entries verified")
assets = [manual_name, uploader_name, "release-manifest.json"]
(OUT / "SHA256SUMS.txt").write_text("".join(digest(read(OUT / p)) + "  " + p + "\n" for p in assets), encoding="ascii", newline="\n")
print("Tested DLL SHA-256:", digest(dll))
print("Assets:", OUT)
