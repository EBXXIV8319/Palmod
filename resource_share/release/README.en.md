# Resource Share — 3.7.1-local-test2 (prerelease)

Palworld **1.0.5.102999**, Windows x64, local single-player. Requires **UE4SS Experimental (Palworld) 2281fa31**, package `UE4SSExperimentalPW`. The loader is not bundled. Other UE4SS ABIs are unverified.

Allows same-guild bases to use materials stored at other bases, with actual consumption from source storage. There is no fixed item whitelist or base-count limit in the implementation.

## Verified and pending

User-confirmed on 2026-10-31: A held 31 stone, the player held none, and B had no chests or stone. Building at B succeeded and A's stone decreased by the recipe cost.

Other items/storage variants, 3+ bases, unvisited distant bases, crafting/production, insufficient resources, chest creation/removal, save reload, Quick Stack, Item Retrieval Device and different guilds remain untested. Multiplayer/dedicated-server behavior is unverified; remote-client display hooks and server install rules are not enabled in this package.

## Install the Win64 ZIP

1. Close the game and back up an existing `ziyuan` mod. Disable/unsubscribe and uninstall the old Workshop package first to prevent it overwriting this package. Do not run multiple IntegratedStorage implementations together.
2. Extract the **Win64.zip** and merge its `Mods` directory into the Palworld game directory. Result: `Mods/NativeMods/UE4SS/Mods/ziyuan/dlls/main.dll`.
3. In the existing `Mods/NativeMods/UE4SS/Mods/mods.txt`, add/enable exactly one `ziyuan : 1` line before Keybinds. Preserve other entries; no global mods.txt is bundled.
4. Restart completely, enter the single-player save and wait about 10 seconds. Check displayed resources and actual source consumption. Do not hot-reload.

The included main.lua is only a launcher message; replace the old Lua implementation when upgrading. Back up custom config before extraction. The default discovery interval is 2000 ms; counts may take around two seconds to refresh.

The **ModUploader.zip** is a separate flat content package with root Info.json, complete install targets and a loader dependency. It is not a game-root overlay. No Steam Workshop item was created or updated by this GitHub release. Its Uploader installation/upload has not been play-tested.

To uninstall the manual installation, close the game, disable/remove the ziyuan entry and move away its mod folder. Restore your backup to roll back. Let the official loader uninstall packages installed through it.

Log: `Mods/NativeMods/UE4SS/UE4SS.log`. Look for four `hooked=true` entries, the test2 native-hooks message, and `SRV discover` after loading a save. Report a minimal reproduction and relevant ISGATE excerpts at https://github.com/EBXXIV8319/Palmod/issues . Verify downloads using SHA256SUMS.txt.

Credits: Sarfflow (original), IanMoroney (upstream 1.0.5 adaptation), EBXXIV8319 (local repair/release). Original Chinese distribution credited 梅川库梓. MIT and third-party licenses are included. See NOTICE.md and the Chinese guide for details and primary documentation links.
