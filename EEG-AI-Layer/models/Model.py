from CCAKNN import CCAKNNModel


def load_model(**kwargs):
    if kwargs.get('model_type', None) == 'cca_knn':
        return CCAKNNModel(**kwargs)
