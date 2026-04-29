# Graph Report - E:\Jarvis-MK37  (2026-04-29)

## Corpus Check
- 31 files · ~95,326 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 654 nodes · 1479 edges · 52 communities detected
- Extraction: 76% EXTRACTED · 24% INFERRED · 0% AMBIGUOUS · INFERRED: 353 edges (avg confidence: 0.79)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Community 0|Community 0]]
- [[_COMMUNITY_Community 1|Community 1]]
- [[_COMMUNITY_Community 2|Community 2]]
- [[_COMMUNITY_Community 3|Community 3]]
- [[_COMMUNITY_Community 4|Community 4]]
- [[_COMMUNITY_Community 5|Community 5]]
- [[_COMMUNITY_Community 6|Community 6]]
- [[_COMMUNITY_Community 7|Community 7]]
- [[_COMMUNITY_Community 8|Community 8]]
- [[_COMMUNITY_Community 9|Community 9]]
- [[_COMMUNITY_Community 10|Community 10]]
- [[_COMMUNITY_Community 11|Community 11]]
- [[_COMMUNITY_Community 12|Community 12]]
- [[_COMMUNITY_Community 13|Community 13]]
- [[_COMMUNITY_Community 14|Community 14]]
- [[_COMMUNITY_Community 15|Community 15]]
- [[_COMMUNITY_Community 16|Community 16]]
- [[_COMMUNITY_Community 17|Community 17]]
- [[_COMMUNITY_Community 18|Community 18]]
- [[_COMMUNITY_Community 19|Community 19]]
- [[_COMMUNITY_Community 20|Community 20]]
- [[_COMMUNITY_Community 21|Community 21]]
- [[_COMMUNITY_Community 22|Community 22]]
- [[_COMMUNITY_Community 23|Community 23]]
- [[_COMMUNITY_Community 24|Community 24]]
- [[_COMMUNITY_Community 25|Community 25]]
- [[_COMMUNITY_Community 26|Community 26]]
- [[_COMMUNITY_Community 27|Community 27]]
- [[_COMMUNITY_Community 28|Community 28]]
- [[_COMMUNITY_Community 29|Community 29]]
- [[_COMMUNITY_Community 30|Community 30]]
- [[_COMMUNITY_Community 31|Community 31]]
- [[_COMMUNITY_Community 32|Community 32]]
- [[_COMMUNITY_Community 33|Community 33]]
- [[_COMMUNITY_Community 34|Community 34]]
- [[_COMMUNITY_Community 35|Community 35]]
- [[_COMMUNITY_Community 36|Community 36]]
- [[_COMMUNITY_Community 37|Community 37]]
- [[_COMMUNITY_Community 38|Community 38]]
- [[_COMMUNITY_Community 39|Community 39]]
- [[_COMMUNITY_Community 40|Community 40]]
- [[_COMMUNITY_Community 41|Community 41]]
- [[_COMMUNITY_Community 42|Community 42]]
- [[_COMMUNITY_Community 43|Community 43]]
- [[_COMMUNITY_Community 44|Community 44]]
- [[_COMMUNITY_Community 45|Community 45]]
- [[_COMMUNITY_Community 46|Community 46]]
- [[_COMMUNITY_Community 47|Community 47]]
- [[_COMMUNITY_Community 48|Community 48]]
- [[_COMMUNITY_Community 49|Community 49]]
- [[_COMMUNITY_Community 50|Community 50]]
- [[_COMMUNITY_Community 51|Community 51]]

## God Nodes (most connected - your core abstractions)
1. `JarvisUI` - 37 edges
2. `_BrowserSession` - 30 edges
3. `browser_control()` - 29 edges
4. `get_os_system()` - 26 edges
5. `computer_control()` - 24 edges
6. `get_gemini_key()` - 24 edges
7. `_resolve_path()` - 20 edges
8. `_call_tool()` - 20 edges
9. `file_controller()` - 19 edges
10. `game_updater()` - 19 edges

## Surprising Connections (you probably didn't know these)
- `JarvisUI` --uses--> `Gemini'nin ürettiği <ctrlXX> artefaktlarını ve kontrol karakterlerini temizler.`  [INFERRED]
  E:\Jarvis-MK37\ui.py → E:\Jarvis-MK37\main.py
- `JarvisUI` --uses--> `Gemini'nin ürettiği <ctrlXX> artefaktlarını ve kontrol karakterlerini temizler.`  [INFERRED]
  E:\Jarvis-MK37\ui.py → E:\Jarvis-MK37\main.py
- `browser_control()` --calls--> `_search_flights_browser()`  [INFERRED]
  E:\Jarvis-MK37\actions\browser_control.py → E:\Jarvis-MK37\actions\flight_finder.py
