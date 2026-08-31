import matplotlib.pyplot as plt

# Histogram boundaries obtained from PostgreSQL pg_stats
boundaries = [
    5, 25115, 51032, 77854, 104855, 128544, 153252, 178094,
    204585, 228696, 252756, 277787, 303649, 328202, 354017,
    380635, 407446, 433631, 458753, 484592, 509939, 535092,
    562500, 587095, 611308, 638200, 664487, 689484, 716642,
    742068, 766652, 791299, 817195, 841652, 865990, 889561,
    916584, 938211, 962496, 985895, 1011069, 1039483, 1067227,
    1093856, 1118487, 1145174, 1167334, 1191936, 1216954,
    1243317, 1269294, 1295848, 1318631, 1343675, 1369352,
    1393108, 1419093, 1442295, 1468720, 1494199, 1517077,
    1543511, 1569356, 1593191, 1622323, 1646279, 1670339,
    1698260, 1724458, 1749374, 1772473, 1798903, 1822509,
    1848852, 1875716, 1901087, 1926138, 1951650, 1974528,
    1999624, 2024573, 2051030, 2074075, 2099721, 2124168,
    2149618, 2173299, 2197911, 2224452, 2251996, 2278040,
    2300968, 2327759, 2353484, 2378200, 2402275, 2425644,
    2453035, 2478393, 2503117, 2528121
]

# 101 boundaries -> 100 buckets
num_buckets = len(boundaries) - 1

# Equi-depth frequency
bucket_frequency = 25283

# Width of every bucket
widths = [
    boundaries[i + 1] - boundaries[i]
    for i in range(num_buckets)
]

# Center of every bucket
centers = [
    (boundaries[i] + boundaries[i + 1]) / 2
    for i in range(num_buckets)
]

# Same frequency for every equi-depth bucket
heights = [bucket_frequency] * num_buckets

plt.figure(figsize=(16, 7))

plt.bar(
    centers,
    heights,
    width=widths,
    align="center",
    edgecolor="black"
)

plt.xlabel("Value Boundaries")
plt.ylabel("Frequency")
plt.title("Equi-Depth Histogram for title.id")

# Show boundary values on X-axis
plt.xticks(boundaries, rotation=90, fontsize=7)

plt.grid(axis="y", linestyle="--", alpha=0.7)

plt.tight_layout()
plt.show()