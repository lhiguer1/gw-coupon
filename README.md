# Goodwill Coupon Downloader
Enrolls into the Goodwill newsletter using a temporary email address so that I don't have to go through the process manually.

## Installation & Usage
I recomend using a python virtual environment
```bash
python3 -m pip venv .venv
source .venv/bin/activate
python3 -m pip install -e .
python3 -m gw_coupon_downloader 
# files will be saved to ./coupons
```

### Credits
- [secmail](https://github.com/SirLez/secmail)