- `browser_control()` --calls--> `_call_tool()`  [INFERRED]
  E:\Jarvis-MK37\actions\browser_control.py → E:\Jarvis-MK37\agent\executor.py
- `_get_gemini()` --calls--> `get_gemini_key()`  [INFERRED]
  E:\Jarvis-MK37\actions\code_helper.py → E:\Jarvis-MK37\memory\config_manager.py

## Communities

### Community 0 - "Community 0"
Cohesion: 0.04
Nodes (35): QPushButton, QWidget, BootHUDWidget, CameraWidget, ChatWidget, _detect_os(), FooterWidget, HeaderWidget (+27 more)

### Community 1 - "Community 1"
Cohesion: 0.04
Nodes (54): brightness_down(), brightness_up(), computer_settings(), dark_mode(), _detect_action(), full_screen(), _get_macos_wifi_interface(), go_back() (+46 more)

### Community 2 - "Community 2"
Cohesion: 0.04
Nodes (36): _clean_transcript(), is_admin(), JarvisLive, _load_system_prompt(), main(), Gemini'nin ürettiği <ctrlXX> artefaktlarını ve kontrol karakterlerini temizler., Gemini'nin ürettiği <ctrlXX> artefaktlarını ve kontrol karakterlerini temizler., Execute a tool locally and immediately from a UI action. (+28 more)

### Community 3 - "Community 3"
Cohesion: 0.06
Nodes (53): get_gemini_key(), Centralized getter for Gemini API Key., _ask_gemini_for_desktop_action(), _build_sandbox(), clean_desktop(), desktop_control(), _execute_generated_code(), _get_api_key() (+45 more)

### Community 4 - "Community 4"
Cohesion: 0.08
Nodes (19): browser_control(), _BrowserSession, _detect_default_browser(), _find_exe_windows(), _find_opera_windows(), _firefox_profile_dir(), _log(), _normalize_url() (+11 more)

### Community 5 - "Community 5"
Cohesion: 0.12
Nodes (41): get_os_system(), Centralized getter for OS system preference., _cancel_scheduled_update(), _click_button(), _click_first_profile_by_screenshot(), _ensure_steam_running(), _epic_manifests_path(), _find_best_drive() (+33 more)

### Community 6 - "Community 6"
Cohesion: 0.14
Nodes (28): _clear_field(), _click(), _clipboard_get(), _clipboard_paste(), computer_control(), _control_ui(), _drag(), _focus_window() (+20 more)

### Community 7 - "Community 7"
Cohesion: 0.24
Nodes (26): copy_file(), create_file(), create_folder(), delete_file(), file_controller(), find_files(), _format_size(), _get_desktop() (+18 more)

### Community 8 - "Community 8"
Cohesion: 0.24
Nodes (22): _build(), _clean_code(), code_helper(), _detect_intent(), _edit_action(), _explain_action(), _fix_code(), _get_gemini() (+14 more)

### Community 9 - "Community 9"
Cohesion: 0.13
Nodes (17): _cleanup_legacy_json(), config_exists(), ensure_config_dir(), get_config_value(), is_configured(), Determine if the core configuration is complete., Check if the system is configured (either .env or legacy JSON exists)., Save Gemini API key to .env and remove from legacy JSON. (+9 more)

### Community 10 - "Community 10"
Cohesion: 0.19
Nodes (17): get_os(), is_linux(), is_mac(), is_windows(), Returns: 'windows' | 'mac' | 'linux, _ask_for_url(), _extract_video_id(), _get_transcript() (+9 more)

### Community 11 - "Community 11"
Cohesion: 0.25
Nodes (18): _build_project(), _classify_error(), dev_agent(), _fix_files(), _get_model(), _has_error(), _install_dependencies(), _is_rate_limit() (+10 more)

### Community 12 - "Community 12"
Cohesion: 0.32
Nodes (16): _clear_and_paste(), _desktop_send(), _get_os(), _open_app(), _open_browser_url(), _paste_text(), _require_pyautogui(), _resolve_platform() (+8 more)

### Community 13 - "Community 13"
Cohesion: 0.32
Nodes (10): _all_entries(), _empty_memory(), forget(), load_memory(), _recursive_update(), remember(), save_memory(), _trim_to_limit() (+2 more)

### Community 14 - "Community 14"
Cohesion: 0.46
Nodes (6): get_cpu_usage(), get_disk_usage(), get_network_usage(), get_ram_usage(), get_system_summary(), get_top_processes()

### Community 15 - "Community 15"
Cohesion: 1.0
Nodes (0): 

### Community 16 - "Community 16"
Cohesion: 1.0
Nodes (0): 

### Community 17 - "Community 17"
Cohesion: 1.0
Nodes (0): 

### Community 18 - "Community 18"
Cohesion: 1.0
Nodes (1): Runs the camera in a background thread.     Pushes frames to JarvisUI for visual

