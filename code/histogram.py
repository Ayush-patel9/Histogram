# import psycopg2
# import time
# import matplotlib.pyplot as plt
# from collections import Counter

# DB_USER = "ayushpatel"
# NUM_SAMPLES = 3000
# NUM_BUCKETS = 19

# conn = psycopg2.connect(
#     dbname="job",
#     user=DB_USER,
#     host="localhost",
#     port="5432"
# )

# cursor = conn.cursor()


# def build_histogram(column):

#     query = f"""
#         SELECT {column}
#         FROM (
#             SELECT {column}
#             FROM title
#             TABLESAMPLE BERNOULLI (5)
#         ) AS sampled
#         ORDER BY random()
#         LIMIT {NUM_SAMPLES};
#     """

#     cursor.execute(query)

#     raw_data = [row[0] for row in cursor.fetchall()]

#     print(f"{column}: {len(raw_data)} samples")

#     start_time = time.time()

#     freq_map = Counter(raw_data)

#     unique_vals = sorted(freq_map.keys())

#     frequencies = [
#         freq_map[value]
#         for value in unique_vals
#     ]

#     N = len(unique_vals)

#     actual_buckets = min(NUM_BUCKETS, N)

#     # Prefix sums
#     pref_sum = [0] * (N + 1)
#     pref_sq_sum = [0] * (N + 1)

#     for i in range(N):
#         f = frequencies[i]

#         pref_sum[i + 1] = pref_sum[i] + f
#         pref_sq_sum[i + 1] = pref_sq_sum[i] + f * f

#     # SSE for values i through j
#     def get_sse(i, j):

#         count = j - i + 1

#         sum_f = (
#             pref_sum[j + 1]
#             - pref_sum[i]
#         )

#         sum_sq_f = (
#             pref_sq_sum[j + 1]
#             - pref_sq_sum[i]
#         )

#         return (
#             sum_sq_f
#             - (sum_f * sum_f) / count
#         )

#     # DP tables
#     dp = [
#         [float("inf")] * (actual_buckets + 1)
#         for _ in range(N + 1)
#     ]

#     cuts = [
#         [-1] * (actual_buckets + 1)
#         for _ in range(N + 1)
#     ]

#     # One bucket
#     for i in range(1, N + 1):

#         dp[i][1] = get_sse(0, i - 1)

#     # Multiple buckets
#     for b in range(2, actual_buckets + 1):

#         for i in range(b, N + 1):

#             for k in range(b - 1, i):

#                 cost = (
#                     dp[k][b - 1]
#                     + get_sse(k, i - 1)
#                 )

#                 if cost < dp[i][b]:

#                     dp[i][b] = cost
#                     cuts[i][b] = k

#     # Backtrack
#     bucket_ranges = []

#     curr_n = N
#     curr_b = actual_buckets

#     while curr_b > 1:

#         split_point = cuts[curr_n][curr_b]

#         bucket_ranges.append(
#             (
#                 split_point,
#                 curr_n - 1
#             )
#         )

#         curr_n = split_point
#         curr_b -= 1

#     bucket_ranges.append(
#         (0, curr_n - 1)
#     )

#     bucket_ranges.reverse()

#     # Convert ranges to boundaries and frequencies
#     boundaries = []
#     bucket_frequencies = []

#     for start, end in bucket_ranges:

#         lower = unique_vals[start]
#         upper = unique_vals[end]

#         boundaries.append(
#             (lower, upper)
#         )

#         bucket_frequency = sum(
#             frequencies[start:end + 1]
#         )

#         bucket_frequencies.append(
#             bucket_frequency
#         )

#     build_time = time.time() - start_time

#     # ------------------------------------------------
#     # Maximum Selectivity Error
#     # ------------------------------------------------

#     max_error = 0

#     error_details = []

#     for bucket_index, (start, end) in enumerate(bucket_ranges):

#         bucket_total = sum(
#             frequencies[start:end + 1]
#         )

#         distinct_count = end - start + 1

#         mean_frequency = (
#             bucket_total / distinct_count
#         )

#         for i in range(start, end + 1):

#             actual_frequency = frequencies[i]

#             error = abs(
#                 actual_frequency
#                 - mean_frequency
#             ) / len(raw_data)

#             error_details.append(
#                 (
#                     unique_vals[i],
#                     bucket_index + 1,
#                     actual_frequency,
#                     mean_frequency,
#                     error
#                 )
#             )

#             if error > max_error:
#                 max_error = error

