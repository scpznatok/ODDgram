#!/usr/bin/env python3
"""Renew the repository's self-signed, non-distribution CI profiles.

These placeholders are used only to package an IPA. They are not valid Apple
profiles; the IPA must be signed again using the installer's real credentials.
"""
import datetime
import pathlib
import plistlib
import subprocess
import tempfile

ROOT = pathlib.Path("build-system/fake-codesigning")
PROFILES = ROOT / "profiles"
P12 = ROOT / "certs" / "SelfSigned.p12"

def run(*args, **kwargs):
    return subprocess.run(args, check=True, **kwargs)

def main():
    profiles = sorted(PROFILES.glob("*.mobileprovision"))
    if not profiles:
        raise SystemExit("No placeholder provisioning profiles found")
    with tempfile.TemporaryDirectory() as tmp:
        pem = pathlib.Path(tmp) / "placeholder.pem"
        run("openssl", "pkcs12", "-legacy", "-in", str(P12),
            "-nodes", "-passin", "pass:", "-out", str(pem))
        for profile in profiles:
            decoded = run("security", "cms", "-D", "-i", str(profile), stdout=subprocess.PIPE).stdout
            data = plistlib.loads(decoded)
            data["ExpirationDate"] = datetime.datetime.utcnow() + datetime.timedelta(days=365)
            xml = pathlib.Path(tmp) / "profile.plist"
            xml.write_bytes(plistlib.dumps(data))
            signed = pathlib.Path(tmp) / "profile.mobileprovision"
            run("openssl", "smime", "-sign", "-binary", "-nodetach",
                "-in", str(xml), "-out", str(signed), "-outform", "DER",
                "-signer", str(pem), "-inkey", str(pem))
            # Verify the renewed container can be decoded before replacing it.
            decoded_again = run("security", "cms", "-D", "-i", str(signed),
                                stdout=subprocess.PIPE).stdout
            if plistlib.loads(decoded_again)["ExpirationDate"] != data["ExpirationDate"].replace(microsecond=0):
                raise RuntimeError("Profile verification failed: " + profile.name)
            profile.write_bytes(signed.read_bytes())
            print("Renewed CI placeholder:", profile.name)

if __name__ == "__main__":
    main()
