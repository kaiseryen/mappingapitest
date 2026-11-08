import pysrt
import json
import re

def getval(line, word):
    m = re.search(
        rf"{word}[A-Za-z_]*\s*[:=]\s*(-?\d+(?:\.\d+)?)",
        line,
        re.IGNORECASE
    )
    if m:
        return float(m.group(1))

def linksrt(srt_path,frames,fps):
    subs = pysrt.open(srt_path,encoding="latin-1")
    locations = []

    for i in frames:
        t = 1000 * (i-1)
        cur_sub = subs.slice(starts_before={'milliseconds': t}, ends_after={'milliseconds': t})

        if not cur_sub: # There is no sub if the time is exactly the start or end
                        # Should probably improve this method
            cur_sub = subs.slice(starts_before={'milliseconds': t+1}, ends_after={'milliseconds': t+1})

        if cur_sub:
            d = cur_sub.text
            lat, lon = getval(d, "lat"), getval(d, "lon")
            locations.append({"lat": lat, "lon": lon,
                              "altitude": getval(d, "rel"), "label": f"Trash: lat {lat}, lon {lon}"})

    return locations

def mapmarker(locations):
    with open("map/markers.json", "w") as f:
        json.dump(locations, f)
    return



