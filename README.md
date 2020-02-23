# Simple Instagram Bot

This Instagram bot automates simple tasks an Instagram user might do. It can also try to get more followers. For example, crawling through a number of posts under a certain hashtag, following, liking, and commenting each post.

## Installation
Use the package manager [pip3](https://pip.pypa.io/en/stable/) to install selenium and pandas using `requirements.txt`,
```bash
pip3 install -r requirements.txt
```

or use the package manager [pip3](https://pip.pypa.io/en/stable/) to install selenium and pandas individually.

```bash
pip3 install selenium
pip3 install pandas
```

## Usage
Run `config_setup.py` if this is the first time to put in the username and password for Instagram, (you can also update the existing config with this script)
```python
python3 config_setup.py
```
After the config is set, the bot can now login and do its things!
```python
python3 bot.py
```
or
```python
from bot import InstagramBot
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.
