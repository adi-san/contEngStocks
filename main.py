# plot_time_series.py

import matplotlib.pyplot as plt
from datetime import datetime, timedelta
plt.style.use('seaborn')

dates = [
    datetime(2019, 8, 21),
    datetime(2019, 8, 22),
    datetime(2019, 8, 23),
    datetime(2019, 8, 24),
    datetime(2019, 8, 25),
    datetime(2019, 8, 26),
    datetime(2019, 8, 27),
]

y = [0, 1, 2, 3, 4, 5, 6]

plt.plot_date(dates, y)
plt.tight_layout()
plt.show()