#     return (
#         raw_data,
#         boundaries,
#         bucket_frequencies,
#         dp[N][actual_buckets],
#         build_time,
#         max_error,
#         unique_vals,
#         frequencies,
#         bucket_ranges
#     )


# # =====================================================
# # BUILD BOTH HISTOGRAMS
# # =====================================================

# id_result = build_histogram("id")

# title_result = build_histogram("title")


# # =====================================================
# # UNPACK RESULTS
# # =====================================================

# (
#     id_raw_data,
#     id_boundaries,
#     id_bucket_frequencies,
#     id_sse,
#     id_time,
#     id_max_error,
#     id_unique,
#     id_frequencies,
#     id_ranges
# ) = id_result


# (
#     title_raw_data,
#     title_boundaries,
#     title_bucket_frequencies,
#     title_sse,
#     title_time,
#     title_max_error,
#     title_unique,
#     title_frequencies,
#     title_ranges
# ) = title_result


# # =====================================================
# # PRINT ID RESULTS
# # =====================================================

# print("\n==========================================")
# print("OPTIMAL SERIAL HISTOGRAM FOR ID")
# print("==========================================")

# print("Samples:", len(id_raw_data))
# print("Buckets:", len(id_boundaries))
# print("Minimum SSE:", id_sse)
# print("Build Time:", f"{id_time:.6f} seconds")
# print(
#     "Maximum Selectivity Error:",
#     f"{id_max_error:.8f}"
# )
# print(
#     "Maximum Selectivity Error (%):",
#     f"{id_max_error * 100:.6f}%"
# )

# print("\nFrequency Bucket Boundaries:")

# for i in range(len(id_boundaries)):

#     print(
#         f"Bucket {i + 1}: "
#         f"{id_boundaries[i][0]} - "
#         f"{id_boundaries[i][1]} "
#         f"Frequency = "
#         f"{id_bucket_frequencies[i]}"
#     )


# # =====================================================
# # PRINT TITLE RESULTS
# # =====================================================

# print("\n==========================================")
# print("OPTIMAL SERIAL HISTOGRAM FOR TITLE")
# print("==========================================")

# print("Samples:", len(title_raw_data))
# print("Buckets:", len(title_boundaries))
# print("Minimum SSE:", title_sse)
# print("Build Time:", f"{title_time:.6f} seconds")
# print(
#     "Maximum Selectivity Error:",
#     f"{title_max_error:.8f}"
# )
# print(
#     "Maximum Selectivity Error (%):",
#     f"{title_max_error * 100:.6f}%"
# )

# print("\nFrequency Bucket Boundaries:")

# for i in range(len(title_boundaries)):

#     print(
#         f"Bucket {i + 1}: "
#         f"{title_boundaries[i][0]} - "
#         f"{title_boundaries[i][1]} "
#         f"Frequency = "
#         f"{title_bucket_frequencies[i]}"
#     )


# # =====================================================
# # PLOT BOTH HISTOGRAMS
# # =====================================================

# fig, axes = plt.subplots(
#     1,
#     2,
#     figsize=(22, 10)
# )


# # ---------------- ID ----------------

# id_positions = range(
#     len(id_bucket_frequencies)
# )

# axes[0].barh(
#     id_positions,
#     id_bucket_frequencies,
#     edgecolor="black"
# )

# axes[0].set_yticks(
#     id_positions
# )

# axes[0].set_yticklabels(
#     [
#         f"{lower} - {upper}"
#         for lower, upper in id_boundaries
#     ],
#     fontsize=8
# )

# axes[0].set_xlabel("Frequency")
# axes[0].set_ylabel("Value Boundaries")

# axes[0].set_title(
#     "Optimal Serial Histogram for id"
# )

# axes[0].grid(
#     axis="x",
#     linestyle="--",
#     alpha=0.7
# )


# # ---------------- TITLE ----------------

# title_positions = range(
#     len(title_bucket_frequencies)
# )

# axes[1].barh(
#     title_positions,
#     title_bucket_frequencies,
#     edgecolor="black"
# )

# axes[1].set_yticks(
#     title_positions
# )

# axes[1].set_yticklabels(
#     [
#         f"{str(lower)[:20]} - {str(upper)[:20]}"
#         for lower, upper in title_boundaries
#     ],
#     fontsize=7
# )

# axes[1].set_xlabel("Frequency")
# axes[1].set_ylabel("Value Boundaries")

# axes[1].set_title(
#     "Optimal Serial Histogram for title"
# )

