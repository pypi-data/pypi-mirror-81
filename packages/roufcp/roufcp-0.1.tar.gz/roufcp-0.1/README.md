# roufcp - Rough Fuzzy Changepoint Detection

Gradual Change-Point Detection Library based on Rough Fuzzy Changepoint Detection algorithm `roufcp`.

## Usage

```
>> import numpy as np
>> from roufcp import roufCP
>> X = np.concatenate([np.ones(20) * 5, np.zeros(20), np.ones(20) * 10]) + np.random.randn(60)
>> roufCP(delta = 3, w = 3).fit(X, moving_window = 10, k = 2)

```


## Authors & Contributors

* Subhrajyoty Roy - https://subroy13.github.io/
* Ritwik Bhaduri - https://github.com/Ritwik-Bhaduri
* Sankar Kumar Pal - https://www.isical.ac.in/~sankar/


## License

This code is licensed under MIT License.
