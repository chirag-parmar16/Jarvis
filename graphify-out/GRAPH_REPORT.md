# Graph Report - E:\Jarvis-MK37  (2026-04-29)

## Corpus Check
- 30 files · ~89,228 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 597 nodes · 1406 edges · 31 communities detected
- Extraction: 76% EXTRACTED · 24% INFERRED · 0% AMBIGUOUS · INFERRED: 331 edges (avg confidence: 0.79)
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

## God Nodes (most connected - your core abstractions)
1. `JarvisUI` - 31 edges
2. `_BrowserSession` - 30 edges
3. `browser_control()` - 29 edges
4. `get_os_system()` - 26 edges
5. `get_gemini_key()` - 24 edges
6. `computer_control()` - 22 edges
7. `_resolve_path()` - 20 edges
8. `_call_tool()` - 20 edges
9. `file_controller()` - 19 edges
10. `game_updater()` - 19 edges

## Surprising Connections (you probably didn't know these)
- `Gemini'nin ürettiği <ctrlXX> artefaktlarını ve kontrol karakterlerini temizler.` --uses--> `JarvisUI`  [INFERRED]
  E:\Jarvis-MK37\main.py → E:\Jarvis-MK37\ui.py
- `JarvisLive` --uses--> `JarvisUI`  [INFERRED]
  E:\Jarvis-MK37\main.py → E:\Jarvis-MK37\ui.py
- `JarvisLive` --uses--> `TaskPriority`  [INFERRED]
  E:\Jarvis-MK37\main.py → E:\Jarvis-MK37\agent\task_queue.py
- `main()` --calls--> `JarvisUI`  [INFERRED]
  E:\Jarvis-MK37\main.py → E:\Jarvis-MK37\ui.py
- `Gemini'nin ürettiği <ctrlXX> artefaktlarını ve kontrol karakterlerini temizler.` --uses--> `JarvisUI`  [INFERRED]
  E:\Jarvis-MK37\main.py → E:\Jarvis-MK37\ui.py

## Communities

### Community 0 - "Community 0"
Cohesion: 0.04
Nodes (33): main(), QPushButton, QWidget, BootHUDWidget, CameraWidget, ChatWidget, _detect_os(), FooterWidget (+25 more)

### Community 1 - "Community 1"
Cohesion: 0.05
Nodes (42): brightness_down(), brightness_up(), computer_settings(), dark_mode(), _detect_action(), full_screen(), _get_macos_wifi_interface(), go_back() (+34 more)

### Community 2 - "Community 2"
Cohesion: 0.08
Nodes (19): browser_control(), _BrowserSession, _detect_default_browser(), _find_exe_windows(), _find_opera_windows(), _firefox_profile_dir(), _log(), _normalize_url() (+11 more)

### Community 3 - "Community 3"
Cohesion: 0.08
Nodes (32): _build(), _clean_code(), code_helper(), _detect_intent(), _edit_action(), _explain_action(), _fix_code(), _get_gemini() (+24 more)

### Community 4 - "Community 4"
Cohesion: 0.07
Nodes (31): get_gemini_key(), Centralized getter for Gemini API Key., Enum, analyze_error(), ErrorDecision, generate_fix(), When decision is REPLAN and a fix suggestion exists,     generates a replacemen, Analyzes a failed step and returns a recovery decision.      Args:         st (+23 more)

### Community 5 - "Community 5"
Cohesion: 0.08
Nodes (23): _clean_transcript(), is_admin(), JarvisLive, _load_system_prompt(), Gemini'nin ürettiği <ctrlXX> artefaktlarını ve kontrol karakterlerini temizler., run_as_admin(), _all_entries(), _empty_memory() (+15 more)

### Community 6 - "Community 6"
Cohesion: 0.12
Nodes (41): get_os_system(), Centralized getter for OS system preference., _cancel_scheduled_update(), _click_button(), _click_first_profile_by_screenshot(), _ensure_steam_running(), _epic_manifests_path(), _find_best_drive() (+33 more)

