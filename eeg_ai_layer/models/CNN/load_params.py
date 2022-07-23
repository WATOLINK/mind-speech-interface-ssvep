
def get_params():
    CNN_PARAMS = {
        'batch_size': 64,
        'epochs': 250,
        'droprate': 0.25,
        'learning_rate': 0.001,
        'lr_decay': 0.0,
        'l2_lambda': 0.0001,
        'momentum': 0.9,
        'kernel_f': 10,
        'n_ch': 8, 
        'num_classes': 5
    }

    return CNN_PARAMS