Terminal tool for MATE ROV 2026 Explorer Task 2.2 — iceberg tracking. Pass iceberg position, heading, keel depth, and all four platform locations from your map/data sheet. The calculator prints surface and subsea threat levels for each platform.

Python 3.6+ (No pip libs used)

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