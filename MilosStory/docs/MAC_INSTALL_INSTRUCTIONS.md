# Mac Installation Instructions for Milo's Story

## If macOS says the app is "damaged" or "may contain malware"

That message often means **Gatekeeper** blocked the app (especially after download), not that the files are actually corrupt. If you click **Cancel**, newer macOS versions may **not** show **Open Anyway** under Privacy & Security — that is expected.

### Fix that always works: Terminal (`xattr`)

1. Open **Terminal** (Spotlight: Cmd+Space, type `Terminal`).
2. Run (change the path if the app is not in Downloads):

```bash
xattr -cr ~/Downloads/MilosStory.app
open ~/Downloads/MilosStory.app
```

**Tip:** Type `xattr -cr ` with a space at the end, then **drag** `MilosStory.app` from Finder into the Terminal window to paste the full path, then press Enter.

3. If a dialog appears, click **Open**, not Cancel.

`xattr -cr` removes **quarantine** and other extended attributes that trigger the false "damaged" warning.

### Right-click Open

1. **Control+click** (or right-click) `MilosStory.app`.
2. Choose **Open**.
3. Click **Open** in the dialog.

### Privacy & Security ("Open Anyway")

This only appears in some cases **after** macOS has recorded a block:

1. Open **System Settings** → **Privacy & Security**.
2. Scroll down — look for a message about **MilosStory** being blocked.
3. Click **Open Anyway** if it appears.

If it **never** appears (common after you only pressed **Cancel**), use the **Terminal `xattr`** steps above.

## Where saves and options are stored

When running the **built app** (not from source):

`~/Library/Application Support/MilosStory/`

## For developers: rebuild with a clean signature

From the `MilosStory` folder:

```bash
./scripts/build_mac.sh
```

The build runs `scripts/macos_sign_app.sh` to strip `._*` files, clear xattrs, remove broken signatures, and ad-hoc sign again.

To fix an existing `.app` someone sent you:

```bash
./scripts/fix_mac_app.sh /path/to/MilosStory.app
```

## Apple Developer notarization

To remove **all** Gatekeeper prompts for strangers downloading the app, you need an **Apple Developer** account and **notarization**. Ad-hoc signing (what this project uses) is fine for local use and friends if they run `xattr` once.
