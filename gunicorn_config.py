import multiprocessing

# Number of worker processes - typically (2 * CPU cores) + 1
workers = multiprocessing.cpu_count() * 2 + 1

# Number of threads per worker
threads = 2

# Binding
bind = "0.0.0.0:5000"

# Timeout
timeout = 120
