TESTING = True

# HOR = 1080
# VERT = 1360
HOR = 2400
VERT = 1360

# Configurable settings
NUM_STIMS = 8 # same length as below arrs

# ---- 8 stims ---- #
FREQS = [10.25, 11.75, 12.75, 14.75, 11.25, 9.25, 10.75, 13.25]
RADII = [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]

# ---- 6 stims ---- #
# FREQS = [10.25, 11.75, 12.75, 14.75, 11.25, 9.25]
# RADII = [0.5, 0.5, 0.5, 0.5, 0.5, 0.5]

# ---- 4 stims ---- #
#FREQS = [10.25, 11.75, 12.75, 14.75]
#RADII = [0.5, 0.5, 0.5, 0.5]

def demo_configs():
    if TESTING:
        START_DELAY_S = 5
        NUM_TRIALS = 1
        INDICATOR_TIME_VALUE_S = 1
        TRIAL_BREAK_TIME = 1
        STIM_TIME = 1
    else:
        START_DELAY_S = 20  # 20 Seconds
        NUM_TRIALS = 5  # 5 Trials
        INDICATOR_TIME_VALUE_S = 5  # 5 Seconds
        TRIAL_BREAK_TIME = 120  # 120 second
        STIM_TIME = 5  # stim flash time

    return START_DELAY_S, NUM_TRIALS, INDICATOR_TIME_VALUE_S, TRIAL_BREAK_TIME, STIM_TIME