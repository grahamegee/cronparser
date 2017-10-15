# cronparser
Simple script for parsing a single crontab line.

## Install

```bash
git checkout https://github.com/grahamegee/cronparser.git
```

If you just want to use the parser:

```bash
pip install -e cronparser
```

If you need to run tests:

```bash
pip install -e cronparser['test']
```

## Usage

```bash
python -m cronparser.parse <"crontab line">
```

Remember to incluse the crontab line in single or double quotes.