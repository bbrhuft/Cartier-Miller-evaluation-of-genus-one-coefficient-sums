### W1 cold single query, cubics (median per complete query [min–max over blocks])

| bits | cmcs_frozen | bgs_harvey | bgs07 | linrec_c | linrec_py | enum_c | enum_conv | flint_power | polyrec_c | of which PARI trace (TRACE) |
|---|---|---|---|---|---|---|---|---|---|---|
| 10 | 138.3 µs [126.5 µs–147.1 µs] | 561.0 µs [460.7 µs–1.07 ms] | 5.52 ms [4.28 ms–6.75 ms] | 33.2 µs [27.2 µs–58.6 µs] | 326.2 µs [323.0 µs–409.8 µs] | 38.7 µs [37.8 µs–45.5 µs] | 429.8 µs [392.1 µs–442.6 µs] | 35.1 µs [34.1 µs–42.2 µs] | 57.6 µs [52.5 µs–72.1 µs] | 9.9 µs |
| 13 | 150.0 µs [138.6 µs–182.0 µs] | 1.31 ms [1.08 ms–1.58 ms] | 7.18 ms [6.96 ms–8.92 ms] | 214.8 µs [185.8 µs–244.1 µs] | 2.60 ms [2.24 ms–3.22 ms] | 208.7 µs [202.3 µs–278.7 µs] | 4.15 ms [3.21 ms–5.77 ms] | 536.0 µs [484.7 µs–591.1 µs] | 258.7 µs [252.2 µs–280.1 µs] | 13.5 µs |
| 16 | 172.9 µs [153.4 µs–224.6 µs] | 2.45 ms [2.22 ms–3.74 ms] | 10.63 ms [10.12 ms–17.55 ms] | 1.38 ms [1.16 ms–1.94 ms] | 19.49 ms [16.51 ms–31.98 ms] | 1.51 ms [1.36 ms–1.73 ms] | 23.72 ms [19.67 ms–38.00 ms] | 8.68 ms [7.13 ms–12.61 ms] | 3.25 ms [2.68 ms–3.54 ms] | 16.4 µs |
| 20 | 245.8 µs [231.3 µs–359.7 µs] | 6.34 ms [5.46 ms–8.08 ms] | 33.53 ms [26.65 ms–57.39 ms] | 25.04 ms [16.82 ms–29.22 ms] | 430.81 ms [302.36 ms–496.68 ms] | 36.57 ms [23.15 ms–41.29 ms] | 724.51 ms [459.69 ms–956.19 ms] | 259.61 ms [158.39 ms–325.73 ms] | 47.67 ms [31.64 ms–65.19 ms] | 27.3 µs |
| 23 | 340.5 µs [204.9 µs–360.8 µs] | 14.61 ms [12.99 ms–16.79 ms] | 77.02 ms [65.44 ms–94.00 ms] | 177.51 ms [119.13 ms–194.44 ms] | skipped ceiling | 251.13 ms [156.96 ms–319.02 ms] | skipped ceiling | budget (pilot 2.34 s) | 385.35 ms [298.14 ms–538.74 ms] | 28.3 µs |
| 26 | 312.4 µs [282.5 µs–568.2 µs] | 32.18 ms [25.75 ms–46.49 ms] | 225.61 ms [207.20 ms–247.07 ms] | 1.37 s [1.07 s–1.77 s] | skipped ceiling | budget (pilot 3.17 s) | skipped ceiling | skipped ceiling | skipped ceiling | 42.2 µs |
| 30 | 366.5 µs [360.8 µs–383.2 µs] | 170.21 ms [128.62 ms–205.29 ms] | 939.44 ms [813.51 ms–1.06 s] | skipped predicted budget | skipped ceiling | skipped ceiling | skipped ceiling | skipped ceiling | skipped ceiling | 81.3 µs |
| 33 | 476.5 µs [466.6 µs–489.8 µs] | 519.89 ms [339.10 ms–638.19 ms] | 3.05 s [2.53 s–3.49 s] | skipped ceiling | skipped ceiling | skipped ceiling | skipped ceiling | skipped ceiling | skipped ceiling | 114.1 µs |
| 36 | 588.5 µs [539.7 µs–854.5 µs] | 1.84 s [1.32 s–2.19 s] | 9.98 s [9.36 s–10.34 s] | skipped ceiling | skipped ceiling | skipped ceiling | skipped ceiling | skipped ceiling | skipped ceiling | 160.0 µs |
| 40 | 1.18 ms [852.9 µs–1.35 ms] | 6.90 s [4.67 s–9.26 s] | 45.65 s [45.61 s–45.69 s] | skipped ceiling | skipped ceiling | skipped ceiling | skipped ceiling | skipped ceiling | skipped ceiling | 375.0 µs |
| 48 | 1.94 ms [1.77 ms–2.65 ms] | skipped ceiling | skipped ceiling | skipped ceiling | skipped ceiling | skipped ceiling | skipped ceiling | skipped ceiling | skipped ceiling | 1.36 ms |
| 56 | 7.00 ms [5.38 ms–8.66 ms] | skipped ceiling | skipped ceiling | skipped ceiling | skipped ceiling | skipped ceiling | skipped ceiling | skipped ceiling | skipped ceiling | 5.56 ms |
| 62 | 131.73 ms [111.64 ms–171.89 ms] | skipped ceiling | skipped ceiling | skipped ceiling | skipped ceiling | skipped ceiling | skipped ceiling | skipped ceiling | skipped ceiling | 121.79 ms |

Each instance is a new prime p in [2^(bits-1), 2^bits), a new curve and a new pole. cmcs_frozen includes the exact trace (PARI ellap: baby-step/giant-step below ~30 digits), validation and translation sessions; the TRACE column is the trace alone, measured on separate fresh instances of the same class. Square-root comparators (bgs_*) and cmcs at >= 30 bits use the declared 60 s extended budget; others 2 s.

### W1 cold single query, quartics (median per complete query [min–max over blocks])

| bits | cmcs_frozen | bgs_harvey | bgs07 | linrec_c | linrec_py | enum_c | enum_conv | flint_power | polyrec_c | of which PARI trace (TRACE) |
|---|---|---|---|---|---|---|---|---|---|---|
| 10 | 168.7 µs [150.8 µs–251.2 µs] | 610.4 µs [542.8 µs–1.05 ms] | 8.48 ms [7.92 ms–13.59 ms] | 61.8 µs [60.1 µs–68.2 µs] | 822.6 µs [783.6 µs–860.0 µs] | 43.0 µs [35.2 µs–47.2 µs] | 363.7 µs [331.0 µs–434.4 µs] | 40.1 µs [37.9 µs–41.5 µs] | 110.3 µs [89.0 µs–136.7 µs] | 9.8 µs |
| 13 | 133.8 µs [131.8 µs–150.8 µs] | 1.90 ms [1.70 ms–2.21 ms] | 17.32 ms [16.44 ms–18.08 ms] | 453.0 µs [423.2 µs–539.7 µs] | 6.17 ms [5.50 ms–7.76 ms] | 231.6 µs [224.3 µs–235.3 µs] | 3.48 ms [3.25 ms–3.59 ms] | 690.3 µs [628.4 µs–1.00 ms] | 730.7 µs [634.5 µs–881.2 µs] | 14.8 µs |
| 16 | 194.7 µs [181.2 µs–264.8 µs] | 4.43 ms [3.93 ms–4.65 ms] | 28.89 ms [24.92 ms–31.93 ms] | 3.31 ms [3.11 ms–3.77 ms] | 53.90 ms [33.29 ms–67.30 ms] | 1.97 ms [1.88 ms–2.15 ms] | 33.51 ms [23.07 ms–40.57 ms] | 11.17 ms [9.12 ms–13.17 ms] | 5.31 ms [4.69 ms–6.00 ms] | 20.3 µs |
| 20 | 238.8 µs [229.1 µs–247.7 µs] | 14.78 ms [10.26 ms–16.87 ms] | 78.63 ms [62.03 ms–90.74 ms] | 61.59 ms [42.71 ms–85.75 ms] | 1.08 s [667.35 ms–1.41 s] | 38.93 ms [26.27 ms–48.68 ms] | 718.54 ms [513.50 ms–938.81 ms] | 336.63 ms [227.27 ms–412.72 ms] | 113.06 ms [72.73 ms–148.36 ms] | 26.8 µs |
| 23 | 347.3 µs [309.8 µs–387.5 µs] | 29.92 ms [21.07 ms–46.01 ms] | 175.57 ms [155.78 ms–203.72 ms] | 429.14 ms [293.99 ms–638.09 ms] | skipped ceiling | 254.89 ms [178.45 ms–401.33 ms] | skipped ceiling | budget (pilot 4.07 s) | 757.50 ms [583.70 ms–1.30 s] | 38.4 µs |
| 26 | 305.3 µs [301.4 µs–317.0 µs] | 117.78 ms [71.93 ms–154.19 ms] | 478.13 ms [394.51 ms–545.10 ms] | budget (pilot 4.27 s) | skipped ceiling | budget (pilot 4.41 s) | skipped ceiling | skipped ceiling | skipped ceiling | 45.4 µs |
| 30 | 355.9 µs [292.2 µs–363.9 µs] | 474.16 ms [405.99 ms–622.90 ms] | 2.30 s [1.90 s–2.61 s] | skipped predicted budget | skipped ceiling | skipped ceiling | skipped ceiling | skipped ceiling | skipped ceiling | 77.0 µs |
| 33 | 608.0 µs [598.4 µs–627.6 µs] | 1.21 s [843.66 ms–1.53 s] | 7.82 s [6.76 s–8.13 s] | skipped ceiling | skipped ceiling | skipped ceiling | skipped ceiling | skipped ceiling | skipped ceiling | 125.2 µs |
| 36 | 680.1 µs [615.0 µs–722.5 µs] | 3.73 s [3.14 s–5.34 s] | 22.94 s [22.39 s–27.79 s] | skipped ceiling | skipped ceiling | skipped ceiling | skipped ceiling | skipped ceiling | skipped ceiling | 169.6 µs |
| 40 | 982.5 µs [909.1 µs–1.40 ms] | 16.00 s [14.20 s–16.95 s] | budget (pilot 102 s) | skipped ceiling | skipped ceiling | skipped ceiling | skipped ceiling | skipped ceiling | skipped ceiling | 292.5 µs |
| 48 | 2.17 ms [1.86 ms–2.63 ms] | skipped ceiling | skipped ceiling | skipped ceiling | skipped ceiling | skipped ceiling | skipped ceiling | skipped ceiling | skipped ceiling | 1.33 ms |
| 56 | 6.68 ms [5.78 ms–7.53 ms] | skipped ceiling | skipped ceiling | skipped ceiling | skipped ceiling | skipped ceiling | skipped ceiling | skipped ceiling | skipped ceiling | 6.27 ms |
| 62 | 133.69 ms [115.75 ms–194.87 ms] | skipped ceiling | skipped ceiling | skipped ceiling | skipped ceiling | skipped ceiling | skipped ceiling | skipped ceiling | skipped ceiling | 116.58 ms |

Each instance is a new prime p in [2^(bits-1), 2^bits), a new curve and a new pole. cmcs_frozen includes the exact trace (PARI ellap: baby-step/giant-step below ~30 digits), validation and translation sessions; the TRACE column is the trace alone, measured on separate fresh instances of the same class. Square-root comparators (bgs_*) and cmcs at >= 30 bits use the declared 60 s extended budget; others 2 s.

### W7 exceptional traces tau = chi(f(a)) = +-1 (CM-constructed curves; median per query)

| group | cmcs_frozen | cmcs_frozen[trace supplied] | voloch_semaev | bgs_harvey |
|---|---|---|---|---|
| b24_d3_exc | 235.5 µs [231.2 µs–258.9 µs] | 234.4 µs [221.5 µs–246.7 µs] | 55.5 µs [51.8 µs–69.8 µs] | 20.06 ms [13.25 ms–33.92 ms] |
| b32_d3_exc | 508.1 µs [485.3 µs–568.4 µs] | 642.9 µs [476.3 µs–674.6 µs] | 112.5 µs [108.5 µs–123.3 µs] | 357.46 ms [259.25 ms–583.51 ms] |
| b40_d3_exc | 543.0 µs [529.1 µs–600.0 µs] | 424.6 µs [413.1 µs–453.7 µs] | 130.6 µs [116.9 µs–178.4 µs] | 10.17 s [4.26 s–10.45 s] |
| b48_d3_exc | 731.7 µs [699.2 µs–791.3 µs] | 633.4 µs [538.4 µs–735.8 µs] | 317.8 µs [199.8 µs–413.1 µs] | skipped ceiling |
| b56_d3_exc | 650.3 µs [633.1 µs–760.0 µs] | 658.0 µs [614.0 µs–727.4 µs] | 222.4 µs [210.5 µs–316.2 µs] | skipped ceiling |
| b62_d3_exc | 1.04 ms [1.01 ms–1.16 ms] | 1.07 ms [981.0 µs–1.16 ms] | 376.6 µs [358.5 µs–529.1 µs] | skipped ceiling |
| b24_d4_exc | 236.4 µs [225.0 µs–263.9 µs] | 242.0 µs [234.2 µs–258.9 µs] | 50.2 µs [47.8 µs–59.2 µs] | 43.49 ms [30.70 ms–61.22 ms] |
| b32_d4_exc | 560.2 µs [525.2 µs–667.4 µs] | 403.5 µs [390.0 µs–481.3 µs] | 118.3 µs [114.2 µs–211.9 µs] | 866.38 ms [784.00 ms–1.33 s] |
| b40_d4_exc | 535.7 µs [509.9 µs–566.2 µs] | 488.5 µs [453.0 µs–540.8 µs] | 143.9 µs [142.2 µs–151.5 µs] | 19.32 s [16.54 s–20.26 s] |
| b48_d4_exc | 671.1 µs [624.0 µs–987.1 µs] | 635.4 µs [601.7 µs–719.1 µs] | 188.0 µs [181.6 µs–210.9 µs] | skipped ceiling |
| b56_d4_exc | 805.3 µs [781.9 µs–889.9 µs] | 794.6 µs [735.6 µs–835.6 µs] | 266.1 µs [252.1 µs–278.4 µs] | skipped ceiling |
| b62_d4_exc | 1.06 ms [886.8 µs–1.13 ms] | 1.04 ms [982.9 µs–1.12 ms] | 309.7 µs [302.3 µs–376.5 µs] | skipped ceiling |

