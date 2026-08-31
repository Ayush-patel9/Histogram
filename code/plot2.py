import matplotlib.pyplot as plt

# Histogram boundaries obtained from PostgreSQL pg_stats
boundaries = [
    "Presentes",
    "(#1.1447)",
    "(#1.259)",
    "(#1.4603)",
    "(#1.7268)",
    "(#12.8)",
    "(#2.37)",
    "(#3.36)",
    "(#5.173)",
    "(#8.2)",
    "1971-08-23",
    "1988-09-19",
    "1996-01-17",
    "1999-03-12",
    "2001-02-04",
    "2002-10-25",
    "2004-07-06",
    "2005-09-24",
    "2006-12-30",
    "2008-04-22",
    "2010-02-04",
    "2011-05-25",
    "2012-06-08",
    "2013-05-13",
    "A Bride in the Morning",
    "A relixión",
    "Adversidad",
    "All-Stars Tournament: Part 4",
    "Animals: Moles and Voles",
    "Attack",
    "Band Foto with the Throwdowns",
    "Between the Tape",
    "Blue Wind",
    "Bruce Forsyth's Comedy Heroes",
    "Capitulo 8: Alicante",
    "Cherry Festival of Fairies",
    "Cold Fusion",
    "Creep on Trucking/Roman P. Vs. Psycho Kitty",
    "Darumakka and Hihidaruma! The Secret of the Clock Tower!!",
    "Defence of the Realm in the 21st Century",
    "Devenir",
    "DMT: The Spirit Molecule",
    "Duck Soup",
    "El futuro es azul",
    "ERod vs. Episode I, Vol. 3",
    "Family Values",
    "Fix ME",
    "Frolicking Fish",
    "Gesang vom lusitanischen Popanz",
    "Gran Premio Peugeot (Corsa automobilistica del settembre 1910 a Torino)",
    "Harold the Manghuhula!",
    "Higher Learning",
    "House IV",
    "Ich weiß, wer du bist",
    "Initial D: Third Stage",
    "Jak mel Rákosnícek starosti s modní prehlídkou",
    "Judgment in Berlin",
    "Kevin's Room 2: Trust",
    "Kuroi haru",
    "La porta sbagliata",
    "Le couronnement du roi d'Espagne",
    "Letting Go Maybe",
    "Lord of Asses 7",
    "Magtago ka na sa pinangalingan mo",
    "Matten",
    "Mike Leigh",
    "Mort d'une fourmi",
    "Nada sigue igual",
    "Nikuzeme",
    "O sole mio",
    "Oon Paoos",
    "Pandemonium, la capital del infierno",
    "Phil Donahue/Melissa Gilbert",
    "Potato Is King",
    "Quan el camperol es soldat i el soldat es camperol",
    "René Clair",
    "Rosa Thea",
    "Saudade",
    "Senor Stinky Learns Absolutely Nothing About Life",
    "Show #280 - Sendung zur Übergabe HongKongs",
    "Smile",
    "Splatter: Love, Honor and Paintball",
    "Stuka",
    "Tangled Evidence",
    "The Ancient Warrior",
    "The Case of the Frightened Fisherman",
    "The Edge",
    "The Great Trainer Robbery",
    "The Legend of Big Blue",
    "The Next Best Thing to Winning",
    "The River Knows: The Ghost Under the Bridge",
    "The Tenth Battalion",
    "Their Only Son",
    "Tokusha!! Jû-san-nin no onanii",
    "Tsirk zazhigayet ogni",
    "Uncle Reuben at the Waldorf",
    "Verse Versus Reverse",
    "Water Strategies in Disaster Situations and Solutions for a Sustainable Future",
    "White Rose",
    "XX Boy",
    "Zzak"
]

# 101 boundaries -> 100 buckets
num_buckets = len(boundaries) - 1

# Equi-depth frequency
bucket_frequency = 25283

# Use positions for textual boundaries
x = list(range(len(boundaries)))

# Each bucket has approximately the same frequency
heights = [bucket_frequency] * num_buckets

# Use midpoint of each pair of boundaries
centers = [
    (x[i] + x[i + 1]) / 2
    for i in range(num_buckets)
]

plt.figure(figsize=(20, 7))

plt.bar(
    centers,
    heights,
    width=1,
    align="center",
    edgecolor="black"
)

plt.xlabel("Value Boundaries (lexicographic order)")
plt.ylabel("Frequency")
plt.title("Equi-Depth Histogram for title.title")

# Put actual text boundaries on X-axis
plt.xticks(
    x,
    boundaries,
    rotation=90,
    fontsize=6
)

plt.grid(axis="y", linestyle="--", alpha=0.7)

plt.tight_layout()
plt.show()