# axes[1].grid(
#     axis="x",
#     linestyle="--",
#     alpha=0.7
# )

# sample_sizes = [1000, 3000, 5000]

# id_build_times = [
#     1.226,
#     11.0305, 
#     31.3998 
# ]

# title_build_times = [
#     1.116,  
#     9.91, 
#     27.278   
# ]


# total_table_rows = 2528312

# def extrapolate_time(x, y, target_x):
#     n = len(x)
#     sum_x = sum(x)
#     sum_y = sum(y)
#     sum_xy = sum(x[i] * y[i] for i in range(n))
#     sum_x2 = sum(x[i] ** 2 for i in range(n))
    
#     slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x ** 2)
#     intercept = (sum_y - slope * sum_x) / n
    
#     extrapolated_seconds = (slope * target_x) + intercept
#     return slope, intercept, extrapolated_seconds

# def print_results(column_name, x, y):
#     slope, intercept, seconds = extrapolate_time(x, y, total_table_rows)
#     hours = seconds / 3600
#     days = hours / 24
    
#     print(f"==========================================")
#     print(f"EXTRAPOLATION FOR '{column_name.upper()}' COLUMN")
#     print(f"==========================================")
#     print(f"Equation: Time = ({slope:.6f} * rows) + {intercept:.6f}")
#     print(f"Extrapolated Time for {total_table_rows:,} rows:")
#     print(f"Seconds : {seconds:,.2f}")
#     print(f"Hours   : {hours:,.2f}")
#     print(f"Days    : {days:,.2f}\n")

# print_results("id", sample_sizes, id_build_times)
# print_results("title", sample_sizes, title_build_times)

# # =====================================================
# # PLOT 1: ACTUAL SAMPLE SIZE VS BUILD TIME
# # =====================================================

# plt.figure(figsize=(10, 7))

# plt.plot(
#     sample_sizes,
#     id_build_times,
#     marker="o",
#     linewidth=2,
#     label="id"
# )

# plt.plot(
#     sample_sizes,
#     title_build_times,
#     marker="o",
#     linewidth=2,
#     label="title"
# )

# plt.xlabel("Number of Samples")
# plt.ylabel("Build Time (seconds)")
# plt.title("Sample Size vs Histogram Build Time")

# plt.xticks(sample_sizes)

# plt.grid(
#     True,
#     linestyle="--",
#     alpha=0.7
# )

# plt.legend()

# plt.tight_layout()
# plt.show()


# # =====================================================
# # PLOT 2: EXTRAPOLATED SAMPLE SIZE VS BUILD TIME
# # =====================================================

# # Calculate regression parameters
# id_slope, id_intercept, id_extrapolated = extrapolate_time(
#     sample_sizes,
#     id_build_times,
#     total_table_rows
# )

# title_slope, title_intercept, title_extrapolated = extrapolate_time(
#     sample_sizes,
#     title_build_times,
#     total_table_rows
# )

# # Generate points for regression lines
# extrapolation_x = [
#     1000,
#     10000,
#     100000,
#     500000,
#     1000000,
#     1500000,
#     2000000,
#     total_table_rows
# ]

# id_extrapolation_y = [
#     id_slope * x + id_intercept
#     for x in extrapolation_x
# ]

# title_extrapolation_y = [
#     title_slope * x + title_intercept
#     for x in extrapolation_x
# ]

# plt.figure(figsize=(12, 7))

# # Regression lines
# plt.plot(
#     extrapolation_x,
#     id_extrapolation_y,
#     linewidth=2,
#     label="id - extrapolated"
# )

# plt.plot(
#     extrapolation_x,
#     title_extrapolation_y,
#     linewidth=2,
#     label="title - extrapolated"
# )

# # Actual measured points
# plt.scatter(
#     sample_sizes,
#     id_build_times,
#     s=70,
#     label="id - actual"
# )

# plt.scatter(
#     sample_sizes,
#     title_build_times,
#     s=70,
#     label="title - actual"
# )

# # Extrapolated points
# plt.scatter(
#     total_table_rows,
#     id_extrapolated,
#     s=100,
#     marker="X",
#     label="id - full table estimate"
# )

# plt.scatter(
#     total_table_rows,
#     title_extrapolated,
#     s=100,
#     marker="X",
#     label="title - full table estimate"
# )

# # Labels for extrapolated points
# plt.annotate(
#     f"{id_extrapolated:.2f} sec",
#     (total_table_rows, id_extrapolated),
#     xytext=(-100, 10),
#     textcoords="offset points"
# )

