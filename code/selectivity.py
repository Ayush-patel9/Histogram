import psycopg2
import matplotlib.pyplot as plt
from collections import Counter

DB_USER = "ayushpatel"
NUM_BUCKETS = 19
SAMPLE_SIZES = [1000, 3000, 5000]

conn = psycopg2.connect(
    dbname="job",
    user=DB_USER,
    host="localhost",
    port="5432"
)

cursor = conn.cursor()


def calculate_max_error(column, num_samples):

    query = f"""
        SELECT {column}
        FROM (
            SELECT {column}
            FROM title
            TABLESAMPLE BERNOULLI (5)
        ) AS sampled
        ORDER BY random()
        LIMIT {num_samples};
    """

    cursor.execute(query)

    raw_data = [row[0] for row in cursor.fetchall()]

    freq_map = Counter(raw_data)

    unique_vals = sorted(freq_map.keys())

    frequencies = [
        freq_map[value]
        for value in unique_vals
    ]

    N = len(unique_vals)

    actual_buckets = min(NUM_BUCKETS, N)

    pref_sum = [0] * (N + 1)
    pref_sq_sum = [0] * (N + 1)

    for i in range(N):

        f = frequencies[i]

        pref_sum[i + 1] = pref_sum[i] + f
        pref_sq_sum[i + 1] = pref_sq_sum[i] + f * f


    def get_sse(i, j):

        count = j - i + 1

        sum_f = (
            pref_sum[j + 1]
            - pref_sum[i]
        )

        sum_sq_f = (
            pref_sq_sum[j + 1]
            - pref_sq_sum[i]
        )

        return (
            sum_sq_f
            - (sum_f * sum_f) / count
        )


    dp = [
        [float("inf")] * (actual_buckets + 1)
        for _ in range(N + 1)
    ]

    cuts = [
        [-1] * (actual_buckets + 1)
        for _ in range(N + 1)
    ]


    for i in range(1, N + 1):

        dp[i][1] = get_sse(
            0,
            i - 1
        )


    for b in range(2, actual_buckets + 1):

        for i in range(b, N + 1):

            for k in range(b - 1, i):

                cost = (
                    dp[k][b - 1]
                    + get_sse(k, i - 1)
                )

                if cost < dp[i][b]:

                    dp[i][b] = cost
                    cuts[i][b] = k


    bucket_ranges = []

    curr_n = N
    curr_b = actual_buckets

    while curr_b > 1:

        split_point = cuts[curr_n][curr_b]

        bucket_ranges.append(
            (split_point, curr_n - 1)
        )

        curr_n = split_point
        curr_b -= 1

    bucket_ranges.append(
        (0, curr_n - 1)
    )

    bucket_ranges.reverse()


    max_error = 0

    for start, end in bucket_ranges:

        bucket_total = sum(
            frequencies[start:end + 1]
        )

        distinct_count = end - start + 1

        mean_frequency = (
            bucket_total / distinct_count
        )

        for i in range(start, end + 1):

            actual_frequency = frequencies[i]

            error = (
                abs(
                    actual_frequency
                    - mean_frequency
                )
                / len(raw_data)
            )

            max_error = max(
                max_error,
                error
            )

    return max_error


# ==========================================
# CALCULATE ERROR FOR ALL SAMPLE SIZES
# ==========================================

id_errors = []
title_errors = []

for size in SAMPLE_SIZES:

    id_error = calculate_max_error(
        "id",
        size
    )

    title_error = calculate_max_error(
        "title",
        size
    )

    id_errors.append(id_error)
    title_errors.append(title_error)

    print(
        f"Sample Size = {size}"
    )

    print(
        f"ID Max Selectivity Error = "
        f"{id_error:.8f} "
        f"({id_error * 100:.4f}%)"
    )

    print(
        f"TITLE Max Selectivity Error = "
        f"{title_error:.8f} "
        f"({title_error * 100:.4f}%)"
    )

    print("------------------------------------------")


# ==========================================
# PLOT
# ==========================================

plt.figure(figsize=(10, 7))

plt.plot(
    SAMPLE_SIZES,
    id_errors,
    marker="o",
    linewidth=2,
    label="id"
)

plt.plot(
    SAMPLE_SIZES,
    title_errors,
    marker="o",
    linewidth=2,
    label="title"
)

plt.xlabel("Sample Size")
plt.ylabel("Maximum Selectivity Error")

plt.title(
    "Sample Size vs Maximum Selectivity Error"
)

plt.xticks(SAMPLE_SIZES)

plt.grid(
    True,
    linestyle="--",
    alpha=0.7
)

plt.legend()

plt.tight_layout()

plt.show()


cursor.close()
conn.close()