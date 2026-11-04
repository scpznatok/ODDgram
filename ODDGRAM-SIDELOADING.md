# ODDgram sideload test build

This branch imports Swiftgram 13.1.1 at commit `9b35b732e4527e40f0adbb03f4aa22785ddfa74c`.
The previous ODDgram tree remains on `master`; this baseline does not automatically include all old custom changes.

## Build and install

Run **ODDgram sideload build** from GitHub Actions on this branch. If the build succeeds,
download the `ODDgram-unsigned-ipa` artifact. It is built with placeholder signing:
sign it with your own valid certificate and provisioning profile before installing.
It is not a ready-to-run signed app.

The app requires its shared App Group. The app and each extension must be signed
with matching, authorized App Group entitlements and provisioning profiles.
ODDgram does not silently move account data to a separate private container.
The Swiftgram settings page reports whether the shared container is accessible;
this alone does not establish that extensions or push notifications work.
Push notifications additionally require the appropriate entitlement and service.

Changing bundle identifiers, teams, certificates or signing entitlements can
change which Keychain entries or shared containers are accessible. A reinstall
can erase local app data, including secret chats. Do not delete an existing
installation to test unless you accept that loss. The App Group configuration has not been verified on a physical device.

For a black screen, record the iOS version, installation method, signer settings,
whether extensions were removed, whether the app is a fresh install or an update,
and any iOS crash report (Settings > Privacy & Security > Analytics & Improvements
> Analytics Data). Do not share certificates, provisioning profiles, API hashes,
phone numbers, account sessions or other private data.