# plt.annotate(
#     f"{title_extrapolated:.2f} sec",
#     (total_table_rows, title_extrapolated),
#     xytext=(-100, -25),
#     textcoords="offset points"
# )

# plt.xlabel("Number of Rows / Samples")
# plt.ylabel("Build Time (seconds)")

# plt.title(
#     "Extrapolated Sample Size vs Histogram Build Time"
# )

# plt.grid(
#     True,
#     linestyle="--",
#     alpha=0.7
# )

# plt.legend()
# plt.xscale("log")
# plt.tight_layout()
# plt.show()


# cursor.close()
# conn.close()


import psycopg2
import time
import matplotlib.pyplot as plt
from collections import Counter


DB_USER = "ayushpatel"
NUM_SAMPLES = 5000
NUM_BUCKETS = 19


conn = psycopg2.connect(
    dbname="job",
    user=DB_USER,
    host="localhost",
    port="5432"
)

cursor = conn.cursor()


def build_histogram(column):

    query = f"""
        SELECT {column}
        FROM (
            SELECT {column}
            FROM title
            TABLESAMPLE BERNOULLI (5)
        ) AS sampled
        ORDER BY random()
        LIMIT {NUM_SAMPLES};
    """

    cursor.execute(query)

    raw_data = [row[0] for row in cursor.fetchall()]

    print(f"{column}: {len(raw_data)} samples")

    start_time = time.time()

    freq_map = Counter(raw_data)

    unique_vals = sorted(freq_map.keys())

    frequencies = [
        freq_map[value]
        for value in unique_vals
    ]

    N = len(unique_vals)

    actual_buckets = min(NUM_BUCKETS, N)

    # Prefix sums
    pref_sum = [0] * (N + 1)
    pref_sq_sum = [0] * (N + 1)

    for i in range(N):
        f = frequencies[i]

        pref_sum[i + 1] = pref_sum[i] + f
        pref_sq_sum[i + 1] = pref_sq_sum[i] + f * f

    # SSE for values i through j
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

    # DP tables
    dp = [
        [float("inf")] * (actual_buckets + 1)
        for _ in range(N + 1)
    ]

    cuts = [
        [-1] * (actual_buckets + 1)
        for _ in range(N + 1)
    ]

    # One bucket
    for i in range(1, N + 1):

        dp[i][1] = get_sse(0, i - 1)

    # Multiple buckets
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

    # Backtrack
    bucket_ranges = []

    curr_n = N
    curr_b = actual_buckets

    while curr_b > 1:

        split_point = cuts[curr_n][curr_b]

        bucket_ranges.append(
            (
                split_point,
                curr_n - 1
            )
        )

        curr_n = split_point
        curr_b -= 1

    bucket_ranges.append(
        (0, curr_n - 1)
    )

    bucket_ranges.reverse()

    # Convert ranges to boundaries and frequencies
    boundaries = []
    bucket_frequencies = []

    for start, end in bucket_ranges:

        lower = unique_vals[start]
        upper = unique_vals[end]

        boundaries.append(
            (lower, upper)
        )

        bucket_frequency = sum(
            frequencies[start:end + 1]
        )

        bucket_frequencies.append(
            bucket_frequency
        )

    build_time = time.time() - start_time

    # ------------------------------------------------
    # Maximum Selectivity Error
    # ------------------------------------------------

    max_error = 0

    error_details = []

    for bucket_index, (start, end) in enumerate(bucket_ranges):

        bucket_total = sum(
            frequencies[start:end + 1]
        )

        distinct_count = end - start + 1

        mean_frequency = (
            bucket_total / distinct_count
        )

        for i in range(start, end + 1):

            actual_frequency = frequencies[i]

            error = abs(
                actual_frequency
                - mean_frequency
            ) / len(raw_data)

            error_details.append(
                (
                    unique_vals[i],
                    bucket_index + 1,
                    actual_frequency,
                    mean_frequency,
                    error
                )
            )

            if error > max_error:
                max_error = error

    return (
        raw_data,
        boundaries,
        bucket_frequencies,
        dp[N][actual_buckets],
        build_time,
        max_error,
        unique_vals,
        frequencies,
        bucket_ranges
    )


# =====================================================
# BUILD BOTH HISTOGRAMS
# =====================================================

id_result = build_histogram("id")

title_result = build_histogram("title")


# =====================================================
# UNPACK RESULTS
# =====================================================

