from lxml import etree as ET
from pathlib import Path

all_input_exb_files = Path("iriss_with_w_and_pauses/").glob("*exb.xml")
all_annotated_files = Path("Iriss-disfl-anno-phase1/").glob(".xml")
in_file = Path("iriss_with_w_and_pauses/Iriss-J-Gvecg-P580009.exb.xml")
out_file = Path("Iriss-disfl-anno-phase1/Iriss-J-Gvecg-P580009.exb.xml")

annodoc = ET.fromstring(out_file.read_bytes())

def test_time_uniqness(path:Path):
    doc = ET.fromstring(path.read_bytes())
    all_tlis = doc.findall(".//{*}tli")

    tli_names = [i.get("id") for i in all_tlis]
    tli_times = [i.get("time") for i in all_tlis]

    names_unique = len(tli_names) == len(set(tli_names))
    times_unique = len(tli_times) == len(set(tli_times))
    return times_unique

def test_name_uniqness(path:Path):
    doc = ET.fromstring(path.read_bytes())
    all_tlis = doc.findall(".//{*}tli")

    tli_names = [i.get("id") for i in all_tlis]
    tli_times = [i.get("time") for i in all_tlis]

    names_unique = len(tli_names) == len(set(tli_names))
    times_unique = len(tli_times) == len(set(tli_times))
    return names_unique

def get_non_unique_names(path:Path):
    doc = ET.fromstring(path.read_bytes())
    all_tlis = doc.findall(".//{*}tli")

    tli_names = [i.get("id") for i in all_tlis]
    tli_times = [i.get("time") for i in all_tlis]

    names_unique = len(tli_names) == len(set(tli_names))
    times_unique = len(tli_times) == len(set(tli_times))
    
    from collections import Counter
    namecounter = Counter(tli_names)
    return [i[0] for i in namecounter.most_common() if i[1] > 1]

def get_events_with_nonpositive_duration(path:Path):
    doc = ET.fromstring(path.read_bytes())
    all_tlis = doc.findall(".//{*}tli")

    timelinedict = {i.get("id"): i.get("time") for i in all_tlis}
    fishy_events = []
    for event in doc.findall(".//{*}event"):
        start_s = timelinedict[event.get("start")]
        end_s = timelinedict[event.get("end")]
        is_positive = float(end_s) - float(start_s) > 0
        if not is_positive:
            fishy_events.append((event.get("start"), event.get("end")))
    return fishy_events
bugcounter = 0
names_bugcounter = 0
for file in all_input_exb_files:
    n = test_name_uniqness(file)
    t = test_time_uniqness(file)
    nonpositives = get_events_with_nonpositive_duration(file)
    d = nonpositives == []
    if not (n and d):
        print(f"File {file.name}: names are {'' if n else 'not'} unique, there are {len(nonpositives)} events with nonpositive duration.")
        if not n:
            print(f"\tCheck following tlis: {get_non_unique_names(file)}")
        if not d:
            print("\tFishy events:\n", *[f"\t\t from {i[0]} to {i[1]}\n" for i in nonpositives])
        bugcounter += 1
    if not n:
        names_bugcounter += 1

print(f"Total bugged files: {bugcounter}.")
    
    