### Community 7 - "Community 7"
Cohesion: 0.19
Nodes (31): copy_file(), create_file(), create_folder(), delete_file(), file_controller(), find_files(), _format_size(), _get_desktop() (+23 more)

### Community 8 - "Community 8"
Cohesion: 0.16
Nodes (25): _clear_field(), _click(), _clipboard_get(), _clipboard_paste(), computer_control(), _drag(), _focus_window(), _get_api_key() (+17 more)

### Community 9 - "Community 9"
Cohesion: 0.16
Nodes (20): get_os(), is_linux(), is_mac(), is_windows(), Returns: 'windows' | 'mac' | 'linux, _ask_for_url(), _extract_video_id(), _get_transcript() (+12 more)

### Community 10 - "Community 10"
Cohesion: 0.13
Nodes (17): _cleanup_legacy_json(), config_exists(), ensure_config_dir(), get_config_value(), is_configured(), Determine if the core configuration is complete., Check if the system is configured (either .env or legacy JSON exists)., Save Gemini API key to .env and remove from legacy JSON. (+9 more)

### Community 11 - "Community 11"
Cohesion: 0.25
Nodes (18): _build_project(), _classify_error(), dev_agent(), _fix_files(), _get_model(), _has_error(), _install_dependencies(), _is_rate_limit() (+10 more)

### Community 12 - "Community 12"
Cohesion: 0.32
Nodes (16): _clear_and_paste(), _desktop_send(), _get_os(), _open_app(), _open_browser_url(), _paste_text(), _require_pyautogui(), _resolve_platform() (+8 more)

### Community 13 - "Community 13"
Cohesion: 0.3
Nodes (14): _ask_gemini_for_desktop_action(), _build_sandbox(), clean_desktop(), desktop_control(), _execute_generated_code(), _get_api_key(), get_current_wallpaper(), _get_desktop() (+6 more)

### Community 14 - "Community 14"
Cohesion: 0.2
Nodes (5): Thread-safe signal to finish boot sequence., Thread-safe camera frame update., J.A.R.V.I.S - MARK XXXVII Computer Vision Interaction Module -----------------, Runs the camera in a background thread.     Pushes frames to JarvisUI for visual, VisionManager

### Community 15 - "Community 15"
Cohesion: 0.38
Nodes (8): _get_os(), reminder(), _sanitise(), _schedule_linux(), _schedule_mac(), _schedule_windows(), _scripts_dir(), _write_notify_script()

### Community 16 - "Community 16"
Cohesion: 0.67
Nodes (2): Scans assets/icons/ and generates icons.py with SVG_ICONS dictionary., update_icons()

### Community 17 - "Community 17"
Cohesion: 1.0
Nodes (0): 

### Community 18 - "Community 18"
Cohesion: 1.0
Nodes (0): 

### Community 19 - "Community 19"
Cohesion: 1.0
Nodes (0): 

### Community 20 - "Community 20"
Cohesion: 1.0
Nodes (1): JARVIS Digital Fragment Globe.     Hundreds of short, thin data arcs forming a v

### Community 21 - "Community 21"
Cohesion: 1.0
Nodes (1): Read identity fields from long-term memory.

