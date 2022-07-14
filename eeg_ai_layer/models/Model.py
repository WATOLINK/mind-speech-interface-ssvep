from eeg_ai_layer.models.CCAKNN import CCAKNNModel


def load_model(args):
    if args.model_type == 'cca_knn':
        return CCAKNNModel(args)
