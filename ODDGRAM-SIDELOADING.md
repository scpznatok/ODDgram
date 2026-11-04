# ODDgram sideload test build

This branch imports Swiftgram 13.1.1 at commit `9b35b732e4527e40f0adbb03f4aa22785ddfa74c`.
The previous ODDgram tree remains on `master`; this baseline does not automatically include all old custom changes.

## Build and install

Run **ODDgram sideload build** from GitHub Actions on this branch. If the build succeeds,
download the `ODDgram-unsigned-ipa` artifact. It is built with placeholder signing:
sign it with your own valid certificate and provisioning profile before installing.
It is not a ready-to-run signed app.

The app tries the normal shared App Group first. If it is unavailable, it uses a
private Application Support directory and remembers that selection. In private
container mode, extensions cannot access the app's data. Sharing, widgets and
notification features may therefore be unavailable. A valid notification
entitlement and service are also required for push notifications.

Changing bundle identifiers, teams, certificates or signing entitlements can
change which Keychain entries or shared containers are accessible. A reinstall
can erase local app data, including secret chats. Do not delete an existing
installation to test unless you accept that loss. The private-container fallback
has not been verified on a physical device.

For a black screen, record the iOS version, installation method, signer settings,
whether extensions were removed, whether the app is a fresh install or an update,
and any iOS crash report (Settings > Privacy & Security > Analytics & Improvements
> Analytics Data). Do not share certificates, provisioning profiles, API hashes,
phone numbers, account sessions or other private data.
