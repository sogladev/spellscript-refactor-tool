# Spellscript Refactor Tool
Convert spellscript to new format

This tool find the first SpellScript by searching for `public SpellScriptLoader` in a file and converts it. Use `--skip` to start at a specific line

Disclaimer: this tool is dumb. It does not add enums for magic numbers, and may remove variables; some manual work is required, but is a good first pass

[See sample log./refactor.log](./refactor.log)

Run tests
```
pytest .
```

Development
```
pip install -e .
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

run on script
```
python3 -m acore_spellscript_refactor.main `realpath boss_xt002.cpp` --skip 950
```

Run on all `*cpp` in a folder
```
ls *cpp | xargs -n 1 -I {} python3 -m acore_spellscript_refactor.main `realpath {}`
```
