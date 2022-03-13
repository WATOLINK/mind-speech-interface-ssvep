from .CCAKNN import CCAKNNModel

class Model():
    """
    Model chooser that chooses a model.
    """
    def __init__(self, kwargs = None):
        self.model = self.load_model_arch(kwargs)

    def load_model_arch(self, kwargs = None):
        if kwargs.model_type == 'cca_knn':
            return CCAKNNModel(kwargs)

    def predict(self, data):
        return self.model.predict(data)