(
    id_raw_data,
    id_boundaries,
    id_bucket_frequencies,
    id_sse,
    id_time,
    id_max_error,
    id_unique,
    id_frequencies,
    id_ranges
) = id_result


(
    title_raw_data,
    title_boundaries,
    title_bucket_frequencies,
    title_sse,
    title_time,
    title_max_error,
    title_unique,
    title_frequencies,
    title_ranges
) = title_result


# =====================================================
# PRINT ID RESULTS
# =====================================================

print("\n==========================================")
print("OPTIMAL SERIAL HISTOGRAM FOR ID")
print("==========================================")

print("Samples:", len(id_raw_data))
print("Buckets:", len(id_boundaries))
print("Minimum SSE:", id_sse)
print("Build Time:", f"{id_time:.6f} seconds")
print(
    "Maximum Selectivity Error:",
    f"{id_max_error:.8f}"
)

print(
    "Maximum Selectivity Error (%):",
    f"{id_max_error * 100:.6f}%"
)

print("\nFrequency Bucket Boundaries:")

for i in range(len(id_boundaries)):

    print(
        f"Bucket {i + 1}: "
        f"{id_boundaries[i][0]} - "
        f"{id_boundaries[i][1]} "
        f"Frequency = "
        f"{id_bucket_frequencies[i]}"
    )


# =====================================================
# PRINT TITLE RESULTS
# =====================================================

print("\n==========================================")
print("OPTIMAL SERIAL HISTOGRAM FOR TITLE")
print("==========================================")

print("Samples:", len(title_raw_data))
print("Buckets:", len(title_boundaries))
print("Minimum SSE:", title_sse)
print("Build Time:", f"{title_time:.6f} seconds")
print(
    "Maximum Selectivity Error:",
    f"{title_max_error:.8f}"
)

print(
    "Maximum Selectivity Error (%):",
    f"{title_max_error * 100:.6f}%"
)

print("\nFrequency Bucket Boundaries:")

for i in range(len(title_boundaries)):

    print(
        f"Bucket {i + 1}: "
        f"{title_boundaries[i][0]} - "
        f"{title_boundaries[i][1]} "
        f"Frequency = "
        f"{title_bucket_frequencies[i]}"
    )


# =====================================================
# PLOT BOTH HISTOGRAMS
# =====================================================

fig, axes = plt.subplots(
    1,
    2,
    figsize=(22, 10)
)


# ---------------- ID ----------------

id_positions = range(
    len(id_bucket_frequencies)
)

axes[0].bar(
    id_positions,
    id_bucket_frequencies,
    edgecolor="black"
)

axes[0].set_xticks(
    id_positions
)

axes[0].set_xticklabels(
    [
        f"{lower} - {upper}"
        for lower, upper in id_boundaries
    ],
    rotation=90,
    fontsize=8
)

axes[0].set_xlabel("Value Boundaries")
axes[0].set_ylabel("Frequency")

axes[0].set_title(
    "Optimal Serial Histogram for id"
)

axes[0].grid(
    axis="y",
    linestyle="--",
    alpha=0.7
)


# ---------------- TITLE ----------------

title_positions = range(
    len(title_bucket_frequencies)
)

axes[1].bar(
    title_positions,
    title_bucket_frequencies,
    edgecolor="black"
)

axes[1].set_xticks(
    title_positions
)

axes[1].set_xticklabels(
    [
        f"{str(lower)[:20]} - {str(upper)[:20]}"
        for lower, upper in title_boundaries
    ],
    rotation=90,
    fontsize=7
)

axes[1].set_xlabel("Value Boundaries")
axes[1].set_ylabel("Frequency")

axes[1].set_title(
    "Optimal Serial Histogram for title"
)

axes[1].grid(
    axis="y",
    linestyle="--",
    alpha=0.7
)


plt.tight_layout()
plt.show()


sample_sizes = [1000, 3000, 5000]

id_build_times = [
    1.226,
    11.0305,
    31.3998
]

title_build_times = [
    1.116,
    9.91,
    27.278
]


total_table_rows = 2528312


def extrapolate_time(x, y, target_x):

    n = len(x)

    sum_x = sum(x)
    sum_y = sum(y)

    sum_xy = sum(
        x[i] * y[i]
        for i in range(n)
    )

    sum_x2 = sum(
        x[i] ** 2
        for i in range(n)
    )

    slope = (
        n * sum_xy - sum_x * sum_y
    ) / (
        n * sum_x2 - sum_x ** 2
    )

    intercept = (
        sum_y - slope * sum_x
    ) / n

    extrapolated_seconds = (
        slope * target_x
    ) + intercept

    return (
        slope,
        intercept,
        extrapolated_seconds
    )


