# Native compatibility work in progress

Status: SDK access blocked; no repaired binary has been compiled or deployed.

`reference/` contains the unchanged upstream candidate, not our completed fix:
- Repository: https://github.com/IanMoroney/palworld-integrated-storage
- Commit: `6a3de750da7d416a2b02d1852c3dac27d21a6b8b`
- PR: https://github.com/Sarfflow/palworld-integrated-storage/pull/5
- `dllmain.cpp` SHA-256: `6e60aa41e6f5ebc29fc0f55c86ed0bd9bbc309275c0ebd1e279dfb870d5f1d93`
- License: reference/LICENSE (MIT, Sarfflow)
- xmake.lua is the original target definition; its `src/dllmain.cpp` path assumes the upstream build layout.

Local build inputs (ignored by Git):
- build/RE-UE4SS: checked out at installed UE4SS revision 2281fa31.
- Required deps/first/Unreal commit: 1cb4c98746f03dfcbf2f0394b59dfec0c9f83a04.
- Authenticated requests for Re-UE4SS/UEPseudo and EpicGames/UnrealEngine returned HTTP 404.
- Official UE4SS-Palworld_zDev.zip contains DLL/PDB and runtime files, not the required Unreal headers.
- Visual Studio 2022 Community, MSVC 14.44.35207 is installed.
- build/minhook was fetched for feasibility investigation; the upstream target uses PolyHook2. No MinHook changes were made.

Resume after Epic/GitHub authorization:
1. Verify authenticated access to Re-UE4SS/UEPseudo; do not assume account linking alone suffices.
2. Fetch the exact submodule commit using authenticated Git. Obtain the remaining declared build dependencies.
3. Review the candidate's native discovery heuristics, game-thread safety, raw offsets, lifecycle handling, stale cached counts and chest coverage before adapting it.
4. Build against the installed UE4SS revision and validate imports, hook resolution and failure handling.
5. Back up installed ziyuan, deploy only a built and checked candidate, avoid running two competing storage implementations.
6. Have the user validate all-camp/all-item behavior, UI counts and real consumption.

Account linking instructions: https://www.unrealengine.com/ue-on-github/
No installed game/mod files were changed in this build attempt.
