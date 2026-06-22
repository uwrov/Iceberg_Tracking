Terminal tool for MATE ROV 2026 Explorer Task 2.2 — iceberg tracking. Pass iceberg position, heading, keel depth, and all four platform locations from your map/data sheet. The calculator prints surface and subsea threat levels for each platform.

Python 3.6+ (No pip libs used)

For coordinates given in DMS x°y°z, convert to decimal degrees:
- Ex: 45°30'15"N → 45 + (30/60) + (15/3600) = 45.5042°N
Use the DMS to decimal converter if needed, separating each subpart by a comma (ex: "45,30,15"). 
Currently, does two in one requiring the user the separate the two coordinates with a space 

map_rendering (CLI input, matplotlib output)

Follow the provided prompts. The platforms are hardcoded, so only need to input iceberg.

Will output two plots, one for platforms, and one for subsea assets corresponding to the platforms.








(DEPRECATED)
threat_calculator.py (Command line I/O)
Usage: 
Being with the iceberg specifications:
(separate each argument with a comma)
--lat 
--lon
--heading
--keel

followed by four platform specifications:
--platform "name",latitude,longitude,ocean_depth_m

Ex of arguments.  --lat 47.39 --lon -48.37, --heading 158 --keel 99 --platform hibernia,46.75,-48.7819,-78 --platform searose,46.78,48.146,-107 --platform terranova,46.4,-48.4,-91 --platform hebron,46.54,-48.518,-93

All arguments are required. Provide exactly four --platform entries.

Each --platform value is name,latitude,longitude,ocean_depth_m. Ocean depth may be positive or negative (as on some map sheets); negative values are converted to positive meters.

Approach:

1. Perpendicular distance (nautical miles) from each platform to the iceberg path line, using the rule that 1 minute of latitude = 1 nautical mile.
2. Surface threat:
   - Keel ≥ 110% of water depth → green (grounds before platform)
   - Track distance > 10 nm → green
   - 5–10 nm → yellow
   - < 5 nm → red
3. Subsea threat (only evaluated within 25 nm)
   - Keel ≥ 110% of water depth → green
   - 90–110% → red
   - 70–90% → yellow
   - < 70% → green
   - Beyond 25 nm → green