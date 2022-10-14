# AI Team

## Supported Models
- CCA w/ k-nn
- FB-CCA

## Model Training/Testing

Training models is relatively simple using the training script! 

The only default parameters to pass would be:
- data: The path to your data. The data path can be a folder of folders of csvs or a path to the csv itself. Both should be fine.

By default, we use an **FB-CCA** model, which is a statistical model!

There are some handy flags:
- train: Whether to train a model
- verbose: Whether to output metrics information like accuracy and a confusion matrix to the terminal.

Navigate to `mind-speech-interface-ssvep/` and run

```python
python -m eeg_ai_layer.models.train --data=<YOUR_DATA_PATH> 
```

If you'd like to **see metrics**, pass the `--verbose` flag:

```python
python -m eeg_ai_layer.models.train --data=<YOUR_DATA_PATH> --verbose
```

To train a **CCA-KNN** model, use
```python
python -m eeg_ai_layer.models.train --data=<YOUR_DATA_PATH> --train --output-path=./ --output-name="model.model" --verbose
```