PARI ellap recognises CM by a principal order and uses its O(log q)^2 formula here, so the cmcs_frozen trace cost is not representative of general curves. voloch_semaev receives the hypothesis tau = +-1 for free (known-trace family assumption), as does cmcs_frozen[trace supplied].

### W2 prepared curve: fixed (p, f), Q distinct admissible poles (medians over 5 fresh curves)

| group | method | preparation | query | total per block | peak RSS above imports | output validation |
|---|---|---|---|---|---|---|
| b16_d3_Q1 | cmcs_frozen | 143.2 µs | 204.7 µs/query | 347.9 µs | 2 MiB | consensus |
| b16_d3_Q1 | cmcs_frozen[trace supplied] | 168.2 µs | 200.0 µs/query | 368.1 µs | 2 MiB | consensus |
| b16_d3_Q1 | flint_power | 6.70 ms | 27.5 µs/query | 6.72 ms | 0 MiB | consensus |
| b16_d3_Q1 | flint_power+multipoint | 6.70 ms | 3.93 ms/query | 10.63 ms | 0 MiB | consensus |
| b16_d3_Q1 | polyrec_c | 2.51 ms | 48.2 µs/query | 2.57 ms | 10 MiB | consensus |
| b16_d3_Q1 | polyrec_c+multipoint | 2.38 ms | 3.84 ms/query | 6.18 ms | 12 MiB | consensus |
| b16_d3_Q1 | enum_conv | 30.59 ms | 6.3 µs/query | 30.59 ms | 21 MiB | consensus |
| b16_d3_Q1 | enum_c | 140.7 µs | 1.90 ms/query | 2.04 ms | 0 MiB | consensus |
| b16_d3_Q1 | linrec_c | 8.2 µs | 1.56 ms/query | 1.57 ms | 0 MiB | consensus |
| b16_d3_Q1 | bgs_harvey | 8.6 µs | 3.25 ms/query | 3.26 ms | 2 MiB | consensus |
| b16_d3_Q1 | bgs07 | 9.6 µs | 13.47 ms/query | 13.48 ms | 9 MiB | consensus |
| b16_d3_Q8 | cmcs_frozen | 119.9 µs | 107.1 µs/query | 971.9 µs | 2 MiB | consensus |
| b16_d3_Q8 | cmcs_frozen[trace supplied] | 156.7 µs | 127.3 µs/query | 1.20 ms | 2 MiB | consensus |
| b16_d3_Q8 | flint_power | 9.00 ms | 17.3 µs/query | 9.12 ms | 0 MiB | consensus |
| b16_d3_Q8 | flint_power+multipoint | 8.52 ms | 825.8 µs/query | 15.12 ms | 0 MiB | consensus |
| b16_d3_Q8 | polyrec_c | 2.33 ms | 16.5 µs/query | 2.46 ms | 10 MiB | consensus |
| b16_d3_Q8 | polyrec_c+multipoint | 2.90 ms | 747.3 µs/query | 8.88 ms | 12 MiB | consensus |
| b16_d3_Q8 | enum_conv | 30.78 ms | 1.3 µs/query | 30.78 ms | 22 MiB | consensus |
| b16_d3_Q8 | enum_c | 129.8 µs | 1.62 ms/query | 13.11 ms | 0 MiB | consensus |
| b16_d3_Q8 | linrec_c | 7.3 µs | 1.50 ms/query | 12.01 ms | 0 MiB | consensus |
| b16_d3_Q8 | bgs_harvey | 9.6 µs | 1.91 ms/query | 15.30 ms | 2 MiB | consensus |
| b16_d3_Q8 | bgs07 | 11.4 µs | 13.21 ms/query | 105.69 ms | 9 MiB | consensus |
| b16_d3_Q64 | cmcs_frozen | 186.8 µs | 117.4 µs/query | 7.70 ms | 2 MiB | consensus |
| b16_d3_Q64 | cmcs_frozen[trace supplied] | 139.1 µs | 89.1 µs/query | 6.03 ms | 2 MiB | consensus |
| b16_d3_Q64 | flint_power | 9.62 ms | 15.6 µs/query | 10.62 ms | 0 MiB | consensus |
| b16_d3_Q64 | flint_power+multipoint | 7.29 ms | 186.2 µs/query | 19.21 ms | 0 MiB | consensus |
| b16_d3_Q64 | polyrec_c | 3.20 ms | 17.6 µs/query | 4.36 ms | 10 MiB | consensus |
| b16_d3_Q64 | polyrec_c+multipoint | 2.47 ms | 195.3 µs/query | 14.96 ms | 13 MiB | consensus |
| b16_d3_Q64 | enum_conv | 35.72 ms | 0.4 µs/query | 35.75 ms | 22 MiB | consensus |
| b16_d3_Q64 | enum_c | 131.2 µs | 1.69 ms/query | 108.40 ms | 0 MiB | consensus |
| b16_d3_Q64 | linrec_c | 11.1 µs | 1.70 ms/query | 108.62 ms | 0 MiB | consensus |
| b16_d3_Q64 | bgs_harvey | 10.3 µs | 1.48 ms/query | 94.78 ms | 2 MiB | consensus |
| b16_d3_Q64 | bgs07 | 10.8 µs | 13.89 ms/query | 889.09 ms | 9 MiB | consensus |
| b16_d3_Q512 | cmcs_frozen | 195.7 µs | 115.0 µs/query | 59.10 ms | 2 MiB | consensus |
| b16_d3_Q512 | cmcs_frozen[trace supplied] | 284.6 µs | 107.2 µs/query | 56.89 ms | 2 MiB | consensus |
| b16_d3_Q512 | flint_power | 6.89 ms | 12.1 µs/query | 13.09 ms | 0 MiB | consensus |
| b16_d3_Q512 | flint_power+multipoint | 6.84 ms | 25.6 µs/query | 19.93 ms | 0 MiB | consensus |
| b16_d3_Q512 | polyrec_c | 2.81 ms | 12.7 µs/query | 9.29 ms | 9 MiB | consensus |
| b16_d3_Q512 | polyrec_c+multipoint | 1.99 ms | 24.3 µs/query | 14.42 ms | 12 MiB | consensus |
| b16_d3_Q512 | enum_conv | 26.92 ms | 0.2 µs/query | 27.03 ms | 22 MiB | consensus |
| b16_d3_Q512 | enum_c | 176.8 µs | 1.62 ms/query | 828.19 ms | 0 MiB | consensus |
| b16_d3_Q512 | linrec_c | 10.5 µs | 1.44 ms/query | 737.43 ms | 0 MiB | consensus |
| b16_d3_Q512 | bgs_harvey | 13.4 µs | 1.24 ms/query | 635.09 ms | 2 MiB | consensus |
| b16_d3_Q512 | bgs07 | 10.6 µs | 12.54 ms/query | 6.42 s | 9 MiB | consensus |
| b16_d4_Q1 | cmcs_frozen | 181.2 µs | 216.6 µs/query | 387.4 µs | 2 MiB | consensus |
| b16_d4_Q1 | cmcs_frozen[trace supplied] | 184.7 µs | 246.5 µs/query | 463.4 µs | 2 MiB | consensus |
| b16_d4_Q1 | flint_power | 9.49 ms | 37.9 µs/query | 9.53 ms | 0 MiB | consensus |
| b16_d4_Q1 | flint_power+multipoint | 12.14 ms | 9.31 ms/query | 21.45 ms | 0 MiB | consensus |
| b16_d4_Q1 | polyrec_c | 5.53 ms | 76.4 µs/query | 5.59 ms | 10 MiB | consensus |
| b16_d4_Q1 | polyrec_c+multipoint | 5.82 ms | 8.27 ms/query | 14.08 ms | 13 MiB | consensus |
| b16_d4_Q1 | enum_conv | 28.15 ms | 5.6 µs/query | 28.16 ms | 19 MiB | consensus |
| b16_d4_Q1 | enum_c | 164.1 µs | 2.15 ms/query | 2.32 ms | 0 MiB | consensus |
| b16_d4_Q1 | linrec_c | 7.0 µs | 3.21 ms/query | 3.22 ms | 0 MiB | consensus |
| b16_d4_Q1 | bgs_harvey | 17.0 µs | 5.90 ms/query | 5.92 ms | 2 MiB | consensus |
| b16_d4_Q1 | bgs07 | 11.6 µs | 25.12 ms/query | 25.13 ms | 9 MiB | consensus |
| b16_d4_Q8 | cmcs_frozen | 197.2 µs | 163.7 µs/query | 1.71 ms | 2 MiB | consensus |
| b16_d4_Q8 | cmcs_frozen[trace supplied] | 160.1 µs | 112.5 µs/query | 1.11 ms | 2 MiB | consensus |
| b16_d4_Q8 | flint_power | 16.66 ms | 26.4 µs/query | 16.91 ms | 0 MiB | consensus |
| b16_d4_Q8 | flint_power+multipoint | 13.79 ms | 1.71 ms/query | 27.50 ms | 1 MiB | consensus |
| b16_d4_Q8 | polyrec_c | 7.47 ms | 37.7 µs/query | 7.79 ms | 11 MiB | consensus |
| b16_d4_Q8 | polyrec_c+multipoint | 6.89 ms | 1.57 ms/query | 19.42 ms | 14 MiB | consensus |
| b16_d4_Q8 | enum_conv | 35.94 ms | 1.6 µs/query | 35.95 ms | 22 MiB | consensus |
| b16_d4_Q8 | enum_c | 152.8 µs | 2.46 ms/query | 19.87 ms | 0 MiB | consensus |
| b16_d4_Q8 | linrec_c | 8.9 µs | 3.64 ms/query | 29.12 ms | 0 MiB | consensus |
| b16_d4_Q8 | bgs_harvey | 12.3 µs | 4.21 ms/query | 33.70 ms | 2 MiB | consensus |
| b16_d4_Q8 | bgs07 | 10.4 µs | 26.08 ms/query | 208.67 ms | 9 MiB | consensus |
| b16_d4_Q64 | cmcs_frozen | 168.8 µs | 108.8 µs/query | 7.16 ms | 2 MiB | consensus |
| b16_d4_Q64 | cmcs_frozen[trace supplied] | 178.5 µs | 123.0 µs/query | 8.15 ms | 2 MiB | consensus |
| b16_d4_Q64 | flint_power | 11.59 ms | 23.7 µs/query | 13.11 ms | 0 MiB | consensus |
| b16_d4_Q64 | flint_power+multipoint | 10.48 ms | 420.6 µs/query | 37.39 ms | 2 MiB | consensus |
| b16_d4_Q64 | polyrec_c | 7.20 ms | 28.7 µs/query | 9.14 ms | 11 MiB | consensus |
| b16_d4_Q64 | polyrec_c+multipoint | 6.13 ms | 426.3 µs/query | 33.41 ms | 16 MiB | consensus |
| b16_d4_Q64 | enum_conv | 30.72 ms | 0.4 µs/query | 30.77 ms | 21 MiB | consensus |
| b16_d4_Q64 | enum_c | 157.5 µs | 2.00 ms/query | 128.44 ms | 0 MiB | consensus |
| b16_d4_Q64 | linrec_c | 11.4 µs | 3.65 ms/query | 233.48 ms | 0 MiB | consensus |
| b16_d4_Q64 | bgs_harvey | 16.4 µs | 3.79 ms/query | 242.72 ms | 2 MiB | consensus |
| b16_d4_Q64 | bgs07 | 11.3 µs | 28.22 ms/query | 1.81 s | 9 MiB | consensus |
| b16_d4_Q512 | cmcs_frozen | 246.7 µs | 109.4 µs/query | 56.24 ms | 2 MiB | consensus |
| b16_d4_Q512 | cmcs_frozen[trace supplied] | 235.6 µs | 90.8 µs/query | 46.70 ms | 2 MiB | consensus |
| b16_d4_Q512 | flint_power | 7.98 ms | 17.3 µs/query | 15.47 ms | 0 MiB | consensus |
| b16_d4_Q512 | flint_power+multipoint | 8.73 ms | 46.9 µs/query | 31.83 ms | 1 MiB | consensus |
| b16_d4_Q512 | polyrec_c | 5.09 ms | 18.6 µs/query | 14.60 ms | 11 MiB | consensus |
| b16_d4_Q512 | polyrec_c+multipoint | 4.62 ms | 56.3 µs/query | 33.43 ms | 15 MiB | consensus |
| b16_d4_Q512 | enum_conv | 18.71 ms | 0.2 µs/query | 18.80 ms | 21 MiB | consensus |
| b16_d4_Q512 | enum_c | 168.1 µs | 1.70 ms/query | 870.96 ms | 0 MiB | consensus |
| b16_d4_Q512 | linrec_c | 9.9 µs | 3.31 ms/query | 1.70 s | 0 MiB | consensus |
| b16_d4_Q512 | bgs_harvey | 17.2 µs | 2.78 ms/query | 1.42 s | 2 MiB | consensus |
| b16_d4_Q512 | bgs07 | 11.5 µs | 24.25 ms/query | 12.42 s | 9 MiB | consensus |
| b20_d3_Q1 | cmcs_frozen | 207.7 µs | 226.7 µs/query | 436.3 µs | 2 MiB | consensus |
| b20_d3_Q1 | cmcs_frozen[trace supplied] | 158.2 µs | 204.3 µs/query | 370.4 µs | 2 MiB | consensus |
| b20_d3_Q1 | flint_power | 228.49 ms | 321.4 µs/query | 228.81 ms | 43 MiB | consensus |
| b20_d3_Q1 | flint_power+multipoint | 226.94 ms | 76.93 ms/query | 301.99 ms | 56 MiB | consensus |
| b20_d3_Q1 | polyrec_c | 56.56 ms | 569.9 µs/query | 57.23 ms | 35 MiB | consensus |
| b20_d3_Q1 | polyrec_c+multipoint | 46.81 ms | 77.08 ms/query | 124.25 ms | 63 MiB | consensus |
| b20_d3_Q1 | enum_conv | 700.86 ms | 12.0 µs/query | 700.88 ms | 227 MiB | consensus |
| b20_d3_Q1 | enum_c | 1.23 ms | 28.67 ms/query | 29.91 ms | 0 MiB | consensus |
| b20_d3_Q1 | linrec_c | 8.7 µs | 27.37 ms/query | 27.38 ms | 0 MiB | consensus |
| b20_d3_Q1 | bgs_harvey | 10.9 µs | 7.03 ms/query | 7.04 ms | 2 MiB | consensus |
| b20_d3_Q1 | bgs07 | 10.5 µs | 32.55 ms/query | 32.56 ms | 9 MiB | consensus |
| b20_d3_Q8 | cmcs_frozen | 157.8 µs | 157.9 µs/query | 1.42 ms | 2 MiB | consensus |
| b20_d3_Q8 | cmcs_frozen[trace supplied] | 124.1 µs | 126.1 µs/query | 1.13 ms | 2 MiB | consensus |
| b20_d3_Q8 | flint_power | 235.12 ms | 267.9 µs/query | 237.69 ms | 45 MiB | consensus |
| b20_d3_Q8 | flint_power+multipoint | 226.77 ms | 13.72 ms/query | 318.42 ms | 55 MiB | consensus |
| b20_d3_Q8 | polyrec_c | 51.53 ms | 342.3 µs/query | 54.06 ms | 34 MiB | consensus |
| b20_d3_Q8 | polyrec_c+multipoint | 41.58 ms | 10.61 ms/query | 126.46 ms | 62 MiB | consensus |
| b20_d3_Q8 | enum_conv | 662.80 ms | 2.5 µs/query | 662.82 ms | 222 MiB | consensus |
| b20_d3_Q8 | enum_c | 1.34 ms | 32.57 ms/query | 262.04 ms | 0 MiB | consensus |
| b20_d3_Q8 | linrec_c | 10.3 µs | 22.30 ms/query | 178.44 ms | 0 MiB | consensus |
| b20_d3_Q8 | bgs_harvey | 12.0 µs | 6.13 ms/query | 49.05 ms | 2 MiB | consensus |
| b20_d3_Q8 | bgs07 | 10.0 µs | 29.01 ms/query | 232.08 ms | 9 MiB | consensus |
| b20_d3_Q64 | cmcs_frozen | 179.7 µs | 140.4 µs/query | 9.17 ms | 2 MiB | consensus |
| b20_d3_Q64 | cmcs_frozen[trace supplied] | 167.6 µs | 130.9 µs/query | 8.54 ms | 2 MiB | consensus |
| b20_d3_Q64 | flint_power | 280.60 ms | 332.6 µs/query | 301.88 ms | 44 MiB | consensus |
| b20_d3_Q64 | flint_power+multipoint | 262.39 ms | 5.67 ms/query | 625.41 ms | 53 MiB | consensus |
| b20_d3_Q64 | polyrec_c | 53.38 ms | 311.9 µs/query | 73.34 ms | 35 MiB | consensus |
| b20_d3_Q64 | polyrec_c+multipoint | 54.53 ms | 6.09 ms/query | 443.99 ms | 62 MiB | consensus |
| b20_d3_Q64 | enum_conv | 642.06 ms | 1.0 µs/query | 642.12 ms | 220 MiB | consensus |
| b20_d3_Q64 | enum_c | 1.43 ms | 32.40 ms/query | 2.08 s | 0 MiB | consensus |
| b20_d3_Q64 | linrec_c | 9.9 µs | 24.06 ms/query | 1.54 s | 0 MiB | consensus |
| b20_d3_Q64 | bgs_harvey | 11.0 µs | 6.18 ms/query | 395.38 ms | 2 MiB | consensus |
| b20_d3_Q64 | bgs07 | 10.9 µs | 33.70 ms/query | 2.16 s | 9 MiB | consensus |
| b20_d3_Q512 | cmcs_frozen | 210.6 µs | 115.6 µs/query | 59.40 ms | 2 MiB | consensus |
| b20_d3_Q512 | cmcs_frozen[trace supplied] | 313.6 µs | 132.2 µs/query | 74.92 ms | 2 MiB | consensus |
| b20_d3_Q512 | flint_power | 237.83 ms | 260.1 µs/query | 399.38 ms | 41 MiB | consensus |
| b20_d3_Q512 | flint_power+multipoint | 221.96 ms | 629.7 µs/query | 544.34 ms | 52 MiB | consensus |
| b20_d3_Q512 | polyrec_c | 48.63 ms | 282.9 µs/query | 193.49 ms | 33 MiB | consensus |
| b20_d3_Q512 | polyrec_c+multipoint | 50.24 ms | 802.6 µs/query | 461.20 ms | 64 MiB | consensus |
| b20_d3_Q512 | enum_conv | 742.23 ms | 0.8 µs/query | 742.64 ms | 235 MiB | consensus |
| b20_d3_Q512 | enum_c | 1.44 ms | 32.20 ms/query | 16.49 s | 0 MiB | consensus |
| b20_d3_Q512 | linrec_c | 10.5 µs | 23.87 ms/query | 12.22 s | 0 MiB | consensus |
| b20_d3_Q512 | bgs_harvey | 12.2 µs | 5.84 ms/query | 2.99 s | 2 MiB | consensus |
| b20_d3_Q512 | bgs07 | 11.6 µs | 33.83 ms/query | 17.32 s | 9 MiB | consensus |
| b20_d4_Q1 | cmcs_frozen | 172.9 µs | 226.7 µs/query | 412.1 µs | 2 MiB | consensus |
| b20_d4_Q1 | cmcs_frozen[trace supplied] | 170.1 µs | 215.0 µs/query | 385.1 µs | 2 MiB | consensus |
| b20_d4_Q1 | flint_power | 335.80 ms | 951.8 µs/query | 337.04 ms | 66 MiB | consensus |
| b20_d4_Q1 | flint_power+multipoint | 304.56 ms | 158.44 ms/query | 459.60 ms | 113 MiB | consensus |
| b20_d4_Q1 | polyrec_c | 89.29 ms | 1.04 ms/query | 90.41 ms | 61 MiB | consensus |
| b20_d4_Q1 | polyrec_c+multipoint | 105.75 ms | 158.39 ms/query | 254.68 ms | 120 MiB | consensus |
| b20_d4_Q1 | enum_conv | 617.17 ms | 12.3 µs/query | 617.18 ms | 218 MiB | consensus |
| b20_d4_Q1 | enum_c | 1.56 ms | 40.02 ms/query | 41.58 ms | 0 MiB | consensus |
| b20_d4_Q1 | linrec_c | 10.4 µs | 55.98 ms/query | 55.99 ms | 0 MiB | consensus |
| b20_d4_Q1 | bgs_harvey | 9.9 µs | 13.62 ms/query | 13.63 ms | 2 MiB | consensus |
| b20_d4_Q1 | bgs07 | 11.4 µs | 67.79 ms/query | 67.80 ms | 9 MiB | consensus |
| b20_d4_Q8 | cmcs_frozen | 177.5 µs | 163.5 µs/query | 1.50 ms | 2 MiB | consensus |
| b20_d4_Q8 | cmcs_frozen[trace supplied] | 158.5 µs | 140.4 µs/query | 1.33 ms | 2 MiB | consensus |
| b20_d4_Q8 | flint_power | 353.59 ms | 524.7 µs/query | 357.78 ms | 65 MiB | consensus |
| b20_d4_Q8 | flint_power+multipoint | 303.39 ms | 27.20 ms/query | 521.01 ms | 102 MiB | consensus |
| b20_d4_Q8 | polyrec_c | 118.31 ms | 704.7 µs/query | 123.95 ms | 61 MiB | consensus |
| b20_d4_Q8 | polyrec_c+multipoint | 120.68 ms | 29.03 ms/query | 359.50 ms | 117 MiB | consensus |
| b20_d4_Q8 | enum_conv | 718.64 ms | 2.2 µs/query | 718.66 ms | 244 MiB | consensus |
| b20_d4_Q8 | enum_c | 1.31 ms | 33.62 ms/query | 270.24 ms | 0 MiB | consensus |
| b20_d4_Q8 | linrec_c | 12.6 µs | 64.66 ms/query | 517.31 ms | 0 MiB | consensus |
| b20_d4_Q8 | bgs_harvey | 13.5 µs | 14.60 ms/query | 116.79 ms | 3 MiB | consensus |
| b20_d4_Q8 | bgs07 | 12.1 µs | 70.50 ms/query | 563.98 ms | 9 MiB | consensus |
| b20_d4_Q64 | cmcs_frozen | 169.6 µs | 123.6 µs/query | 8.11 ms | 2 MiB | consensus |
| b20_d4_Q64 | cmcs_frozen[trace supplied] | 188.9 µs | 125.1 µs/query | 8.19 ms | 2 MiB | consensus |
| b20_d4_Q64 | flint_power | 307.14 ms | 534.1 µs/query | 341.32 ms | 62 MiB | consensus |
| b20_d4_Q64 | flint_power+multipoint | 338.02 ms | 12.26 ms/query | 1.13 s | 116 MiB | consensus |
| b20_d4_Q64 | polyrec_c | 116.29 ms | 547.2 µs/query | 151.31 ms | 62 MiB | consensus |
| b20_d4_Q64 | polyrec_c+multipoint | 115.75 ms | 14.02 ms/query | 1.01 s | 122 MiB | consensus |
| b20_d4_Q64 | enum_conv | 642.50 ms | 1.1 µs/query | 642.57 ms | 224 MiB | consensus |
| b20_d4_Q64 | enum_c | 1.26 ms | 37.90 ms/query | 2.43 s | 0 MiB | consensus |
| b20_d4_Q64 | linrec_c | 10.6 µs | 56.77 ms/query | 3.63 s | 0 MiB | consensus |
| b20_d4_Q64 | bgs_harvey | 12.9 µs | 12.08 ms/query | 773.00 ms | 2 MiB | consensus |
| b20_d4_Q64 | bgs07 | 10.5 µs | 77.78 ms/query | 4.98 s | 10 MiB | consensus |
| b20_d4_Q512 | cmcs_frozen | 262.1 µs | 141.0 µs/query | 72.47 ms | 2 MiB | consensus |
| b20_d4_Q512 | cmcs_frozen[trace supplied] | 228.8 µs | 117.2 µs/query | 62.03 ms | 2 MiB | consensus |
| b20_d4_Q512 | flint_power | 345.26 ms | 596.3 µs/query | 650.58 ms | 63 MiB | consensus |
| b20_d4_Q512 | flint_power+multipoint | 338.36 ms | 1.61 ms/query | 1.16 s | 98 MiB | consensus |
| b20_d4_Q512 | polyrec_c | 138.48 ms | 617.4 µs/query | 454.59 ms | 59 MiB | consensus |
| b20_d4_Q512 | polyrec_c+multipoint | 130.59 ms | 1.90 ms/query | 1.10 s | 122 MiB | consensus |
| b20_d4_Q512 | enum_conv | 740.09 ms | 0.7 µs/query | 740.47 ms | 221 MiB | consensus |
| b20_d4_Q512 | enum_c | 1.60 ms | 40.00 ms/query | 20.48 s | 0 MiB | consensus |
| b20_d4_Q512 | linrec_c | — | — | budget (pilot 21.2 s) | — |  |
| b20_d4_Q512 | bgs_harvey | 12.5 µs | 15.05 ms/query | 7.71 s | 2 MiB | consensus |
| b20_d4_Q512 | bgs07 | — | — | budget (pilot 32.4 s) | — |  |
| b23_d3_Q1 | cmcs_frozen | 175.7 µs | 284.9 µs/query | 480.8 µs | 2 MiB | consensus |
| b23_d3_Q1 | cmcs_frozen[trace supplied] | 223.6 µs | 309.5 µs/query | 515.4 µs | 2 MiB | consensus |
| b23_d3_Q1 | flint_power | 3.61 s | 4.85 ms/query | 3.62 s | 362 MiB | consensus |
| b23_d3_Q1 | flint_power+multipoint | 3.81 s | 809.53 ms/query | 4.62 s | 419 MiB | consensus |
| b23_d3_Q1 | polyrec_c | 488.67 ms | 4.88 ms/query | 494.18 ms | 238 MiB | consensus |
| b23_d3_Q1 | polyrec_c+multipoint | 459.90 ms | 1.05 s/query | 1.51 s | 459 MiB | consensus |
| b23_d3_Q1 | enum_conv | — | — | skipped_ceiling | — |  |
| b23_d3_Q1 | enum_c | 10.98 ms | 269.51 ms/query | 283.20 ms | 0 MiB | consensus |
| b23_d3_Q1 | linrec_c | 11.6 µs | 206.37 ms/query | 206.38 ms | 0 MiB | consensus |
| b23_d3_Q1 | bgs_harvey | 11.6 µs | 16.02 ms/query | 16.03 ms | 2 MiB | consensus |
| b23_d3_Q1 | bgs07 | 13.1 µs | 95.86 ms/query | 95.87 ms | 10 MiB | consensus |
| b23_d3_Q8 | cmcs_frozen | 178.9 µs | 172.6 µs/query | 1.56 ms | 2 MiB | consensus |
| b23_d3_Q8 | cmcs_frozen[trace supplied] | 176.1 µs | 175.5 µs/query | 1.61 ms | 2 MiB | consensus |
| b23_d3_Q8 | flint_power | 1.96 s | 2.44 ms/query | 1.98 s | 316 MiB | consensus |
| b23_d3_Q8 | flint_power+multipoint | 2.11 s | 83.24 ms/query | 2.74 s | 327 MiB | consensus |
| b23_d3_Q8 | polyrec_c | 395.77 ms | 2.62 ms/query | 416.71 ms | 204 MiB | consensus |
| b23_d3_Q8 | polyrec_c+multipoint | 360.63 ms | 92.90 ms/query | 1.10 s | 368 MiB | consensus |
| b23_d3_Q8 | enum_conv | — | — | skipped_ceiling | — |  |
| b23_d3_Q8 | enum_c | 9.74 ms | 228.18 ms/query | 1.84 s | 0 MiB | consensus |
| b23_d3_Q8 | linrec_c | 13.2 µs | 139.23 ms/query | 1.11 s | 0 MiB | consensus |
| b23_d3_Q8 | bgs_harvey | 21.2 µs | 15.52 ms/query | 124.21 ms | 2 MiB | consensus |
| b23_d3_Q8 | bgs07 | 11.1 µs | 86.89 ms/query | 695.15 ms | 10 MiB | consensus |
| b23_d3_Q64 | cmcs_frozen | 188.7 µs | 161.2 µs/query | 10.50 ms | 2 MiB | consensus |
| b23_d3_Q64 | cmcs_frozen[trace supplied] | 184.2 µs | 169.2 µs/query | 11.03 ms | 2 MiB | consensus |
| b23_d3_Q64 | flint_power | 3.55 s | 1.78 ms/query | 3.66 s | 354 MiB | consensus |
| b23_d3_Q64 | flint_power+multipoint | 3.73 s | 70.98 ms/query | 8.30 s | 532 MiB | consensus |
| b23_d3_Q64 | polyrec_c | 407.77 ms | 1.70 ms/query | 516.50 ms | 227 MiB | consensus |
| b23_d3_Q64 | polyrec_c+multipoint | 419.39 ms | 71.95 ms/query | 5.07 s | 560 MiB | consensus |
| b23_d3_Q64 | enum_conv | — | — | skipped_ceiling | — |  |
| b23_d3_Q64 | enum_c | 9.08 ms | 272.45 ms/query | 17.45 s | 0 MiB | consensus |
| b23_d3_Q64 | linrec_c | 13.1 µs | 191.22 ms/query | 12.24 s | 0 MiB | consensus |
| b23_d3_Q64 | bgs_harvey | 12.4 µs | 12.37 ms/query | 791.79 ms | 3 MiB | consensus |
| b23_d3_Q64 | bgs07 | 10.7 µs | 86.20 ms/query | 5.52 s | 10 MiB | consensus |
| b23_d3_Q512 | cmcs_frozen | 232.4 µs | 164.6 µs/query | 84.48 ms | 2 MiB | consensus |
| b23_d3_Q512 | cmcs_frozen[trace supplied] | 351.2 µs | 147.5 µs/query | 76.53 ms | 2 MiB | consensus |
| b23_d3_Q512 | flint_power | 3.07 s | 1.59 ms/query | 3.92 s | 381 MiB | consensus |
| b23_d3_Q512 | flint_power+multipoint | 2.99 s | 7.72 ms/query | 6.94 s | 533 MiB | consensus |
| b23_d3_Q512 | polyrec_c | 295.59 ms | 1.83 ms/query | 1.21 s | 229 MiB | consensus |
| b23_d3_Q512 | polyrec_c+multipoint | 330.60 ms | 7.87 ms/query | 4.35 s | 542 MiB | consensus |
| b23_d3_Q512 | enum_conv | — | — | skipped_ceiling | — |  |
| b23_d3_Q512 | enum_c | — | — | budget (pilot 178 s) | — |  |
| b23_d3_Q512 | linrec_c | — | — | budget (pilot 121 s) | — |  |
| b23_d3_Q512 | bgs_harvey | 12.1 µs | 12.94 ms/query | 6.63 s | 3 MiB | consensus |
| b23_d3_Q512 | bgs07 | — | — | budget (pilot 51.4 s) | — |  |
| b23_d4_Q1 | cmcs_frozen | 154.2 µs | 210.5 µs/query | 352.2 µs | 2 MiB | consensus |
| b23_d4_Q1 | cmcs_frozen[trace supplied] | 180.3 µs | 264.9 µs/query | 449.5 µs | 2 MiB | consensus |
| b23_d4_Q1 | flint_power | 3.92 s | 6.33 ms/query | 3.93 s | 451 MiB | consensus |
| b23_d4_Q1 | flint_power+multipoint | 3.86 s | 1.22 s/query | 5.07 s | 723 MiB | consensus |
| b23_d4_Q1 | polyrec_c | 772.92 ms | 6.70 ms/query | 779.62 ms | 372 MiB | consensus |
| b23_d4_Q1 | polyrec_c+multipoint | 730.61 ms | 1.42 s/query | 2.15 s | 686 MiB | consensus |
| b23_d4_Q1 | enum_conv | — | — | skipped_ceiling | — |  |
| b23_d4_Q1 | enum_c | 9.81 ms | 255.27 ms/query | 265.08 ms | 0 MiB | consensus |
| b23_d4_Q1 | linrec_c | 10.1 µs | 380.09 ms/query | 380.13 ms | 0 MiB | consensus |
| b23_d4_Q1 | bgs_harvey | 12.9 µs | 31.36 ms/query | 31.37 ms | 3 MiB | consensus |
| b23_d4_Q1 | bgs07 | 11.1 µs | 171.28 ms/query | 171.29 ms | 12 MiB | consensus |
| b23_d4_Q8 | cmcs_frozen | 188.7 µs | 180.8 µs/query | 1.66 ms | 2 MiB | consensus |
| b23_d4_Q8 | cmcs_frozen[trace supplied] | 195.2 µs | 177.4 µs/query | 1.65 ms | 2 MiB | consensus |
| b23_d4_Q8 | flint_power | 3.46 s | 3.71 ms/query | 3.48 s | 491 MiB | consensus |
| b23_d4_Q8 | flint_power+multipoint | 3.58 s | 197.29 ms/query | 5.16 s | 854 MiB | consensus |
| b23_d4_Q8 | polyrec_c | 751.78 ms | 4.51 ms/query | 787.85 ms | 454 MiB | consensus |
| b23_d4_Q8 | polyrec_c+multipoint | 872.97 ms | 193.29 ms/query | 2.22 s | 838 MiB | consensus |
| b23_d4_Q8 | enum_conv | — | — | skipped_ceiling | — |  |
| b23_d4_Q8 | enum_c | 10.74 ms | 223.22 ms/query | 1.80 s | 0 MiB | consensus |
| b23_d4_Q8 | linrec_c | 14.3 µs | 371.08 ms/query | 2.97 s | 0 MiB | consensus |
| b23_d4_Q8 | bgs_harvey | 14.1 µs | 23.12 ms/query | 184.96 ms | 3 MiB | consensus |
| b23_d4_Q8 | bgs07 | 10.4 µs | 138.23 ms/query | 1.11 s | 12 MiB | consensus |
| b23_d4_Q64 | cmcs_frozen | 245.3 µs | 172.4 µs/query | 11.32 ms | 2 MiB | consensus |
| b23_d4_Q64 | cmcs_frozen[trace supplied] | 174.7 µs | 160.9 µs/query | 10.54 ms | 2 MiB | consensus |
| b23_d4_Q64 | flint_power | 5.05 s | 3.84 ms/query | 5.32 s | 517 MiB | consensus |
| b23_d4_Q64 | flint_power+multipoint | 5.11 s | 166.19 ms/query | 16.13 s | 1024 MiB | consensus |
| b23_d4_Q64 | polyrec_c | 1.11 s | 4.25 ms/query | 1.39 s | 427 MiB | consensus |
| b23_d4_Q64 | polyrec_c+multipoint | 1.10 s | 155.21 ms/query | 11.03 s | 977 MiB | consensus |
| b23_d4_Q64 | enum_conv | — | — | skipped_ceiling | — |  |
| b23_d4_Q64 | enum_c | 11.86 ms | 329.30 ms/query | 21.09 s | 0 MiB | consensus |
| b23_d4_Q64 | linrec_c | — | — | budget (pilot 25.2 s) | — |  |
| b23_d4_Q64 | bgs_harvey | 15.7 µs | 38.55 ms/query | 2.47 s | 3 MiB | consensus |
| b23_d4_Q64 | bgs07 | 11.5 µs | 173.89 ms/query | 11.13 s | 12 MiB | consensus |
| b23_d4_Q512 | cmcs_frozen | 274.5 µs | 162.3 µs/query | 83.36 ms | 2 MiB | consensus |
| b23_d4_Q512 | cmcs_frozen[trace supplied] | 324.7 µs | 177.3 µs/query | 94.78 ms | 2 MiB | consensus |
| b23_d4_Q512 | flint_power | 4.27 s | 3.13 ms/query | 5.88 s | 492 MiB | consensus |
| b23_d4_Q512 | flint_power+multipoint | 4.17 s | 17.44 ms/query | 13.10 s | 1107 MiB | consensus |
| b23_d4_Q512 | polyrec_c | 961.09 ms | 3.68 ms/query | 2.74 s | 454 MiB | consensus |
| b23_d4_Q512 | polyrec_c+multipoint | 793.22 ms | 15.54 ms/query | 8.67 s | 1116 MiB | consensus |
| b23_d4_Q512 | enum_conv | — | — | skipped_ceiling | — |  |
| b23_d4_Q512 | enum_c | — | — | budget (pilot 176 s) | — |  |
| b23_d4_Q512 | linrec_c | — | — | timeout | — |  |
| b23_d4_Q512 | bgs_harvey | — | — | budget (pilot 20.9 s) | — |  |
| b23_d4_Q512 | bgs07 | — | — | budget (pilot 94.2 s) | — |  |

