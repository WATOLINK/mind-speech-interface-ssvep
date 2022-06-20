from CCAKNN import CCAKNNModel


class Model():
    """
    Model chooser that chooses a model.
    """
    def __init__(self, model_path, model_type: str = 'cca_knn', **kwargs):
        self.model = self.load_model_arch(model_path, model_type, **kwargs)

    def load_model_arch(self, model_path: str, model_type: str = 'cca_knn', **kwargs):
        if model_type == 'cca_knn':
            return CCAKNNModel(model_path, **kwargs)

    def predict(self, data):
        return self.model.predict(data)
