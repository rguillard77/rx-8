#!/usr/bin/env python3

import sys
max_m = []
line_count = 0
last_meas = 0
rotor_face = 0
rotor_faces = {
    0: [],
    1: [],
    2: []
}
FLOOR = 4500
ADC_FS = 4.096
ADC_VMAX = 0x7FFF
VOLUME_CORRECTION_FACTOR = 1
PRESSURE_TRANSDUCER_PMAX = 200
PRESSURE_TRANSDUCER_VMAX = 4.5

def avg(lst):
    return sum(lst) / len(lst)

def print_rotor(records):
    for x in records:
        avg_psi(x, records[x])

def avg_psi(face, serie):
    v = []
    for r in serie:
        v.append(r['m'])
    m_adc = avg(v)
    m_v = m_adc * ADC_FS / ADC_VMAX
    m_psi = m_v * PRESSURE_TRANSDUCER_PMAX / PRESSURE_TRANSDUCER_VMAX
    m_corrected_psi = m_psi * VOLUME_CORRECTION_FACTOR

    print("FACE %d: BARS: %.2f CPSI: %.2f PSI: %.2f V: %f ADC: %d" %
        (face,
        round(m_corrected_psi / 14.5, 2),
        round(m_corrected_psi, 2),
        round(m_psi, 2),
        m_v,
        int(m_adc)
        )
    )

with open(sys.argv[1], "r") as fd:
    window = [0] * 3
    time = [0] * 3
    for line in fd:
        ts, meas = line.split(';')

        window.pop(0)
        time.pop(0)
        window.append(int(meas))
        time.append(float(ts))

        if window[0] < window[1] and window[1] > window[2] and window[1] > FLOOR:
            r = {
                "ts": time[1],
                "m": window[1],
            }
            rotor_faces[rotor_face].append(r)
            rotor_face += 1

        line_count += 1
        if rotor_face > 2:
            rotor_face = 0

# Cleanup (remove head and tail measurements from face 0, and normalize other faces to measurements count)
seq = rotor_faces[0]
seq.pop(0)
seq.pop()

m_size = len(rotor_faces[0])
for i in range(1, 3):
    while(m_size < len(rotor_faces[i])):
        rotor_faces[i].pop(0)

# Compute RPM
last_v = 0
v = []
for i in range(m_size):
    for y in range(3):
        r = rotor_faces[y][i]
        ts = r['ts']
        #print('%f %f' % (ts, last_v))
        if last_v > 0:
            c = ts - last_v
            #print(c)
            v.append(c)
        last_v = ts

avg_s = avg(v)
print("AVG: %f, RPM: %d" % (avg_s, int(60 / avg_s)))
print_rotor(rotor_faces)

#print("Line count {0}".format(line_count))
#print(rotor_faces)
