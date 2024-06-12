# Spellscript Refactor Tool for AzerothCore
Convert spellscript to use registry macros (see official wiki https://www.azerothcore.org/wiki/core-scripts)

This tool find the first SpellScript by searching for `public SpellScriptLoader` in a file and converts it. Use `--skip` to start at a specific line

Disclaimer: this tool is dumb. It does not add enums for magic numbers, and may remove variables; some manual work is required, but is a good first pass

## Features

- [x] convert AuraScript
- [x] convert SpellScript
- [x] convert Spell- and Aurascript Pairs
- [x] Add `bool Validate...` if it does not exist already
- [x] read/write to file
- [x] `--skip` to specify line number to search for SpellScript
- [x] `--debug` to write debug info to a `refactor.log` file
- [ ] magic numbers to Enum

[See sample log./refactor.log](https://github.com/sogladev/spellscript-refactor-tool/blob/main/refactor.log)

## Install
clone directory

published on test.pypi.org

https://test.pypi.org/project/acore-spellscript-refactor/

## Usage

examples run on script
```
python3 -m acore_spellscript_refactor.main ".../azerothcore-wotlk/src/server/scripts/Northrend/Ulduar/Ulduar/boss_xt002.cpp" --skip 950
python3 -m acore_spellscript_refactor.main `realpath boss_xt002.cpp` --skip 950
python3 -m acore_spellscript_refactor.main `realpath boss_xt002.cpp` --skip 950 --debug
```

Run on all scripts in a directory
```
ls *cpp | xargs -n 1 -I {} python3 -m acore_spellscript_refactor.main `realpath {}`
```

Run main
```
python3 -m acore_spellscript_refactor.main input_file output_file
overwrite input_file
python3 -m acore_spellscript_refactor.main input_file input_file
python3 -m acore_spellscript_refactor.main input_file
skip set amount of lines
python3 -m acore_spellscript_refactor.main input_file output_file --skip 1200
```

## Development

Run tests
```
pytest .
```

Development
```
pip install -e .
```
