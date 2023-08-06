# Classification Library

*A classification library using a [novel audio-inspired technique](https://youtu.be/dQw4w9WgXcQ).*

## Installation

Try:

```
pip install classification_library
```

Except:

```
pip install git+https://github.com/lol-cubes/classification-library
```

## Usage

```python
from classification_library import AudioClassifier
import numpy as np


X_train = np.array([1, 2, 3, 4])
y_train = np.array([1, 4, 9, 16])
X_test = np.array([5, 6])
y_test = np.array([25, 36])


model = AudioClassifier(alpha=10)
model.fit(X_train, y_train)

predictions = model.predict(X_test)
correct_predictions = 0
for y_true, y_pred in zip(y_test, predictions):
    if y_true == y_pred:
        correct_predictions += 1
print(f"Accuracy: {correct_predictions / len(y_test)}")
```