query = per-pole time; total = preparation + all Q queries. cmcs_frozen acquires the trace in preparation; [trace supplied] is the workload assumption of a free trace.

### W5 dense queries: Q ~ p/16, p/4 or all admissible poles

| group | method | preparation | query | total per block | peak RSS above imports | output validation |
|---|---|---|---|---|---|---|
| b12_d3_Qp/16 | cmcs_frozen | 147.6 µs | 75.2 µs/query | 14.75 ms | 0 MiB | direct |
| b12_d3_Qp/16 | cmcs_frozen[trace supplied] | 179.3 µs | 84.9 µs/query | 16.85 ms | 0 MiB | direct |
| b12_d3_Qp/16 | flint_power+multipoint | 304.9 µs | 4.9 µs/query | 1.20 ms | 0 MiB | direct |
| b12_d3_Qp/16 | polyrec_c+multipoint | 276.8 µs | 5.6 µs/query | 1.31 ms | 0 MiB | direct |
| b12_d3_Qp/16 | enum_conv | 1.57 ms | 0.1 µs/query | 1.59 ms | 0 MiB | direct |
| b12_d3_Qp/16 | enum_c | 71.2 µs | 142.7 µs/query | 26.47 ms | 0 MiB | direct |
| b12_d3_Qp/16 | bgs_harvey | 14.6 µs | 418.1 µs/query | 83.78 ms | 2 MiB | direct |
| b12_d3_Qp/4 | cmcs_frozen | 161.6 µs | 79.4 µs/query | 53.29 ms | 0 MiB | direct |
| b12_d3_Qp/4 | cmcs_frozen[trace supplied] | 285.7 µs | 93.6 µs/query | 66.10 ms | 0 MiB | direct |
| b12_d3_Qp/4 | flint_power+multipoint | 297.0 µs | 3.8 µs/query | 2.89 ms | 0 MiB | direct |
| b12_d3_Qp/4 | polyrec_c+multipoint | 286.7 µs | 3.4 µs/query | 2.59 ms | 0 MiB | direct |
| b12_d3_Qp/4 | enum_conv | 1.65 ms | 0.1 µs/query | 1.70 ms | 0 MiB | direct |
| b12_d3_Qp/4 | enum_c | 86.9 µs | 110.5 µs/query | 75.36 ms | 0 MiB | direct |
| b12_d3_Qp/4 | bgs_harvey | 19.5 µs | 293.0 µs/query | 199.55 ms | 2 MiB | direct |
| b12_d3_Qp/1 | cmcs_frozen | 227.9 µs | 89.1 µs/query | 230.47 ms | 0 MiB | direct |
| b12_d3_Qp/1 | cmcs_frozen[trace supplied] | 254.5 µs | 80.9 µs/query | 208.87 ms | 0 MiB | direct |
| b12_d3_Qp/1 | flint_power+multipoint | 195.9 µs | 3.1 µs/query | 8.09 ms | 0 MiB | direct |
| b12_d3_Qp/1 | polyrec_c+multipoint | 277.4 µs | 2.9 µs/query | 7.94 ms | 0 MiB | direct |
| b12_d3_Qp/1 | enum_conv | 1.57 ms | 0.1 µs/query | 1.73 ms | 0 MiB | direct |
| b12_d3_Qp/1 | enum_c | 91.5 µs | 103.8 µs/query | 271.74 ms | 0 MiB | direct |
| b12_d3_Qp/1 | bgs_harvey | 13.7 µs | 452.2 µs/query | 1.04 s | 2 MiB | direct |
| b12_d4_Qp/16 | cmcs_frozen | 173.4 µs | 109.8 µs/query | 18.89 ms | 0 MiB | direct |
| b12_d4_Qp/16 | cmcs_frozen[trace supplied] | 207.0 µs | 87.8 µs/query | 20.75 ms | 0 MiB | direct |
| b12_d4_Qp/16 | flint_power+multipoint | 377.7 µs | 8.9 µs/query | 2.23 ms | 0 MiB | direct |
| b12_d4_Qp/16 | polyrec_c+multipoint | 486.2 µs | 8.7 µs/query | 2.37 ms | 0 MiB | direct |
| b12_d4_Qp/16 | enum_conv | 2.01 ms | 0.1 µs/query | 2.03 ms | 0 MiB | direct |
| b12_d4_Qp/16 | enum_c | 56.3 µs | 138.3 µs/query | 28.81 ms | 0 MiB | direct |
| b12_d4_Qp/16 | bgs_harvey | 12.7 µs | 830.9 µs/query | 168.84 ms | 2 MiB | direct |
| b12_d4_Qp/4 | cmcs_frozen | 245.8 µs | 96.3 µs/query | 77.35 ms | 0 MiB | direct |
| b12_d4_Qp/4 | cmcs_frozen[trace supplied] | 249.2 µs | 83.7 µs/query | 75.50 ms | 0 MiB | direct |
| b12_d4_Qp/4 | flint_power+multipoint | 432.2 µs | 4.2 µs/query | 3.81 ms | 0 MiB | direct |
| b12_d4_Qp/4 | polyrec_c+multipoint | 505.2 µs | 4.8 µs/query | 4.44 ms | 0 MiB | direct |
| b12_d4_Qp/4 | enum_conv | 1.71 ms | 0.1 µs/query | 1.77 ms | 0 MiB | direct |
| b12_d4_Qp/4 | enum_c | 98.3 µs | 152.9 µs/query | 123.85 ms | 0 MiB | direct |
| b12_d4_Qp/4 | bgs_harvey | 17.9 µs | 898.5 µs/query | 649.37 ms | 2 MiB | direct |
| b12_d4_Qp/1 | cmcs_frozen | 233.2 µs | 92.2 µs/query | 352.03 ms | 0 MiB | direct |
| b12_d4_Qp/1 | cmcs_frozen[trace supplied] | 274.6 µs | 94.1 µs/query | 361.72 ms | 0 MiB | direct |
| b12_d4_Qp/1 | flint_power+multipoint | 492.8 µs | 4.5 µs/query | 17.51 ms | 0 MiB | direct |
| b12_d4_Qp/1 | polyrec_c+multipoint | 561.3 µs | 3.3 µs/query | 12.94 ms | 0 MiB | direct |
| b12_d4_Qp/1 | enum_conv | 2.16 ms | 0.1 µs/query | 2.40 ms | 0 MiB | direct |
| b12_d4_Qp/1 | enum_c | 89.7 µs | 176.1 µs/query | 663.91 ms | 0 MiB | direct |
| b12_d4_Qp/1 | bgs_harvey | 15.2 µs | 1.04 ms/query | 3.91 s | 2 MiB | direct |
| b14_d3_Qp/16 | cmcs_frozen | 263.3 µs | 128.0 µs/query | 111.09 ms | 0 MiB | direct |
| b14_d3_Qp/16 | cmcs_frozen[trace supplied] | 281.5 µs | 100.4 µs/query | 88.61 ms | 0 MiB | direct |
| b14_d3_Qp/16 | flint_power+multipoint | 1.58 ms | 6.0 µs/query | 6.68 ms | 0 MiB | direct |
| b14_d3_Qp/16 | polyrec_c+multipoint | 808.5 µs | 10.4 µs/query | 9.98 ms | 0 MiB | direct |
| b14_d3_Qp/16 | enum_conv | 8.37 ms | 0.2 µs/query | 8.51 ms | 0 MiB | direct |
| b14_d3_Qp/16 | enum_c | 106.5 µs | 539.5 µs/query | 455.45 ms | 0 MiB | direct |
| b14_d3_Qp/16 | bgs_harvey | 11.7 µs | 732.6 µs/query | 618.29 ms | 1 MiB | direct |
| b14_d3_Qp/4 | cmcs_frozen | 255.3 µs | 90.7 µs/query | 309.41 ms | 0 MiB | direct |
| b14_d3_Qp/4 | cmcs_frozen[trace supplied] | 239.2 µs | 82.4 µs/query | 339.02 ms | 0 MiB | direct |
| b14_d3_Qp/4 | flint_power+multipoint | 1.81 ms | 3.9 µs/query | 17.52 ms | 0 MiB | direct |
| b14_d3_Qp/4 | polyrec_c+multipoint | 783.7 µs | 4.1 µs/query | 14.47 ms | 0 MiB | direct |
| b14_d3_Qp/4 | enum_conv | 7.98 ms | 0.1 µs/query | 8.39 ms | 0 MiB | direct |
| b14_d3_Qp/4 | enum_c | 109.0 µs | 528.6 µs/query | 1.75 s | 0 MiB | direct |
| b14_d3_Qp/4 | bgs_harvey | 14.6 µs | 719.8 µs/query | 2.38 s | 2 MiB | direct |
| b14_d3_Qp/1 | cmcs_frozen | 224.8 µs | 95.1 µs/query | 1.48 s | 0 MiB | direct |
| b14_d3_Qp/1 | cmcs_frozen[trace supplied] | 295.1 µs | 101.9 µs/query | 1.61 s | 0 MiB | direct |
| b14_d3_Qp/1 | flint_power+multipoint | 2.58 ms | 4.0 µs/query | 65.55 ms | 0 MiB | direct |
| b14_d3_Qp/1 | polyrec_c+multipoint | 1.02 ms | 4.4 µs/query | 70.38 ms | 0 MiB | direct |
| b14_d3_Qp/1 | enum_conv | 9.84 ms | 0.1 µs/query | 11.59 ms | 0 MiB | direct |
| b14_d3_Qp/1 | enum_c | 108.7 µs | 599.2 µs/query | 9.31 s | 0 MiB | direct |
| b14_d3_Qp/1 | bgs_harvey | 15.4 µs | 826.1 µs/query | 12.98 s | 3 MiB | direct |
| b14_d4_Qp/16 | cmcs_frozen | 288.8 µs | 92.4 µs/query | 76.72 ms | 0 MiB | direct |
| b14_d4_Qp/16 | cmcs_frozen[trace supplied] | 346.0 µs | 94.5 µs/query | 55.89 ms | 0 MiB | direct |
| b14_d4_Qp/16 | flint_power+multipoint | 1.41 ms | 10.0 µs/query | 7.39 ms | 0 MiB | direct |
| b14_d4_Qp/16 | polyrec_c+multipoint | 1.26 ms | 11.1 µs/query | 7.98 ms | 0 MiB | direct |
| b14_d4_Qp/16 | enum_conv | 6.14 ms | 0.2 µs/query | 6.25 ms | 0 MiB | direct |
| b14_d4_Qp/16 | enum_c | 103.2 µs | 448.0 µs/query | 263.52 ms | 0 MiB | direct |
| b14_d4_Qp/16 | bgs_harvey | 9.4 µs | 1.29 ms/query | 782.20 ms | 0 MiB | direct |
| b14_d4_Qp/4 | cmcs_frozen | 240.1 µs | 95.1 µs/query | 290.87 ms | 0 MiB | direct |
| b14_d4_Qp/4 | cmcs_frozen[trace supplied] | 291.8 µs | 101.3 µs/query | 299.30 ms | 0 MiB | direct |
| b14_d4_Qp/4 | flint_power+multipoint | 1.88 ms | 5.5 µs/query | 17.36 ms | 0 MiB | direct |
| b14_d4_Qp/4 | polyrec_c+multipoint | 1.61 ms | 5.9 µs/query | 19.82 ms | 0 MiB | direct |
| b14_d4_Qp/4 | enum_conv | 8.35 ms | 0.1 µs/query | 8.75 ms | 0 MiB | direct |
| b14_d4_Qp/4 | enum_c | 105.2 µs | 539.4 µs/query | 1.68 s | 0 MiB | direct |
| b14_d4_Qp/4 | bgs_harvey | 15.0 µs | 1.32 ms/query | 4.25 s | 0 MiB | direct |
| b14_d4_Qp/1 | cmcs_frozen | 271.0 µs | 92.6 µs/query | 863.30 ms | 0 MiB | direct |
| b14_d4_Qp/1 | cmcs_frozen[trace supplied] | 316.1 µs | 96.2 µs/query | 896.86 ms | 0 MiB | direct |
| b14_d4_Qp/1 | flint_power+multipoint | 1.82 ms | 4.8 µs/query | 42.84 ms | 0 MiB | direct |
| b14_d4_Qp/1 | polyrec_c+multipoint | 1.33 ms | 4.5 µs/query | 42.86 ms | 0 MiB | direct |
| b14_d4_Qp/1 | enum_conv | 5.31 ms | 0.1 µs/query | 6.04 ms | 0 MiB | direct |
| b14_d4_Qp/1 | enum_c | 118.8 µs | 409.3 µs/query | 3.82 s | 0 MiB | direct |
| b14_d4_Qp/1 | bgs_harvey | 12.1 µs | 1.26 ms/query | 11.78 s | 1 MiB | direct |
| b16_d3_Qp/16 | cmcs_frozen | 236.8 µs | 106.0 µs/query | 336.93 ms | 0 MiB | consensus |
| b16_d3_Qp/16 | cmcs_frozen[trace supplied] | 310.4 µs | 112.7 µs/query | 355.93 ms | 0 MiB | consensus |
| b16_d3_Qp/16 | flint_power+multipoint | 7.28 ms | 7.8 µs/query | 32.49 ms | 0 MiB | consensus |
| b16_d3_Qp/16 | polyrec_c+multipoint | 2.95 ms | 8.8 µs/query | 31.29 ms | 0 MiB | consensus |
| b16_d3_Qp/16 | enum_conv | 31.29 ms | 0.2 µs/query | 31.87 ms | 0 MiB | consensus |
| b16_d3_Qp/16 | enum_c | 162.0 µs | 1.90 ms/query | 6.12 s | 0 MiB | consensus |
| b16_d3_Qp/16 | bgs_harvey | 12.3 µs | 1.51 ms/query | 4.87 s | 0 MiB | consensus |
| b16_d3_Qp/4 | cmcs_frozen | 213.3 µs | 106.5 µs/query | 1.39 s | 0 MiB | consensus |
| b16_d3_Qp/4 | cmcs_frozen[trace supplied] | 296.0 µs | 105.6 µs/query | 1.42 s | 0 MiB | consensus |
| b16_d3_Qp/4 | flint_power+multipoint | 8.71 ms | 5.5 µs/query | 83.92 ms | 0 MiB | consensus |
| b16_d3_Qp/4 | polyrec_c+multipoint | 2.97 ms | 5.0 µs/query | 75.67 ms | 0 MiB | consensus |
| b16_d3_Qp/4 | enum_conv | 36.61 ms | 0.2 µs/query | 39.65 ms | 0 MiB | consensus |
| b16_d3_Qp/4 | enum_c | 149.1 µs | 1.93 ms/query | 25.74 s | 0 MiB | consensus |
| b16_d3_Qp/4 | bgs_harvey | 12.9 µs | 1.73 ms/query | 23.04 s | 2 MiB | consensus |
| b16_d3_Qp/1 | cmcs_frozen | 224.9 µs | 89.7 µs/query | 3.31 s | 0 MiB | consensus |
| b16_d3_Qp/1 | cmcs_frozen[trace supplied] | 241.8 µs | 93.0 µs/query | 3.32 s | 0 MiB | consensus |
| b16_d3_Qp/1 | flint_power+multipoint | 6.02 ms | 5.0 µs/query | 189.94 ms | 0 MiB | consensus |
| b16_d3_Qp/1 | polyrec_c+multipoint | 2.10 ms | 5.3 µs/query | 197.97 ms | 0 MiB | consensus |
| b16_d3_Qp/1 | enum_conv | 24.24 ms | 0.1 µs/query | 28.76 ms | 0 MiB | consensus |
| b16_d3_Qp/1 | enum_c | — | — | budget (pilot 157 s) | — |  |
| b16_d3_Qp/1 | bgs_harvey | — | — | budget (pilot 134 s) | — |  |
| b16_d4_Qp/16 | cmcs_frozen | 248.1 µs | 104.6 µs/query | 405.36 ms | 0 MiB | consensus |
| b16_d4_Qp/16 | cmcs_frozen[trace supplied] | 261.4 µs | 102.3 µs/query | 384.38 ms | 0 MiB | consensus |
| b16_d4_Qp/16 | flint_power+multipoint | 17.81 ms | 15.0 µs/query | 74.86 ms | 0 MiB | consensus |
| b16_d4_Qp/16 | polyrec_c+multipoint | 6.77 ms | 12.7 µs/query | 56.70 ms | 0 MiB | consensus |
| b16_d4_Qp/16 | enum_conv | 31.13 ms | 0.1 µs/query | 31.66 ms | 0 MiB | consensus |
| b16_d4_Qp/16 | enum_c | 159.4 µs | 2.59 ms/query | 9.84 s | 0 MiB | consensus |
| b16_d4_Qp/16 | bgs_harvey | 14.0 µs | 4.30 ms/query | 16.38 s | 0 MiB | consensus |
| b16_d4_Qp/4 | cmcs_frozen | 231.8 µs | 103.9 µs/query | 1.49 s | 0 MiB | consensus |
| b16_d4_Qp/4 | cmcs_frozen[trace supplied] | 244.5 µs | 118.4 µs/query | 1.63 s | 0 MiB | consensus |
| b16_d4_Qp/4 | flint_power+multipoint | 11.02 ms | 7.0 µs/query | 102.33 ms | 0 MiB | consensus |
| b16_d4_Qp/4 | polyrec_c+multipoint | 6.63 ms | 7.7 µs/query | 106.96 ms | 0 MiB | consensus |
| b16_d4_Qp/4 | enum_conv | 34.52 ms | 0.1 µs/query | 36.29 ms | 0 MiB | consensus |
| b16_d4_Qp/4 | enum_c | 186.3 µs | 2.19 ms/query | 28.66 s | 0 MiB | consensus |
| b16_d4_Qp/4 | bgs_harvey | — | — | budget (pilot 45.5 s) | — |  |
| b16_d4_Qp/1 | cmcs_frozen | 253.3 µs | 117.5 µs/query | 6.30 s | 0 MiB | consensus |
| b16_d4_Qp/1 | cmcs_frozen[trace supplied] | 317.7 µs | 120.4 µs/query | 6.26 s | 0 MiB | consensus |
| b16_d4_Qp/1 | flint_power+multipoint | 13.73 ms | 6.3 µs/query | 371.21 ms | 0 MiB | consensus |
| b16_d4_Qp/1 | polyrec_c+multipoint | 7.17 ms | 6.9 µs/query | 391.29 ms | 0 MiB | consensus |
| b16_d4_Qp/1 | enum_conv | 36.48 ms | 0.1 µs/query | 47.35 ms | 0 MiB | consensus |
| b16_d4_Qp/1 | enum_c | — | — | budget (pilot 138 s) | — |  |
| b16_d4_Qp/1 | bgs_harvey | — | — | timeout | — |  |
| b18_d3_Qp/16 | cmcs_frozen | 261.3 µs | 118.5 µs/query | 1.54 s | 0 MiB | consensus |
| b18_d3_Qp/16 | cmcs_frozen[trace supplied] | 269.1 µs | 125.4 µs/query | 1.68 s | 0 MiB | consensus |
| b18_d3_Qp/16 | flint_power+multipoint | 53.97 ms | 12.5 µs/query | 221.65 ms | 0 MiB | consensus |
| b18_d3_Qp/16 | polyrec_c+multipoint | 10.20 ms | 9.2 µs/query | 133.80 ms | 0 MiB | consensus |
| b18_d3_Qp/16 | enum_conv | 160.22 ms | 0.3 µs/query | 163.97 ms | 0 MiB | consensus |
| b18_d3_Qp/16 | enum_c | — | — | budget (pilot 60.4 s) | — |  |
| b18_d3_Qp/16 | bgs_harvey | 11.7 µs | 2.91 ms/query | 34.29 s | 0 MiB | consensus |
| b18_d3_Qp/4 | cmcs_frozen | 254.1 µs | 117.7 µs/query | 6.11 s | 0 MiB | consensus |
| b18_d3_Qp/4 | cmcs_frozen[trace supplied] | 262.1 µs | 119.5 µs/query | 6.20 s | 0 MiB | consensus |
| b18_d3_Qp/4 | flint_power+multipoint | 51.01 ms | 8.2 µs/query | 516.82 ms | 0 MiB | consensus |
| b18_d3_Qp/4 | polyrec_c+multipoint | 12.61 ms | 7.8 µs/query | 416.80 ms | 0 MiB | consensus |
| b18_d3_Qp/4 | enum_conv | 157.27 ms | 0.2 µs/query | 170.54 ms | 0 MiB | consensus |
| b18_d3_Qp/4 | enum_c | — | — | budget (pilot 153 s) | — |  |
| b18_d3_Qp/4 | bgs_harvey | — | — | budget (pilot 47.9 s) | — |  |
| b18_d3_Qp/1 | cmcs_frozen | 304.8 µs | 119.9 µs/query | 22.19 s | 0 MiB | consensus |
| b18_d3_Qp/1 | cmcs_frozen[trace supplied] | 302.0 µs | 119.3 µs/query | 22.08 s | 0 MiB | consensus |
| b18_d3_Qp/1 | flint_power+multipoint | 45.14 ms | 7.7 µs/query | 1.47 s | 0 MiB | consensus |
| b18_d3_Qp/1 | polyrec_c+multipoint | 10.12 ms | 7.6 µs/query | 1.41 s | 0 MiB | consensus |
| b18_d3_Qp/1 | enum_conv | 124.74 ms | 0.2 µs/query | 167.02 ms | 0 MiB | consensus |
| b18_d3_Qp/1 | enum_c | — | — | timeout | — |  |
| b18_d3_Qp/1 | bgs_harvey | — | — | timeout | — |  |
| b18_d4_Qp/16 | cmcs_frozen | 274.1 µs | 205.3 µs/query | 2.75 s | 0 MiB | consensus |
| b18_d4_Qp/16 | cmcs_frozen[trace supplied] | 378.4 µs | 201.9 µs/query | 2.71 s | 0 MiB | consensus |
| b18_d4_Qp/16 | flint_power+multipoint | 88.01 ms | 29.9 µs/query | 469.69 ms | 0 MiB | consensus |
| b18_d4_Qp/16 | polyrec_c+multipoint | 67.16 ms | 31.0 µs/query | 475.74 ms | 0 MiB | consensus |
| b18_d4_Qp/16 | enum_conv | 292.82 ms | 0.4 µs/query | 297.78 ms | 0 MiB | consensus |
| b18_d4_Qp/16 | enum_c | — | — | budget (pilot 120 s) | — |  |
| b18_d4_Qp/16 | bgs_harvey | — | — | budget (pilot 63.7 s) | — |  |
| b18_d4_Qp/4 | cmcs_frozen | 242.1 µs | 214.9 µs/query | 11.16 s | 0 MiB | consensus |
| b18_d4_Qp/4 | cmcs_frozen[trace supplied] | 263.4 µs | 212.3 µs/query | 11.00 s | 0 MiB | consensus |
| b18_d4_Qp/4 | flint_power+multipoint | 82.46 ms | 16.5 µs/query | 937.69 ms | 0 MiB | consensus |
| b18_d4_Qp/4 | polyrec_c+multipoint | 69.11 ms | 16.5 µs/query | 898.01 ms | 0 MiB | consensus |
| b18_d4_Qp/4 | enum_conv | 261.61 ms | 0.4 µs/query | 287.49 ms | 0 MiB | consensus |
| b18_d4_Qp/4 | enum_c | — | — | timeout | — |  |
| b18_d4_Qp/4 | bgs_harvey | — | — | timeout | — |  |
| b18_d4_Qp/1 | cmcs_frozen | — | — | budget (pilot 48.2 s) | — |  |
| b18_d4_Qp/1 | cmcs_frozen[trace supplied] | — | — | budget (pilot 49.1 s) | — |  |
| b18_d4_Qp/1 | flint_power+multipoint | 59.12 ms | 14.5 µs/query | 2.38 s | 0 MiB | consensus |
| b18_d4_Qp/1 | polyrec_c+multipoint | 49.38 ms | 13.9 µs/query | 2.28 s | 22 MiB | consensus |
| b18_d4_Qp/1 | enum_conv | 240.75 ms | 0.3 µs/query | 303.02 ms | 0 MiB | consensus |
| b18_d4_Qp/1 | enum_c | — | — | timeout | — |  |
| b18_d4_Qp/1 | bgs_harvey | — | — | timeout | — |  |