### Community 19 - "Community 19"
Cohesion: 1.0
Nodes (1): Returns the most recent camera frame as JPEG bytes, or None.

### Community 20 - "Community 20"
Cohesion: 1.0
Nodes (1): Drop-in replacement for tk.Tk() — gives main.py a `.mainloop()` call.

### Community 21 - "Community 21"
Cohesion: 1.0
Nodes (1): True 3D Volumetric Orbital Globe with Y-axis rotation and perspective projection

### Community 22 - "Community 22"
Cohesion: 1.0
Nodes (1): Pre-generate the Multi-Axial 'Cage' geometry.

### Community 23 - "Community 23"
Cohesion: 1.0
Nodes (1): Circular HUD loader inspired by the 'ATLAS' reference image.     Features rotat

### Community 24 - "Community 24"
Cohesion: 1.0
Nodes (1): Audio-level bars that pulse when JARVIS is speaking.

### Community 25 - "Community 25"
Cohesion: 1.0
Nodes (1): Scrollable chat log with typewriter effect — mirrors original log_text.

### Community 26 - "Community 26"
Cohesion: 1.0
Nodes (1): Add a styled chat bubble to the layout.

### Community 27 - "Community 27"
Cohesion: 1.0
Nodes (1): Append text to the last bubble if it belongs to the same tag, or create new.

### Community 28 - "Community 28"
Cohesion: 1.0
Nodes (1): Update display with a new BGR frame (from OpenCV).

### Community 29 - "Community 29"
Cohesion: 1.0
Nodes (1): Complete PyQt6 implementation of J.A.R.V.I.S.     ─────────────────────────────

### Community 30 - "Community 30"
Cohesion: 1.0
Nodes (1): Thread-safe — callable from any thread.

### Community 31 - "Community 31"
Cohesion: 1.0
Nodes (1): Thread-safe signal to finish boot sequence.

### Community 32 - "Community 32"
Cohesion: 1.0
Nodes (1): Perform the actual UI transition on the main thread.

### Community 33 - "Community 33"
Cohesion: 1.0
Nodes (1): Thread-safe — adds a new log entry with typewriter effect.

### Community 34 - "Community 34"
Cohesion: 1.0
Nodes (1): Thread-safe — appends text to the last bubble immediately.

### Community 35 - "Community 35"
Cohesion: 1.0
Nodes (1): Handle global UI hotkeys.

### Community 36 - "Community 36"
Cohesion: 1.0
Nodes (1): Called by InputBarWidget.submitted signal.

### Community 37 - "Community 37"
Cohesion: 1.0
Nodes (1): Thread-safe camera frame update.

### Community 38 - "Community 38"
Cohesion: 1.0
Nodes (1): Thread-safe gesture callback — called by VisionManager.

### Community 39 - "Community 39"
Cohesion: 1.0
Nodes (1): Read identity fields from long-term memory.

