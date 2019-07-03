# Quickstart

```python
from falconx_py import FalconxClient

fnx = FalconxClient(key=KEY, secret=SECRET, passphrase=PASSPHRASE)

quote = fnx.get_quote('BTC', 'USD', 5, 'two-way')

result = fnx.execute_quote(quote['fx_quote_id'], 'buy')
```

# Installation
Clone the git and add directory to PYTHONPATH

Install requirements:
```sh
pip install -r requirements.txt
```

# About FalconX
FalconX is an institutional digital asset brokerage. 