multipoint = FLINT fmpz_mod_poly_evaluate_fmpz_vec (subproduct tree); enum_conv = one cyclic correlation for all poles.

### W6 branch poles (all rational roots of f), secondary workload

| group | method | preparation | query | total per block | peak RSS above imports | output validation |
|---|---|---|---|---|---|---|
| b13_d3_branch | cmcs_frozen[second-kind prepared] | 6.93 ms | 22.6 µs/query | 6.98 ms | 0 MiB | direct |
| b13_d3_branch | linrec_c | 8.5 µs | 303.0 µs/query | 639.0 µs | 0 MiB | direct |
| b13_d3_branch | polyrec_c | 453.6 µs | 11.6 µs/query | 470.7 µs | 0 MiB | direct |
| b13_d3_branch | enum_c | 60.3 µs | 228.9 µs/query | 541.7 µs | 0 MiB | direct |
| b13_d3_branch | bgs_harvey | 12.5 µs | 1.39 ms/query | 2.46 ms | 2 MiB | direct |
| b13_d4_branch | cmcs_frozen[second-kind prepared] | 9.81 ms | 24.0 µs/query | 9.86 ms | 0 MiB | direct |
| b13_d4_branch | linrec_c | 7.6 µs | 563.5 µs/query | 899.8 µs | 0 MiB | direct |
| b13_d4_branch | polyrec_c | 1.06 ms | 18.0 µs/query | 1.10 ms | 0 MiB | direct |
| b13_d4_branch | enum_c | 56.3 µs | 282.7 µs/query | 505.4 µs | 0 MiB | direct |
| b13_d4_branch | bgs_harvey | 12.2 µs | 1.85 ms/query | 2.89 ms | 2 MiB | direct |
| b16_d3_branch | cmcs_frozen[second-kind prepared] | 78.55 ms | 40.7 µs/query | 78.62 ms | 0 MiB | consensus |
| b16_d3_branch | linrec_c | 7.5 µs | 1.75 ms/query | 1.85 ms | 0 MiB | consensus |
| b16_d3_branch | polyrec_c | 3.47 ms | 44.3 µs/query | 3.52 ms | 0 MiB | consensus |
| b16_d3_branch | enum_c | 154.0 µs | 2.25 ms/query | 2.48 ms | 0 MiB | consensus |
| b16_d3_branch | bgs_harvey | 13.2 µs | 2.43 ms/query | 2.94 ms | 2 MiB | consensus |
| b16_d4_branch | cmcs_frozen[second-kind prepared] | 54.36 ms | 32.7 µs/query | 54.42 ms | 0 MiB | consensus |
| b16_d4_branch | linrec_c | 8.4 µs | 2.98 ms/query | 5.97 ms | 0 MiB | consensus |
| b16_d4_branch | polyrec_c | 4.00 ms | 48.8 µs/query | 4.08 ms | 0 MiB | consensus |
| b16_d4_branch | enum_c | 125.1 µs | 1.36 ms/query | 2.83 ms | 0 MiB | consensus |
| b16_d4_branch | bgs_harvey | 13.1 µs | 2.97 ms/query | 5.83 ms | 2 MiB | consensus |
| b20_d3_branch | cmcs_frozen[second-kind prepared] | 983.25 ms | 39.9 µs/query | 983.29 ms | 0 MiB | consensus |
| b20_d3_branch | linrec_c | 8.9 µs | 24.30 ms/query | 24.31 ms | 0 MiB | consensus |
| b20_d3_branch | polyrec_c | 46.22 ms | 399.2 µs/query | 46.71 ms | 22 MiB | consensus |
| b20_d3_branch | enum_c | 1.32 ms | 31.65 ms/query | 33.00 ms | 0 MiB | consensus |
| b20_d3_branch | bgs_harvey | 12.6 µs | 5.32 ms/query | 5.98 ms | 2 MiB | consensus |
| b20_d4_branch | cmcs_frozen[second-kind prepared] | 1.27 s | 47.7 µs/query | 1.27 s | 0 MiB | consensus |
| b20_d4_branch | linrec_c | 12.7 µs | 61.58 ms/query | 69.14 ms | 0 MiB | consensus |
| b20_d4_branch | polyrec_c | 93.57 ms | 1.10 ms/query | 94.73 ms | 41 MiB | consensus |
| b20_d4_branch | enum_c | 1.31 ms | 35.58 ms/query | 41.22 ms | 0 MiB | consensus |
| b20_d4_branch | bgs_harvey | 12.6 µs | 12.20 ms/query | 12.42 ms | 2 MiB | consensus |

