# Spellscript Refactor Tool
Convert spellscript to new format

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
skip set amount of lines
python3 -m spellscript_refactor.main input_file output_file 1200
```

[See sample log./refactor.log](./refactor.log)