def print_results(column_name, x, y):

    slope, intercept, seconds = (
        extrapolate_time(
            x,
            y,
            total_table_rows
        )
    )

    hours = seconds / 3600
    days = hours / 24

    print(
        f"=========================================="
    )

    print(
        f"EXTRAPOLATION FOR "
        f"'{column_name.upper()}' COLUMN"
    )

    print(
        f"=========================================="
    )

    print(
        f"Equation: Time = "
        f"({slope:.6f} * rows) + "
        f"{intercept:.6f}"
    )

    print(
        f"Extrapolated Time for "
        f"{total_table_rows:,} rows:"
    )

    print(
        f"Seconds : {seconds:,.2f}"
    )

    print(
        f"Hours   : {hours:,.2f}"
    )

    print(
        f"Days    : {days:,.2f}\n"
    )


print_results(
    "id",
    sample_sizes,
    id_build_times
)

print_results(
    "title",
    sample_sizes,
    title_build_times
)


# =====================================================
# PLOT 1: ACTUAL SAMPLE SIZE VS BUILD TIME
# =====================================================

plt.figure(
    figsize=(10, 7)
)

plt.plot(
    sample_sizes,
    id_build_times,
    marker="o",
    linewidth=2,
    label="id"
)

plt.plot(
    sample_sizes,
    title_build_times,
    marker="o",
    linewidth=2,
    label="title"
)

plt.xlabel(
    "Number of Samples"
)

plt.ylabel(
    "Build Time (seconds)"
)

plt.title(
    "Sample Size vs Histogram Build Time"
)

plt.xticks(
    sample_sizes
)

plt.grid(
    True,
    linestyle="--",
    alpha=0.7
)

plt.legend()

plt.tight_layout()

plt.show()


# =====================================================
# PLOT 2: EXTRAPOLATED SAMPLE SIZE VS BUILD TIME
# =====================================================

# Calculate regression parameters

id_slope, id_intercept, id_extrapolated = (
    extrapolate_time(
        sample_sizes,
        id_build_times,
        total_table_rows
    )
)

title_slope, title_intercept, title_extrapolated = (
    extrapolate_time(
        sample_sizes,
        title_build_times,
        total_table_rows
    )
)


# Generate points for regression lines

extrapolation_x = [
    1000,
    10000,
    100000,
    500000,
    1000000,
    1500000,
    2000000,
    total_table_rows
]


id_extrapolation_y = [
    id_slope * x + id_intercept
    for x in extrapolation_x
]

title_extrapolation_y = [
    title_slope * x + title_intercept
    for x in extrapolation_x
]


plt.figure(
    figsize=(12, 7)
)


# Regression lines

plt.plot(
    extrapolation_x,
    id_extrapolation_y,
    linewidth=2,
    label="id - extrapolated"
)

plt.plot(
    extrapolation_x,
    title_extrapolation_y,
    linewidth=2,
    label="title - extrapolated"
)


# Actual measured points

plt.scatter(
    sample_sizes,
    id_build_times,
    s=70,
    label="id - actual"
)

plt.scatter(
    sample_sizes,
    title_build_times,
    s=70,
    label="title - actual"
)


# Extrapolated points

plt.scatter(
    total_table_rows,
    id_extrapolated,
    s=100,
    marker="X",
    label="id - full table estimate"
)

plt.scatter(
    total_table_rows,
    title_extrapolated,
    s=100,
    marker="X",
    label="title - full table estimate"
)


# Labels for extrapolated points

plt.annotate(
    f"{id_extrapolated:.2f} sec",
    (total_table_rows, id_extrapolated),
    xytext=(-100, 10),
    textcoords="offset points"
)

plt.annotate(
    f"{title_extrapolated:.2f} sec",
    (total_table_rows, title_extrapolated),
    xytext=(-100, -25),
    textcoords="offset points"
)


plt.xlabel(
    "Number of Rows / Samples"
)

plt.ylabel(
    "Build Time (seconds)"
)

plt.title(
    "Extrapolated Sample Size vs Histogram Build Time"
)

plt.grid(
    True,
    linestyle="--",
    alpha=0.7
)

plt.legend()

plt.xscale("log")

plt.tight_layout()

plt.show()


cursor.close()
conn.close()