cmcs_frozen charges the trace and its O(p) streaming second-kind recurrence (Python) in preparation; the coefficient methods need no extra data.

### W3 fixed excluded set (s = 8) and 1000 coefficient vectors

| group | method | preparation | query | total per block | peak RSS above imports | output validation |
|---|---|---|---|---|---|---|
| b20_d3_s8_V1000 | cmcs_frozen | 1.64 ms | 0.9 µs/query | 2.55 ms | 0 MiB | consensus |
| b20_d3_s8_V1000 | cmcs_frozen[trace supplied] | 1.73 ms | 1.0 µs/query | 2.63 ms | 0 MiB | consensus |
| b20_d3_s8_V1000 | enum_c | 325.10 ms | 1.0 µs/query | 326.22 ms | 0 MiB | consensus |
| b20_d3_s8_V1000 | linrec_c | 257.59 ms | 0.9 µs/query | 258.45 ms | 0 MiB | consensus |
| b20_d3_s8_V1000 | polyrec_c | 58.02 ms | 0.7 µs/query | 58.77 ms | 31 MiB | consensus |
| b20_d3_s8_V1000 | bgs_harvey | 51.04 ms | 0.9 µs/query | 52.00 ms | 2 MiB | consensus |
| b20_d4_s8_V1000 | cmcs_frozen | 1.46 ms | 0.8 µs/query | 2.34 ms | 0 MiB | consensus |
| b20_d4_s8_V1000 | cmcs_frozen[trace supplied] | 1.99 ms | 0.9 µs/query | 3.34 ms | 0 MiB | consensus |
| b20_d4_s8_V1000 | enum_c | 305.42 ms | 0.9 µs/query | 306.45 ms | 0 MiB | consensus |
| b20_d4_s8_V1000 | linrec_c | 542.75 ms | 1.0 µs/query | 543.76 ms | 0 MiB | consensus |
| b20_d4_s8_V1000 | polyrec_c | 132.49 ms | 1.0 µs/query | 133.52 ms | 63 MiB | consensus |
| b20_d4_s8_V1000 | bgs_harvey | 121.03 ms | 1.0 µs/query | 122.09 ms | 2 MiB | consensus |
| b30_d3_s8_V1000 | cmcs_frozen | 2.12 ms | 0.9 µs/query | 3.03 ms | 0 MiB | consensus |
| b30_d3_s8_V1000 | cmcs_frozen[trace supplied] | 2.03 ms | 0.8 µs/query | 2.83 ms | 0 MiB | consensus |
| b30_d3_s8_V1000 | enum_c | — | — | skipped_ceiling | — |  |
| b30_d3_s8_V1000 | linrec_c | — | — | timeout | — |  |
| b30_d3_s8_V1000 | polyrec_c | — | — | skipped_ceiling | — |  |
| b30_d3_s8_V1000 | bgs_harvey | 1.57 s | 1.1 µs/query | 1.57 s | 7 MiB | consensus |
| b30_d4_s8_V1000 | cmcs_frozen | 2.26 ms | 0.9 µs/query | 3.23 ms | 0 MiB | consensus |
| b30_d4_s8_V1000 | cmcs_frozen[trace supplied] | 2.24 ms | 0.8 µs/query | 3.15 ms | 0 MiB | consensus |
| b30_d4_s8_V1000 | enum_c | — | — | skipped_ceiling | — |  |
| b30_d4_s8_V1000 | linrec_c | — | — | timeout | — |  |
| b30_d4_s8_V1000 | polyrec_c | — | — | skipped_ceiling | — |  |
| b30_d4_s8_V1000 | bgs_harvey | 4.75 s | 0.9 µs/query | 4.75 s | 9 MiB | consensus |

