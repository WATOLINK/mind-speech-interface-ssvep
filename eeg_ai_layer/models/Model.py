from eeg_ai_layer.models.CCAKNN import CCAKNNModel
from eeg_ai_layer.models.FBCCA import FBCCA
from eeg_ai_layer.models.KNN import KNN


def load_model(args):
    """
    Loads the model specified in the args
    """
    if args.model_type == 'cca_knn':
        return CCAKNNModel(args)
    if args.model_type == 'fbcca':
        return FBCCA(args)
    if args.model_type == 'fbcca_knn':
        return KNN(args)
