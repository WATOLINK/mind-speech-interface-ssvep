from .CCAKNN import CCAKNNModel


def load_model(**kwargs):
    if kwargs['model_type'] == 'cca_knn':
        return CCAKNNModel(**kwargs)