query = per coefficient vector (identical O(s) dot product for every method).

### W2 condensed: median total per workload block (preparation + all Q queries)

| group | cmcs_frozen | cmcs_frozen[trace supplied] | polyrec_c | polyrec_c+multipoint | flint_power | enum_conv | bgs_harvey | enum_c | linrec_c | bgs07 | fastest measured |
|---|---|---|---|---|---|---|---|---|---|---|---|
| b16_d3_Q1 | 347.9 µs | 368.1 µs | 2.57 ms | 6.18 ms | 6.72 ms | 30.59 ms | 3.26 ms | 2.04 ms | 1.57 ms | 13.48 ms | cmcs_frozen |
| b16_d3_Q8 | 971.9 µs | 1.20 ms | 2.46 ms | 8.88 ms | 9.12 ms | 30.78 ms | 15.30 ms | 13.11 ms | 12.01 ms | 105.69 ms | cmcs_frozen |
| b16_d3_Q64 | 7.70 ms | 6.03 ms | 4.36 ms | 14.96 ms | 10.62 ms | 35.75 ms | 94.78 ms | 108.40 ms | 108.62 ms | 889.09 ms | polyrec_c |
| b16_d3_Q512 | 59.10 ms | 56.89 ms | 9.29 ms | 14.42 ms | 13.09 ms | 27.03 ms | 635.09 ms | 828.19 ms | 737.43 ms | 6.42 s | polyrec_c |
| b16_d4_Q1 | 387.4 µs | 463.4 µs | 5.59 ms | 14.08 ms | 9.53 ms | 28.16 ms | 5.92 ms | 2.32 ms | 3.22 ms | 25.13 ms | cmcs_frozen |
| b16_d4_Q8 | 1.71 ms | 1.11 ms | 7.79 ms | 19.42 ms | 16.91 ms | 35.95 ms | 33.70 ms | 19.87 ms | 29.12 ms | 208.67 ms | cmcs_frozen[trace supplied] |
| b16_d4_Q64 | 7.16 ms | 8.15 ms | 9.14 ms | 33.41 ms | 13.11 ms | 30.77 ms | 242.72 ms | 128.44 ms | 233.48 ms | 1.81 s | cmcs_frozen |
| b16_d4_Q512 | 56.24 ms | 46.70 ms | 14.60 ms | 33.43 ms | 15.47 ms | 18.80 ms | 1.42 s | 870.96 ms | 1.70 s | 12.42 s | polyrec_c |
| b20_d3_Q1 | 436.3 µs | 370.4 µs | 57.23 ms | 124.25 ms | 228.81 ms | 700.88 ms | 7.04 ms | 29.91 ms | 27.38 ms | 32.56 ms | cmcs_frozen[trace supplied] |
| b20_d3_Q8 | 1.42 ms | 1.13 ms | 54.06 ms | 126.46 ms | 237.69 ms | 662.82 ms | 49.05 ms | 262.04 ms | 178.44 ms | 232.08 ms | cmcs_frozen[trace supplied] |
| b20_d3_Q64 | 9.17 ms | 8.54 ms | 73.34 ms | 443.99 ms | 301.88 ms | 642.12 ms | 395.38 ms | 2.08 s | 1.54 s | 2.16 s | cmcs_frozen[trace supplied] |
| b20_d3_Q512 | 59.40 ms | 74.92 ms | 193.49 ms | 461.20 ms | 399.38 ms | 742.64 ms | 2.99 s | 16.49 s | 12.22 s | 17.32 s | cmcs_frozen |
| b20_d4_Q1 | 412.1 µs | 385.1 µs | 90.41 ms | 254.68 ms | 337.04 ms | 617.18 ms | 13.63 ms | 41.58 ms | 55.99 ms | 67.80 ms | cmcs_frozen[trace supplied] |
| b20_d4_Q8 | 1.50 ms | 1.33 ms | 123.95 ms | 359.50 ms | 357.78 ms | 718.66 ms | 116.79 ms | 270.24 ms | 517.31 ms | 563.98 ms | cmcs_frozen[trace supplied] |
| b20_d4_Q64 | 8.11 ms | 8.19 ms | 151.31 ms | 1.01 s | 341.32 ms | 642.57 ms | 773.00 ms | 2.43 s | 3.63 s | 4.98 s | cmcs_frozen |
| b20_d4_Q512 | 72.47 ms | 62.03 ms | 454.59 ms | 1.10 s | 650.58 ms | 740.47 ms | 7.71 s | 20.48 s | budget (pilot 21.2 s) | budget (pilot 32.4 s) | cmcs_frozen[trace supplied] |
| b23_d3_Q1 | 480.8 µs | 515.4 µs | 494.18 ms | 1.51 s | 3.62 s | skipped ceiling | 16.03 ms | 283.20 ms | 206.38 ms | 95.87 ms | cmcs_frozen |
| b23_d3_Q8 | 1.56 ms | 1.61 ms | 416.71 ms | 1.10 s | 1.98 s | skipped ceiling | 124.21 ms | 1.84 s | 1.11 s | 695.15 ms | cmcs_frozen |
| b23_d3_Q64 | 10.50 ms | 11.03 ms | 516.50 ms | 5.07 s | 3.66 s | skipped ceiling | 791.79 ms | 17.45 s | 12.24 s | 5.52 s | cmcs_frozen |
| b23_d3_Q512 | 84.48 ms | 76.53 ms | 1.21 s | 4.35 s | 3.92 s | skipped ceiling | 6.63 s | budget (pilot 178 s) | budget (pilot 121 s) | budget (pilot 51.4 s) | cmcs_frozen[trace supplied] |
| b23_d4_Q1 | 352.2 µs | 449.5 µs | 779.62 ms | 2.15 s | 3.93 s | skipped ceiling | 31.37 ms | 265.08 ms | 380.13 ms | 171.29 ms | cmcs_frozen |
| b23_d4_Q8 | 1.66 ms | 1.65 ms | 787.85 ms | 2.22 s | 3.48 s | skipped ceiling | 184.96 ms | 1.80 s | 2.97 s | 1.11 s | cmcs_frozen[trace supplied] |
| b23_d4_Q64 | 11.32 ms | 10.54 ms | 1.39 s | 11.03 s | 5.32 s | skipped ceiling | 2.47 s | 21.09 s | budget (pilot 25.2 s) | 11.13 s | cmcs_frozen[trace supplied] |
| b23_d4_Q512 | 83.36 ms | 94.78 ms | 2.74 s | 8.67 s | 5.88 s | skipped ceiling | budget (pilot 20.9 s) | budget (pilot 176 s) | timeout | budget (pilot 94.2 s) | cmcs_frozen |

