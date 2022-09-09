# HOR = 1080
# VERT = 1360
HOR = 1280
VERT = 720
TESTING = True

def demo_configs():
    if TESTING:
        START_DELAY_S = 5
        NUM_TRIALS = 1
        INDICATOR_TIME_VALUE_S = 1
        TRIAL_BREAK_TIME = 1
        STIM_PERIOD_TRIALS = 4
        STIM_TIME = 1
    else:
        START_DELAY_S = 20  # 20 Seconds
        NUM_TRIALS = 5  # 5 Trials
        INDICATOR_TIME_VALUE_S = 5  # 5 Seconds
        TRIAL_BREAK_TIME = 120  # 120 second
        STIM_PERIOD_TRIALS = 4  # number of stim it goes through
        STIM_TIME = 5  # stim flash time

    return START_DELAY_S, NUM_TRIALS, INDICATOR_TIME_VALUE_S, TRIAL_BREAK_TIME, STIM_PERIOD_TRIALS, STIM_TIME