### Community 40 - "Community 40"
Cohesion: 1.0
Nodes (1): Dispatch table for all computer control actions.      parameters keys (all opt

### Community 41 - "Community 41"
Cohesion: 1.0
Nodes (1): JARVIS Digital Fragment Globe.     Hundreds of short, thin data arcs forming a v

### Community 42 - "Community 42"
Cohesion: 1.0
Nodes (1): Read identity fields from long-term memory.

### Community 43 - "Community 43"
Cohesion: 1.0
Nodes (1): Dispatch table for all computer control actions.      parameters keys (all opt

### Community 44 - "Community 44"
Cohesion: 1.0
Nodes (1): Verilen path _SAFE_ROOTS içinde mi? Değilse işlemi reddet.

### Community 45 - "Community 45"
Cohesion: 1.0
Nodes (1): Thin wrapper that works with whichever mediapipe API is available.

### Community 46 - "Community 46"
Cohesion: 1.0
Nodes (1): Returns list-of-landmark-lists (one per hand) or [].

### Community 47 - "Community 47"
Cohesion: 1.0
Nodes (1): Draw hand skeleton overlay (legacy API only).

### Community 48 - "Community 48"
Cohesion: 1.0
Nodes (1): Runs the camera in a background thread.     Pushes frames to JarvisUI and dispa

### Community 49 - "Community 49"
Cohesion: 1.0
Nodes (1): Returns the most recent camera frame as JPEG bytes, or None.

### Community 50 - "Community 50"
Cohesion: 1.0
Nodes (1): Require the same gesture for CONFIRM_FRAMES consecutive frames.         Also en

### Community 51 - "Community 51"
Cohesion: 1.0
Nodes (1): Create, start, and return a VisionManager.

## Knowledge Gaps
- **93 isolated node(s):** `J.A.R.V.I.S — MARK XXXVII UI Module — PyQt6 Enhanced Edition ─────────────────`, `Drop-in replacement for tk.Tk() — gives main.py a `.mainloop()` call.`, `True 3D Volumetric Orbital Globe with Y-axis rotation and perspective projection`, `Pre-generate the Multi-Axial 'Cage' geometry.`, `Circular HUD loader inspired by the 'ATLAS' reference image.     Features rotat` (+88 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Community 15`** (1 nodes): `icons.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 16`** (1 nodes): `setup.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 17`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 18`** (1 nodes): `Runs the camera in a background thread.     Pushes frames to JarvisUI for visual`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 19`** (1 nodes): `Returns the most recent camera frame as JPEG bytes, or None.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 20`** (1 nodes): `Drop-in replacement for tk.Tk() — gives main.py a `.mainloop()` call.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 21`** (1 nodes): `True 3D Volumetric Orbital Globe with Y-axis rotation and perspective projection`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 22`** (1 nodes): `Pre-generate the Multi-Axial 'Cage' geometry.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 23`** (1 nodes): `Circular HUD loader inspired by the 'ATLAS' reference image.     Features rotat`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 24`** (1 nodes): `Audio-level bars that pulse when JARVIS is speaking.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 25`** (1 nodes): `Scrollable chat log with typewriter effect — mirrors original log_text.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 26`** (1 nodes): `Add a styled chat bubble to the layout.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 27`** (1 nodes): `Append text to the last bubble if it belongs to the same tag, or create new.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 28`** (1 nodes): `Update display with a new BGR frame (from OpenCV).`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 29`** (1 nodes): `Complete PyQt6 implementation of J.A.R.V.I.S.     ─────────────────────────────`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 30`** (1 nodes): `Thread-safe — callable from any thread.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 31`** (1 nodes): `Thread-safe signal to finish boot sequence.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 32`** (1 nodes): `Perform the actual UI transition on the main thread.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 33`** (1 nodes): `Thread-safe — adds a new log entry with typewriter effect.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 34`** (1 nodes): `Thread-safe — appends text to the last bubble immediately.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 35`** (1 nodes): `Handle global UI hotkeys.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 36`** (1 nodes): `Called by InputBarWidget.submitted signal.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 37`** (1 nodes): `Thread-safe camera frame update.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 38`** (1 nodes): `Thread-safe gesture callback — called by VisionManager.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 39`** (1 nodes): `Read identity fields from long-term memory.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 40`** (1 nodes): `Dispatch table for all computer control actions.      parameters keys (all opt`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 41`** (1 nodes): `JARVIS Digital Fragment Globe.     Hundreds of short, thin data arcs forming a v`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 42`** (1 nodes): `Read identity fields from long-term memory.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 43`** (1 nodes): `Dispatch table for all computer control actions.      parameters keys (all opt`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 44`** (1 nodes): `Verilen path _SAFE_ROOTS içinde mi? Değilse işlemi reddet.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 45`** (1 nodes): `Thin wrapper that works with whichever mediapipe API is available.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 46`** (1 nodes): `Returns list-of-landmark-lists (one per hand) or [].`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 47`** (1 nodes): `Draw hand skeleton overlay (legacy API only).`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 48`** (1 nodes): `Runs the camera in a background thread.     Pushes frames to JarvisUI and dispa`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 49`** (1 nodes): `Returns the most recent camera frame as JPEG bytes, or None.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 50`** (1 nodes): `Require the same gesture for CONFIRM_FRAMES consecutive frames.         Also en`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 51`** (1 nodes): `Create, start, and return a VisionManager.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `JarvisUI` connect `Community 2` to `Community 0`, `Community 9`, `Community 6`?**
  _High betweenness centrality (0.129) - this node is a cross-community bridge._
- **Why does `load_svg_icon()` connect `Community 0` to `Community 3`?**
  _High betweenness centrality (0.072) - this node is a cross-community bridge._
- **Why does `browser_control()` connect `Community 4` to `Community 2`, `Community 1`, `Community 10`, `Community 3`?**
  _High betweenness centrality (0.069) - this node is a cross-community bridge._
- **Are the 7 inferred relationships involving `JarvisUI` (e.g. with `JarvisLive` and `Gemini'nin ürettiği <ctrlXX> artefaktlarını ve kontrol karakterlerini temizler.`) actually correct?**
  _`JarvisUI` has 7 INFERRED edges - model-reasoned connections that need verification._
- **Are the 3 inferred relationships involving `browser_control()` (e.g. with `._execute_tool()` and `_search_flights_browser()`) actually correct?**
  _`browser_control()` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Are the 23 inferred relationships involving `get_os_system()` (e.g. with `_get_os()` and `_save_to_desktop()`) actually correct?**
  _`get_os_system()` has 23 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `computer_control()` (e.g. with `._execute_tool()` and `.get()`) actually correct?**
  _`computer_control()` has 4 INFERRED edges - model-reasoned connections that need verification._