### Community 22 - "Community 22"
Cohesion: 1.0
Nodes (1): Dispatch table for all computer control actions.      parameters keys (all opt

### Community 23 - "Community 23"
Cohesion: 1.0
Nodes (1): Verilen path _SAFE_ROOTS içinde mi? Değilse işlemi reddet.

### Community 24 - "Community 24"
Cohesion: 1.0
Nodes (1): Thin wrapper that works with whichever mediapipe API is available.

### Community 25 - "Community 25"
Cohesion: 1.0
Nodes (1): Returns list-of-landmark-lists (one per hand) or [].

### Community 26 - "Community 26"
Cohesion: 1.0
Nodes (1): Draw hand skeleton overlay (legacy API only).

### Community 27 - "Community 27"
Cohesion: 1.0
Nodes (1): Runs the camera in a background thread.     Pushes frames to JarvisUI and dispa

### Community 28 - "Community 28"
Cohesion: 1.0
Nodes (1): Returns the most recent camera frame as JPEG bytes, or None.

### Community 29 - "Community 29"
Cohesion: 1.0
Nodes (1): Require the same gesture for CONFIRM_FRAMES consecutive frames.         Also en

### Community 30 - "Community 30"
Cohesion: 1.0
Nodes (1): Create, start, and return a VisionManager.

## Knowledge Gaps
- **62 isolated node(s):** `J.A.R.V.I.S — MARK XXXVII UI Module — PyQt6 Enhanced Edition ─────────────────`, `Drop-in replacement for tk.Tk() — gives main.py a `.mainloop()` call.`, `True 3D Volumetric Orbital Globe with Y-axis rotation and perspective projection`, `Pre-generate the Multi-Axial 'Cage' geometry.`, `Circular HUD loader inspired by the 'ATLAS' reference image.     Features rotat` (+57 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Community 17`** (1 nodes): `icons.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 18`** (1 nodes): `setup.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 19`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 20`** (1 nodes): `JARVIS Digital Fragment Globe.     Hundreds of short, thin data arcs forming a v`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 21`** (1 nodes): `Read identity fields from long-term memory.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 22`** (1 nodes): `Dispatch table for all computer control actions.      parameters keys (all opt`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 23`** (1 nodes): `Verilen path _SAFE_ROOTS içinde mi? Değilse işlemi reddet.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 24`** (1 nodes): `Thin wrapper that works with whichever mediapipe API is available.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 25`** (1 nodes): `Returns list-of-landmark-lists (one per hand) or [].`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 26`** (1 nodes): `Draw hand skeleton overlay (legacy API only).`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 27`** (1 nodes): `Runs the camera in a background thread.     Pushes frames to JarvisUI and dispa`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 28`** (1 nodes): `Returns the most recent camera frame as JPEG bytes, or None.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 29`** (1 nodes): `Require the same gesture for CONFIRM_FRAMES consecutive frames.         Also en`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 30`** (1 nodes): `Create, start, and return a VisionManager.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `JarvisUI` connect `Community 3` to `Community 0`, `Community 4`, `Community 5`, `Community 8`, `Community 10`, `Community 14`?**
  _High betweenness centrality (0.127) - this node is a cross-community bridge._
- **Why does `load_svg_icon()` connect `Community 0` to `Community 7`?**
  _High betweenness centrality (0.085) - this node is a cross-community bridge._
- **Why does `browser_control()` connect `Community 2` to `Community 1`, `Community 4`, `Community 5`, `Community 7`, `Community 9`?**
  _High betweenness centrality (0.080) - this node is a cross-community bridge._
- **Are the 4 inferred relationships involving `JarvisUI` (e.g. with `JarvisLive` and `Gemini'nin ürettiği <ctrlXX> artefaktlarını ve kontrol karakterlerini temizler.`) actually correct?**
  _`JarvisUI` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Are the 3 inferred relationships involving `browser_control()` (e.g. with `._execute_tool()` and `_search_flights_browser()`) actually correct?**
  _`browser_control()` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Are the 23 inferred relationships involving `get_os_system()` (e.g. with `_get_os()` and `_save_to_desktop()`) actually correct?**
  _`get_os_system()` has 23 INFERRED edges - model-reasoned connections that need verification._
- **Are the 20 inferred relationships involving `get_gemini_key()` (e.g. with `.run()` and `_get_gemini()`) actually correct?**
  _`get_gemini_key()` has 20 INFERRED edges - model-reasoned connections that need verification._