Totals include each method's legitimate preparation once per curve. Budget outcomes are recorded pilots (no timing blocks run).

### W5 condensed: dense queries, median total per block

| group | cmcs_frozen | cmcs_frozen[trace supplied] | polyrec_c+multipoint | flint_power+multipoint | enum_conv | enum_c | bgs_harvey | fastest measured |
|---|---|---|---|---|---|---|---|---|
| b12_d3_Qp/16 | 14.75 ms | 16.85 ms | 1.31 ms | 1.20 ms | 1.59 ms | 26.47 ms | 83.78 ms | flint_power+multipoint |
| b12_d3_Qp/4 | 53.29 ms | 66.10 ms | 2.59 ms | 2.89 ms | 1.70 ms | 75.36 ms | 199.55 ms | enum_conv |
| b12_d3_Qp/1 | 230.47 ms | 208.87 ms | 7.94 ms | 8.09 ms | 1.73 ms | 271.74 ms | 1.04 s | enum_conv |
| b12_d4_Qp/16 | 18.89 ms | 20.75 ms | 2.37 ms | 2.23 ms | 2.03 ms | 28.81 ms | 168.84 ms | enum_conv |
| b12_d4_Qp/4 | 77.35 ms | 75.50 ms | 4.44 ms | 3.81 ms | 1.77 ms | 123.85 ms | 649.37 ms | enum_conv |
| b12_d4_Qp/1 | 352.03 ms | 361.72 ms | 12.94 ms | 17.51 ms | 2.40 ms | 663.91 ms | 3.91 s | enum_conv |
| b14_d3_Qp/16 | 111.09 ms | 88.61 ms | 9.98 ms | 6.68 ms | 8.51 ms | 455.45 ms | 618.29 ms | flint_power+multipoint |
| b14_d3_Qp/4 | 309.41 ms | 339.02 ms | 14.47 ms | 17.52 ms | 8.39 ms | 1.75 s | 2.38 s | enum_conv |
| b14_d3_Qp/1 | 1.48 s | 1.61 s | 70.38 ms | 65.55 ms | 11.59 ms | 9.31 s | 12.98 s | enum_conv |
| b14_d4_Qp/16 | 76.72 ms | 55.89 ms | 7.98 ms | 7.39 ms | 6.25 ms | 263.52 ms | 782.20 ms | enum_conv |
| b14_d4_Qp/4 | 290.87 ms | 299.30 ms | 19.82 ms | 17.36 ms | 8.75 ms | 1.68 s | 4.25 s | enum_conv |
| b14_d4_Qp/1 | 863.30 ms | 896.86 ms | 42.86 ms | 42.84 ms | 6.04 ms | 3.82 s | 11.78 s | enum_conv |
| b16_d3_Qp/16 | 336.93 ms | 355.93 ms | 31.29 ms | 32.49 ms | 31.87 ms | 6.12 s | 4.87 s | polyrec_c+multipoint |
| b16_d3_Qp/4 | 1.39 s | 1.42 s | 75.67 ms | 83.92 ms | 39.65 ms | 25.74 s | 23.04 s | enum_conv |
| b16_d3_Qp/1 | 3.31 s | 3.32 s | 197.97 ms | 189.94 ms | 28.76 ms | budget (pilot 157 s) | budget (pilot 134 s) | enum_conv |
| b16_d4_Qp/16 | 405.36 ms | 384.38 ms | 56.70 ms | 74.86 ms | 31.66 ms | 9.84 s | 16.38 s | enum_conv |
| b16_d4_Qp/4 | 1.49 s | 1.63 s | 106.96 ms | 102.33 ms | 36.29 ms | 28.66 s | budget (pilot 45.5 s) | enum_conv |
| b16_d4_Qp/1 | 6.30 s | 6.26 s | 391.29 ms | 371.21 ms | 47.35 ms | budget (pilot 138 s) | timeout | enum_conv |
| b18_d3_Qp/16 | 1.54 s | 1.68 s | 133.80 ms | 221.65 ms | 163.97 ms | budget (pilot 60.4 s) | 34.29 s | polyrec_c+multipoint |
| b18_d3_Qp/4 | 6.11 s | 6.20 s | 416.80 ms | 516.82 ms | 170.54 ms | budget (pilot 153 s) | budget (pilot 47.9 s) | enum_conv |
| b18_d3_Qp/1 | 22.19 s | 22.08 s | 1.41 s | 1.47 s | 167.02 ms | timeout | timeout | enum_conv |
| b18_d4_Qp/16 | 2.75 s | 2.71 s | 475.74 ms | 469.69 ms | 297.78 ms | budget (pilot 120 s) | budget (pilot 63.7 s) | enum_conv |
| b18_d4_Qp/4 | 11.16 s | 11.00 s | 898.01 ms | 937.69 ms | 287.49 ms | timeout | timeout | enum_conv |
| b18_d4_Qp/1 | budget (pilot 48.2 s) | budget (pilot 49.1 s) | 2.28 s | 2.38 s | 303.02 ms | timeout | timeout | enum_conv |

Q = floor((p-4)/16), floor((p-4)/4) or all admissible poles of a fresh curve.

### W4 one weighted sum with s poles, b20_d3_s1-256 (median over 3 fresh curves)

| s | bgs_harvey | cmcs_frozen | cmcs_frozen+weighted_sum | enum_c | linrec_c | polyrec_c | polyrec_c+multipoint |
|---|---|---|---|---|---|---|---|
| prep | 11.8 µs | 253.5 µs | 209.7 µs | 1.64 ms | 10.6 µs | 55.07 ms | 61.82 ms |
| 1 | 8.00 ms (scalars 7.99 ms, corr 11.8 µs) | 246.3 µs (scalars 237.0 µs, corr 9.3 µs) | 302.4 µs (scalars 302.4 µs, corr 0.0 µs) | 64.53 ms (scalars 64.50 ms, corr 34.2 µs) | 30.95 ms (scalars 30.93 ms, corr 16.4 µs) | 587.8 µs (scalars 571.0 µs, corr 21.2 µs) | 724.9 µs (scalars 693.8 µs, corr 23.6 µs) |
| 2 | 12.23 ms (scalars 12.19 ms, corr 31.1 µs) | 341.1 µs (scalars 299.6 µs, corr 19.9 µs) | 175.7 µs (scalars 175.7 µs, corr 0.0 µs) | 100.63 ms (scalars 100.56 ms, corr 66.9 µs) | 52.95 ms (scalars 52.91 ms, corr 30.6 µs) | 811.0 µs (scalars 786.2 µs, corr 27.9 µs) | 954.5 µs (scalars 922.9 µs, corr 50.3 µs) |
| 4 | 23.89 ms (scalars 23.86 ms, corr 29.8 µs) | 591.3 µs (scalars 570.4 µs, corr 21.0 µs) | 454.9 µs (scalars 454.9 µs, corr 0.0 µs) | 167.31 ms (scalars 167.25 ms, corr 54.9 µs) | 107.00 ms (scalars 106.95 ms, corr 42.8 µs) | 1.32 ms (scalars 1.29 ms, corr 31.4 µs) | 1.61 ms (scalars 1.57 ms, corr 34.7 µs) |
| 8 | 48.73 ms (scalars 48.68 ms, corr 53.5 µs) | 1.23 ms (scalars 1.18 ms, corr 41.8 µs) | 992.9 µs (scalars 992.9 µs, corr 0.0 µs) | 346.02 ms (scalars 345.94 ms, corr 77.6 µs) | 212.47 ms (scalars 212.40 ms, corr 67.5 µs) | 2.47 ms (scalars 2.42 ms, corr 53.9 µs) | 2.81 ms (scalars 2.76 ms, corr 52.7 µs) |
| 16 | 98.21 ms (scalars 98.08 ms, corr 133.3 µs) | 2.42 ms (scalars 2.28 ms, corr 137.4 µs) | 2.34 ms (scalars 2.34 ms, corr 0.0 µs) | 659.77 ms (scalars 659.59 ms, corr 180.2 µs) | 402.93 ms (scalars 402.78 ms, corr 147.3 µs) | 4.76 ms (scalars 4.65 ms, corr 116.0 µs) | 5.86 ms (scalars 5.72 ms, corr 124.8 µs) |
| 32 | 218.17 ms (scalars 217.75 ms, corr 422.0 µs) | 4.93 ms (scalars 4.58 ms, corr 349.1 µs) | 4.59 ms (scalars 4.59 ms, corr 0.0 µs) | 1.29 s (scalars 1.29 s, corr 410.3 µs) | 866.30 ms (scalars 865.94 ms, corr 353.4 µs) | 9.57 ms (scalars 9.21 ms, corr 373.2 µs) | 11.76 ms (scalars 11.38 ms, corr 366.7 µs) |
| 64 | 424.98 ms (scalars 423.70 ms, corr 1.28 ms) | 10.28 ms (scalars 9.03 ms, corr 1.22 ms) | 9.74 ms (scalars 9.74 ms, corr 0.0 µs) | 2.34 s (scalars 2.34 s, corr 1.25 ms) | 1.72 s (scalars 1.72 s, corr 1.20 ms) | 19.42 ms (scalars 18.21 ms, corr 1.21 ms) | 23.35 ms (scalars 21.94 ms, corr 1.29 ms) |
| 128 | 867.67 ms (scalars 862.56 ms, corr 4.90 ms) | 22.49 ms (scalars 17.81 ms, corr 4.79 ms) | 23.57 ms (scalars 23.57 ms, corr 0.0 µs) | 4.41 s (scalars 4.40 s, corr 4.87 ms) | 3.66 s (scalars 3.65 s, corr 5.18 ms) | 43.76 ms (scalars 38.75 ms, corr 4.95 ms) | 47.88 ms (scalars 42.88 ms, corr 4.99 ms) |
| 256 | 1.77 s (scalars 1.75 s, corr 19.32 ms) | 54.87 ms (scalars 36.04 ms, corr 19.32 ms) | 63.50 ms (scalars 63.50 ms, corr 0.0 µs) | 8.79 s (scalars 8.76 s, corr 16.19 ms) | 6.86 s (scalars 6.85 s, corr 16.96 ms) | 86.63 ms (scalars 69.50 ms, corr 17.13 ms) | 107.68 ms (scalars 87.89 ms, corr 19.79 ms) |

