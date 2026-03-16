# Mac Installation Instructions for Milo's Story

## If you see "MilosStory.app is damaged and can't be opened"

This is a common macOS security feature (Gatekeeper) that blocks unsigned apps. Here's how to fix it:

### Method 1: Right-Click and Open (Easiest)

1. **Right-click** (or Control+Click) on `MilosStory.app`
2. Select **"Open"** from the context menu
3. Click **"Open"** in the security dialog that appears
4. The app will now run normally, and you can double-click it in the future

### Method 2: Remove Quarantine Attribute (For Advanced Users)

If Method 1 doesn't work, open Terminal and run:

```bash
xattr -dr com.apple.quarantine /path/to/MilosStory.app
```

Replace `/path/to/MilosStory.app` with the actual path to the app.

For example, if it's in your Downloads folder:
```bash
xattr -dr com.apple.quarantine ~/Downloads/MilosStory.app
```

Then try opening the app again.

### Method 3: System Preferences (If Still Blocked)

1. Go to **System Preferences** (or **System Settings** on newer macOS)
2. Click **Security & Privacy** (or **Privacy & Security**)
3. Under the **General** tab, you should see a message about MilosStory.app being blocked
4. Click **"Open Anyway"**

## Why This Happens

macOS Gatekeeper protects your Mac by blocking apps that aren't signed with an Apple Developer certificate. Since this app is distributed independently, it doesn't have Apple's signature. The methods above allow you to bypass this security check for this specific app.

## After First Launch

Once you've opened the app using one of the methods above, macOS will remember your choice and you can double-click it normally in the future.
