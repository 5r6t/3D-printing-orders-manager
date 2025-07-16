# Currently supports gcode from (tested):
# * Prusaslicer

import re

def parse_gcode(filepath):
    filament_grams = 0.0
    print_time_min = 0


    with open(filepath, 'r', encoding='utf-8', errors='ignore') as file:
        lines = file.readlines()

    for line in reversed(lines): # faster for Prusaslicer gcode
        # Total filament used
        if "total filament used [g]" in line:
            match = re.search(r"([\d.]+)", line)
            if match:
                filament_grams = float(match.group(1))

        # Estimated printing time (normal mode)
        elif "estimated printing time (normal mode)" in line:
            h = m = s = 0
            h_match = re.search(r"(\d+)h", line)
            m_match = re.search(r"(\d+)m", line)
            s_match = re.search(r"(\d+)s", line)

            if h_match:
                h = int(h_match.group(1))
            if m_match:
                m = int(m_match.group(1))
            if s_match:
                s = int(s_match.group(1))

            print_time_min = h * 60 + m + (1 if s > 30 else 0)  # seconds rounded

    return round(filament_grams), print_time_min