Weighted sum with a constant term and one zero coefficient (an extra exclusion). Each method also acquires sum_x chi(f(x)) mod p by its own route (trace; coefficient index N+1; table sum).

### W4 one weighted sum with s poles, b20_d4_s1-256 (median over 3 fresh curves)

| s | bgs_harvey | cmcs_frozen | cmcs_frozen+weighted_sum | enum_c | linrec_c | polyrec_c | polyrec_c+multipoint |
|---|---|---|---|---|---|---|---|
| prep | 9.9 µs | 196.6 µs | 293.2 µs | 1.63 ms | 9.7 µs | 134.71 ms | 124.90 ms |
| 1 | 16.93 ms (scalars 16.92 ms, corr 11.7 µs) | 217.1 µs (scalars 209.5 µs, corr 7.9 µs) | 275.3 µs (scalars 275.3 µs, corr 0.0 µs) | 75.98 ms (scalars 75.94 ms, corr 33.6 µs) | 64.73 ms (scalars 64.71 ms, corr 24.7 µs) | 1.45 ms (scalars 1.42 ms, corr 26.9 µs) | 1.46 ms (scalars 1.42 ms, corr 35.5 µs) |
| 2 | 31.94 ms (scalars 31.90 ms, corr 30.9 µs) | 291.5 µs (scalars 281.3 µs, corr 11.2 µs) | 216.4 µs (scalars 216.4 µs, corr 0.0 µs) | 110.29 ms (scalars 110.24 ms, corr 50.1 µs) | 126.78 ms (scalars 126.72 ms, corr 41.8 µs) | 1.94 ms (scalars 1.90 ms, corr 34.5 µs) | 1.84 ms (scalars 1.80 ms, corr 36.5 µs) |
| 4 | 61.98 ms (scalars 61.95 ms, corr 37.1 µs) | 484.9 µs (scalars 468.9 µs, corr 16.0 µs) | 527.9 µs (scalars 527.9 µs, corr 0.0 µs) | 182.95 ms (scalars 182.89 ms, corr 58.5 µs) | 245.25 ms (scalars 245.19 ms, corr 56.7 µs) | 2.43 ms (scalars 2.40 ms, corr 33.4 µs) | 2.37 ms (scalars 2.34 ms, corr 35.5 µs) |
| 8 | 122.44 ms (scalars 122.38 ms, corr 55.0 µs) | 1.23 ms (scalars 1.19 ms, corr 37.6 µs) | 1.14 ms (scalars 1.14 ms, corr 0.0 µs) | 345.28 ms (scalars 345.20 ms, corr 80.9 µs) | 521.47 ms (scalars 521.38 ms, corr 76.3 µs) | 4.95 ms (scalars 4.84 ms, corr 56.5 µs) | 4.68 ms (scalars 4.63 ms, corr 61.7 µs) |
| 16 | 228.00 ms (scalars 227.89 ms, corr 147.3 µs) | 2.69 ms (scalars 2.58 ms, corr 109.9 µs) | 2.42 ms (scalars 2.42 ms, corr 0.0 µs) | 732.76 ms (scalars 732.61 ms, corr 158.9 µs) | 1.11 s (scalars 1.11 s, corr 137.6 µs) | 9.80 ms (scalars 9.68 ms, corr 121.3 µs) | 9.19 ms (scalars 9.09 ms, corr 130.3 µs) |
| 32 | 438.93 ms (scalars 438.40 ms, corr 413.2 µs) | 5.14 ms (scalars 4.78 ms, corr 360.9 µs) | 5.05 ms (scalars 5.05 ms, corr 0.0 µs) | 1.36 s (scalars 1.36 s, corr 450.9 µs) | 2.18 s (scalars 2.18 s, corr 468.4 µs) | 19.89 ms (scalars 19.46 ms, corr 351.1 µs) | 18.92 ms (scalars 18.54 ms, corr 387.1 µs) |
| 64 | 872.40 ms (scalars 871.42 ms, corr 1.17 ms) | 10.21 ms (scalars 8.76 ms, corr 1.03 ms) | 10.55 ms (scalars 10.55 ms, corr 0.0 µs) | 2.69 s (scalars 2.69 s, corr 1.35 ms) | 4.41 s (scalars 4.41 s, corr 1.30 ms) | 40.32 ms (scalars 39.00 ms, corr 1.31 ms) | 41.30 ms (scalars 39.93 ms, corr 1.35 ms) |
| 128 | 1.83 s (scalars 1.83 s, corr 4.32 ms) | 18.94 ms (scalars 15.01 ms, corr 4.01 ms) | 24.65 ms (scalars 24.65 ms, corr 0.0 µs) | 5.37 s (scalars 5.37 s, corr 5.19 ms) | 8.88 s (scalars 8.88 s, corr 4.41 ms) | 83.28 ms (scalars 78.30 ms, corr 4.98 ms) | 75.69 ms (scalars 70.74 ms, corr 4.94 ms) |
| 256 | 4.02 s (scalars 4.00 s, corr 18.61 ms) | 46.50 ms (scalars 30.48 ms, corr 16.33 ms) | 60.12 ms (scalars 60.12 ms, corr 0.0 µs) | 10.57 s (scalars 10.55 s, corr 20.10 ms) | 17.29 s (scalars 17.26 s, corr 21.04 ms) | 174.63 ms (scalars 155.54 ms, corr 19.19 ms) | 161.05 ms (scalars 141.72 ms, corr 20.17 ms) |

Weighted sum with a constant term and one zero coefficient (an extra exclusion). Each method also acquires sum_x chi(f(x)) mod p by its own route (trace; coefficient index N+1; table sum).

### W4 one weighted sum with s poles, b62_d3_s1-256 (median over 3 fresh curves)

| s | bgs_harvey | cmcs_frozen | cmcs_frozen+weighted_sum | enum_c | linrec_c | polyrec_c | polyrec_c+multipoint |
|---|---|---|---|---|---|---|---|
| prep | — | 146.69 ms | 128.18 ms | — | — | — | — |
| 1 | skipped_ceiling | 1.28 ms (scalars 1.26 ms, corr 18.0 µs) | 1.08 ms (scalars 1.08 ms, corr 0.0 µs) | skipped_ceiling | skipped_ceiling | skipped_ceiling | skipped_ceiling |
| 2 | skipped_ceiling | 1.94 ms (scalars 1.92 ms, corr 28.8 µs) | 905.1 µs (scalars 905.1 µs, corr 0.0 µs) | skipped_ceiling | skipped_ceiling | skipped_ceiling | skipped_ceiling |
| 4 | skipped_ceiling | 3.63 ms (scalars 3.60 ms, corr 40.1 µs) | 2.49 ms (scalars 2.49 ms, corr 0.0 µs) | skipped_ceiling | skipped_ceiling | skipped_ceiling | skipped_ceiling |
| 8 | skipped_ceiling | 6.85 ms (scalars 6.72 ms, corr 110.8 µs) | 6.38 ms (scalars 6.38 ms, corr 0.0 µs) | skipped_ceiling | skipped_ceiling | skipped_ceiling | skipped_ceiling |
| 16 | skipped_ceiling | 12.70 ms (scalars 12.49 ms, corr 212.1 µs) | 11.52 ms (scalars 11.52 ms, corr 0.0 µs) | skipped_ceiling | skipped_ceiling | skipped_ceiling | skipped_ceiling |
| 32 | skipped_ceiling | 31.51 ms (scalars 30.71 ms, corr 799.5 µs) | 24.30 ms (scalars 24.30 ms, corr 0.0 µs) | skipped_ceiling | skipped_ceiling | skipped_ceiling | skipped_ceiling |
| 64 | skipped_ceiling | 58.42 ms (scalars 55.07 ms, corr 3.35 ms) | 49.67 ms (scalars 49.67 ms, corr 0.0 µs) | skipped_ceiling | skipped_ceiling | skipped_ceiling | skipped_ceiling |
| 128 | skipped_ceiling | 112.48 ms (scalars 102.03 ms, corr 10.45 ms) | 114.53 ms (scalars 114.53 ms, corr 0.0 µs) | skipped_ceiling | skipped_ceiling | skipped_ceiling | skipped_ceiling |
| 256 | skipped_ceiling | 250.65 ms (scalars 210.30 ms, corr 40.35 ms) | 246.58 ms (scalars 246.58 ms, corr 0.0 µs) | skipped_ceiling | skipped_ceiling | skipped_ceiling | skipped_ceiling |

Weighted sum with a constant term and one zero coefficient (an extra exclusion). Each method also acquires sum_x chi(f(x)) mod p by its own route (trace; coefficient index N+1; table sum).

### W4 one weighted sum with s poles, b62_d4_s1-256 (median over 3 fresh curves)

| s | bgs_harvey | cmcs_frozen | cmcs_frozen+weighted_sum | enum_c | linrec_c | polyrec_c | polyrec_c+multipoint |
|---|---|---|---|---|---|---|---|
| prep | — | 162.22 ms | 150.18 ms | — | — | — | — |
| 1 | skipped_ceiling | 1.13 ms (scalars 1.11 ms, corr 16.2 µs) | 1.07 ms (scalars 1.07 ms, corr 0.0 µs) | skipped_ceiling | skipped_ceiling | skipped_ceiling | skipped_ceiling |
| 2 | skipped_ceiling | 1.68 ms (scalars 1.66 ms, corr 19.3 µs) | 815.4 µs (scalars 815.4 µs, corr 0.0 µs) | skipped_ceiling | skipped_ceiling | skipped_ceiling | skipped_ceiling |
| 4 | skipped_ceiling | 3.11 ms (scalars 3.07 ms, corr 36.8 µs) | 2.48 ms (scalars 2.48 ms, corr 0.0 µs) | skipped_ceiling | skipped_ceiling | skipped_ceiling | skipped_ceiling |
| 8 | skipped_ceiling | 6.70 ms (scalars 6.63 ms, corr 72.9 µs) | 6.15 ms (scalars 6.15 ms, corr 0.0 µs) | skipped_ceiling | skipped_ceiling | skipped_ceiling | skipped_ceiling |
| 16 | skipped_ceiling | 12.93 ms (scalars 12.68 ms, corr 240.7 µs) | 12.73 ms (scalars 12.73 ms, corr 0.0 µs) | skipped_ceiling | skipped_ceiling | skipped_ceiling | skipped_ceiling |
| 32 | skipped_ceiling | 27.32 ms (scalars 26.44 ms, corr 755.0 µs) | 27.11 ms (scalars 27.11 ms, corr 0.0 µs) | skipped_ceiling | skipped_ceiling | skipped_ceiling | skipped_ceiling |
| 64 | skipped_ceiling | 55.28 ms (scalars 51.91 ms, corr 2.64 ms) | 57.34 ms (scalars 57.34 ms, corr 0.0 µs) | skipped_ceiling | skipped_ceiling | skipped_ceiling | skipped_ceiling |
| 128 | skipped_ceiling | 116.47 ms (scalars 108.13 ms, corr 9.83 ms) | 116.15 ms (scalars 116.15 ms, corr 0.0 µs) | skipped_ceiling | skipped_ceiling | skipped_ceiling | skipped_ceiling |
| 256 | skipped_ceiling | 240.10 ms (scalars 196.47 ms, corr 43.63 ms) | 235.99 ms (scalars 235.99 ms, corr 0.0 µs) | skipped_ceiling | skipped_ceiling | skipped_ceiling | skipped_ceiling |

Weighted sum with a constant term and one zero coefficient (an extra exclusion). Each method also acquires sum_x chi(f(x)) mod p by its own route (trace; coefficient index N+1; table sum).


Source: timing_samples_validated.csv (sha256 897c306b80bf095b12dcc2af169b02ea89a6474e7ccd2327655cad139f850fa9)
