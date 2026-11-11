#!/usr/bin/env python3
"""Generate WinGet (Windows Package Manager) community repository manifests.

Produces valid multi-file manifests (version, installer, defaultLocale) conforming to
WinGet manifest specification 1.6.0 for submission to microsoft/winget-pkgs.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import urllib.request
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

DEFAULT_PACKAGE_ID = "carlkidcrypto.PurpleAirAPI"
DEFAULT_PACKAGE_NAME = "PurpleAir API"
DEFAULT_PUBLISHER = "carlkidcrypto"
DEFAULT_PUBLISHER_URL = "https://github.com/carlkidcrypto"
MANIFEST_VERSION = "1.6.0"


def _read_current_version() -> str:
    # Check python/setup.cfg first
    setup_cfg = REPO_ROOT / "python" / "setup.cfg"
    if setup_cfg.is_file():
        text = setup_cfg.read_text(encoding="utf-8")
        for line in text.splitlines():
            if line.strip().startswith("version") and "=" in line:
                raw = line.split("=", 1)[1].strip()
                if "a" in raw and "-" not in raw:
                    prefix, num = raw.split("a", 1)
                    return f"{prefix}-alpha.{num}"
                return raw

    # Check meson.build
    meson_file = REPO_ROOT / "meson.build"
    if meson_file.is_file():
        text = meson_file.read_text(encoding="utf-8")
        match = re.search(r"version\s*:\s*['\"]([^'\"]+)['\"]", text)
        if match:
            raw = match.group(1).strip()
            if "a" in raw and "-" not in raw:
                prefix, num = raw.split("a", 1)
                return f"{prefix}-alpha.{num}"
            return raw

    # Check csharp project
    csproj = REPO_ROOT / "csharp" / "PurpleAirAPI.csproj"
    if csproj.is_file():
        text = csproj.read_text(encoding="utf-8")
        match = re.search(r"<Version>([^<]+)</Version>", text)
        if match:
            return match.group(1).strip()

    return "2026.11.11-alpha.1"


def get_canonical_manifest_dir(
    package_id: str,
    package_version: str,
    out_dir: Path,
) -> Path:
    """Return canonical WinGet directory: manifests/{first-letter}/{Publisher}/{AppName}/{Version}/"""
    if not re.fullmatch(r"^[a-zA-Z0-9_\-]+(?:\.[a-zA-Z0-9_\-]+)+$", package_id):
        raise ValueError(f"Invalid package_id format: {package_id}")
    if not re.fullmatch(r"^[0-9a-zA-Z\.\-_]+$", package_version):
        raise ValueError(f"Invalid package_version format: {package_version}")

    parts = package_id.split(".", 1)
    publisher = parts[0]
    app_name = parts[1] if len(parts) > 1 else package_id
    first_letter = publisher[0].lower()

    base_out = out_dir.resolve()
    if base_out.name.lower() == "manifests":
        target = base_out / first_letter / publisher / app_name / package_version
    else:
        target = (
            base_out
            / "manifests"
            / first_letter
            / publisher
            / app_name
            / package_version
        )

    target_resolved = target.resolve()
    if not target_resolved.is_relative_to(base_out):
        raise ValueError(f"Path traversal detected in manifest directory: {target}")
    return target_resolved


def compute_sha256(path_or_url: str) -> str:
    """Compute the lowercase SHA256 hex digest of a local file or remote URL."""
    h = hashlib.sha256()

    if path_or_url.startswith("http://") or path_or_url.startswith("https://"):
        try:
            req = urllib.request.Request(
                path_or_url, headers={"User-Agent": "winget-manifest-gen/1.0"}
            )
            with urllib.request.urlopen(req) as resp:
                while chunk := resp.read(65536):
                    h.update(chunk)
            return h.hexdigest().lower()
        except Exception as exc:
            print(
                f"Warning: Could not fetch remote URL for SHA256 ({exc}); using zero digest."
            )
            return "0000000000000000000000000000000000000000000000000000000000000000"

    safe_name = Path(path_or_url).name
    candidate_paths = [
        (REPO_ROOT / path_or_url).resolve(),
        (REPO_ROOT / "dist" / safe_name).resolve(),
    ]
    for p in candidate_paths:
        if p.is_file() and p.is_relative_to(REPO_ROOT.resolve()):
            with open(p, "rb") as f:
                for chunk in iter(lambda: f.read(65536), b""):
                    h.update(chunk)
            return h.hexdigest().lower()

    raise FileNotFoundError(f"Cannot compute hash for: {path_or_url}")


def generate_manifests(
    package_id: str = DEFAULT_PACKAGE_ID,
    package_version: str = "",
    installer_url: str = "",
    installer_sha256: str = "",
    out_dir: Path | None = None,
    architecture: str = "x64",
    installer_type: str = "auto",
) -> dict[str, Path]:
    """Generate the 3 canonical WinGet manifest YAML files."""
    if not package_version:
        package_version = _read_current_version()

    if out_dir is None:
        out_dir = REPO_ROOT / "dist-winget"

    dest = get_canonical_manifest_dir(package_id, package_version, out_dir)
    dest.mkdir(parents=True, exist_ok=True)

    if not installer_url:
        installer_url = (
            f"https://github.com/carlkidcrypto/purpleair_api/releases/download/"
            f"v{package_version}/PurpleAirAPI-Windows-x64-Setup.exe"
        )

    resolved_type = (installer_type or "auto").strip().lower()
    if resolved_type in ("", "auto"):
        resolved_type = "zip" if installer_url.lower().endswith(".zip") else "inno"

    if not installer_sha256:
        installer_sha256 = (
            "0000000000000000000000000000000000000000000000000000000000000000"
            if not installer_url.startswith("http")
            and not Path(installer_url).is_file()
            else compute_sha256(installer_url)
        )

    version_yaml = (
        f"PackageIdentifier: {package_id}\n"
        f"PackageVersion: {package_version}\n"
        "DefaultLocale: en-US\n"
        "ManifestType: version\n"
        f"ManifestVersion: {MANIFEST_VERSION}\n"
    )

    locale_yaml = (
        f"PackageIdentifier: {package_id}\n"
        f"PackageVersion: {package_version}\n"
        "PackageLocale: en-US\n"
        f"Publisher: {DEFAULT_PUBLISHER}\n"
        f"PublisherUrl: {DEFAULT_PUBLISHER_URL}\n"
        "PublisherSupportUrl: https://github.com/carlkidcrypto/purpleair_api/issues\n"
        f"Author: {DEFAULT_PUBLISHER}\n"
        f"PackageName: {DEFAULT_PACKAGE_NAME}\n"
        "PackageUrl: https://carlkidcrypto.github.io/purpleair_api/\n"
        "License: MIT\n"
        "LicenseUrl: https://raw.githubusercontent.com/carlkidcrypto/purpleair_api/main/LICENSE\n"
        "Copyright: Copyright (c) 2023-2026 carlkidcrypto\n"
        "CopyrightUrl: https://raw.githubusercontent.com/carlkidcrypto/purpleair_api/main/LICENSE\n"
        "ShortDescription: PurpleAir API multi-language client library with C++ backend.\n"
        "Description: |-\n"
        "  PurpleAir API provides high-performance access to PurpleAir sensors and\n"
        "  air quality telemetry data with a unified C++ backend and multi-language\n"
        "  bindings for Python, JavaScript, C#, and Go.\n"
        "Moniker: purpleair-api\n"
        "Tags:\n"
        "  - purpleair\n"
        "  - air-quality\n"
        "  - sensor\n"
        "  - telemetry\n"
        "  - iot\n"
        "ManifestType: defaultLocale\n"
        f"ManifestVersion: {MANIFEST_VERSION}\n"
    )

    if resolved_type == "inno":
        installer_yaml = (
            f"PackageIdentifier: {package_id}\n"
            f"PackageVersion: {package_version}\n"
            "InstallerLocale: en-US\n"
            "Platform:\n"
            "  - Windows.Desktop\n"
            "MinimumOSVersion: 10.0.0.0\n"
            "InstallerType: inno\n"
            "Scope: user\n"
            "InstallModes:\n"
            "  - interactive\n"
            "  - silent\n"
            "  - silentWithProgress\n"
            "InstallerSwitches:\n"
            "  Silent: /VERYSILENT /SUPPRESSMSGBOXES /NORESTART /SP-\n"
            "  SilentWithProgress: /SILENT /SUPPRESSMSGBOXES /NORESTART /SP-\n"
            "UpgradeBehavior: install\n"
            "AppsAndFeaturesEntries:\n"
            "  - DisplayName: PurpleAir API\n"
            "    Publisher: carlkidcrypto\n"
            f"    DisplayVersion: {package_version}\n"
            "    ProductCode: '{A2B4C6D8-1E3F-4A5B-8C7D-9E0F1A2B3C4D}_is1'\n"
            "Installers:\n"
            f"  - Architecture: {architecture}\n"
            f"    InstallerUrl: {installer_url}\n"
            f"    InstallerSha256: {installer_sha256.upper()}\n"
            "ManifestType: installer\n"
            f"ManifestVersion: {MANIFEST_VERSION}\n"
        )
    else:
        installer_yaml = (
            f"PackageIdentifier: {package_id}\n"
            f"PackageVersion: {package_version}\n"
            "InstallerLocale: en-US\n"
            "Platform:\n"
            "  - Windows.Desktop\n"
            "MinimumOSVersion: 10.0.0.0\n"
            "InstallerType: zip\n"
            "NestedInstallerType: portable\n"
            "NestedInstallerFiles:\n"
            "  - RelativeFilePath: PurpleAirAPI.dll\n"
            "    PortableCommandAlias: PurpleAirAPI\n"
            "Installers:\n"
            f"  - Architecture: {architecture}\n"
            f"    InstallerUrl: {installer_url}\n"
            f"    InstallerSha256: {installer_sha256.upper()}\n"
            "ManifestType: installer\n"
            f"ManifestVersion: {MANIFEST_VERSION}\n"
        )

    target_dir = dest.resolve()
    version_path = (target_dir / f"{package_id}.yaml").resolve()
    locale_path = (target_dir / f"{package_id}.locale.en-US.yaml").resolve()
    installer_path = (target_dir / f"{package_id}.installer.yaml").resolve()

    for p in (version_path, locale_path, installer_path):
        if not p.is_relative_to(target_dir):
            raise ValueError(f"Path traversal detected in manifest output file: {p}")

    version_path.write_text(version_yaml, encoding="utf-8")
    locale_path.write_text(locale_yaml, encoding="utf-8")
    installer_path.write_text(installer_yaml, encoding="utf-8")

    return {
        "version": version_path,
        "locale": locale_path,
        "installer": installer_path,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Generate WinGet manifests.")
    parser.add_argument("--package-id", default=DEFAULT_PACKAGE_ID)
    parser.add_argument("--version", default="")
    parser.add_argument(
        "--installer-url",
        default="",
        help="Download URL of installer executable or portable zip",
    )
    parser.add_argument("--sha256", default="")
    parser.add_argument("--out-dir", default=str(REPO_ROOT / "dist-winget"))
    parser.add_argument("--arch", default="x64")
    parser.add_argument(
        "--installer-type",
        default="auto",
        choices=["auto", "inno", "zip"],
        help="Installer type: inno (default for .exe) or zip (for portable .zip)",
    )
    args = parser.parse_args(argv)

    ver = args.version or _read_current_version()
    installer_url = args.installer_url or (
        f"https://github.com/carlkidcrypto/purpleair_api/releases/download/"
        f"v{ver}/PurpleAirAPI-Windows-x64-Setup.exe"
    )

    sha = args.sha256 or (
        "0000000000000000000000000000000000000000000000000000000000000000"
        if not installer_url.startswith("http") and not Path(installer_url).is_file()
        else compute_sha256(installer_url)
    )

    out = Path(args.out_dir)
    res = generate_manifests(
        package_id=args.package_id,
        package_version=ver,
        installer_url=installer_url,
        installer_sha256=sha,
        out_dir=out,
        architecture=args.arch,
        installer_type=args.installer_type,
    )

    print(f"Generated WinGet manifests for {args.package_id} v{ver}:")
    for k, p in res.items():
        print(f"  {k}: {p}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
