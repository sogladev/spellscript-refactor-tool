# Spellscript Refactor Tool
Convert spellscript to new format

This tool find the first SpellScript by searching for `public SpellScriptLoader` in a file and converts it. Use `--skip` to start at a specific line

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
python3 -m spellscript_refactor.main input_file output_file
overwrite input_file
python3 -m spellscript_refactor.main input_file input_file
python3 -m spellscript_refactor.main input_file
skip set amount of lines
python3 -m spellscript_refactor.main input_file output_file --skip 1200
```
