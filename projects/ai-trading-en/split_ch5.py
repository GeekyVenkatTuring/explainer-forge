#!/usr/bin/env python3
"""Split Part 5 (26 beats) into two half-chapters ch5a + ch5b so each renders with a
small temp footprint and short duration (the big single ch5 render kept exhausting disk).
Per-beat WAVs are cached in assets/, so core.build just re-concats — no re-TTS."""
import aitcore as core
import importlib.util, sys
spec = importlib.util.spec_from_file_location("ch5_build", "ch5_build.py")
m = importlib.util.module_from_spec(spec); sys.modules["ch5_build"] = m; spec.loader.exec_module(m)

segs = m.SEGMENTS
half = len(segs) // 2               # 13 / 13
core.build("ch5a", segs[:half])
core.build("ch5b", segs[half:])
