# Spellscript Refactor Tool for AzerothCore
Python tool to convert spellscript(s) to use registry macros (see official wiki https://www.azerothcore.org/wiki/core-scripts)

The `acore_spellscript_refactor` tool provides modules to refactor spellscripts to use registry macros (see official wiki https://www.azerothcore.org/wiki/core-scripts).

Disclaimer: This tool is dumb. It finds the first SpellScript by searching for `public SpellScriptLoader` in a file and converts it. It does not add enums for magic numbers, and may remove variables; some manual work is required, but it is a good first pass

## Features

- [x] convert AuraScript
- [x] convert SpellScript
- [x] convert Spell- and Aurascript Pairs
- [x] add `bool Validate...` if it does not exist already
- [x] read/write to file
- [x] create skeleton update statement `spell_script_names` to `script_name.sql` if type is `_aura`
- [x] fill in spell_ids skeleton update with spell_ids from table `acore_world` `spell_script_names`
- [x] `--skip` to specify line number to search for SpellScript
- [x] `--verbose/-v` to output debug info
- [x] `--sql-file` to write script_name updates to specific file
- [x] `discover` runs repeatedly on all `*cpp` in directory
- [x] spell scripts with args
- [ ] magic numbers to Enum

[See sample log./refactor.log](https://github.com/sogladev/spellscript-refactor-tool/blob/main/refactor.log)

## Install

The `acore-spellscript-refactor` package is published on [Test PyPI](https://test.pypi.org/project/acore-spellscript-refactor/) for testing and development purposes. Follow the steps below to install it.

### Installation Steps

1. **Clone the Repository (Optional)**  
   If you want to work with the source code, clone the repository to your local machine:
   ```bash
   git clone https://github.com/your-username/acore-spellscript-refactor.git
   cd acore-spellscript-refactor
   pip install -e .
   ```

2. **Install from Test PyPI**  
   To install the latest version of `acore-spellscript-refactor` from Test PyPI, use the following command:
   ```bash
   pip install acore-spellscript-refactor
   ```

   This installs the package and all required dependencies from the Test PyPI repository.

3. **Verify the Installation**  
   Confirm the installation by running:
   ```bash
   python3 -m acore_spellscript_refactor.main --help
   ```

For more information, visit the [acore-spellscript-refactor page on Test PyPI](https://test.pypi.org/project/acore-spellscript-refactor/).



## Usage
This covers basic usage, command options, and examples for the `main` and `discover` modules.

To create a `rev_*.sql` file, use `create_sql.sh`
```bash
./data/sql/updates/pending_db_world/create_sql.sh
``` 
In the sections below `$REV_SQL` refers to absolute path of this created `rev_*.sql`.
```bash
REV_SQL="/azerothcore-wotlk/data/sql/updates/pending_db_world/rev_1730477106741869456.sql"
```

note: for file arguments, use **absolute paths**

### Examples

#### Using `main`

The `main` module refactors a single script file at a time or all scripts within a directory.

##### Refactoring a Single Script with Line Offset
To refactor a single script file and specify an offset (e.g., skip the first 950 lines):

```bash
python3 -m acore_spellscript_refactor.main "/azerothcore-wotlk/src/server/scripts/Northrend/Ulduar/Ulduar/boss_xt002.cpp" --skip 950
python3 -m acore_spellscript_refactor.main `realpath boss_xt002.cpp` --skip 950
python3 -m acore_spellscript_refactor.main `realpath boss_xt002.cpp` --skip 950 --verbose
```

##### Refactoring All Scripts in a Directory
To refactor all `.cpp` files in a directory, use `xargs` to iterate through each file:

```bash
ls *cpp | xargs -n 1 -I {} python3 -m acore_spellscript_refactor.main `realpath {}`
```

##### Command Options

1. **Specify input and output files**:
   - Provide an `input_file` and `output_file` to save results to a specific file.
   ```bash
   python3 -m acore_spellscript_refactor.main input_file output_file
   ```

2. **Overwrite input file**:
   - Use the same file for both `input_file` and `output_file` to overwrite.
   ```bash
   python3 -m acore_spellscript_refactor.main input_file input_file
   ```

3. **Default single file refactor**:
   - Refactor a single file without specifying an output, defaults to overwriting the `input_file`.
   ```bash
   python3 -m acore_spellscript_refactor.main input_file
   ```

4. **Skip a specified number of lines**:
   - Use `--skip` to ignore a set number of lines.
   ```bash
   python3 -m acore_spellscript_refactor.main input_file output_file --skip 1200
   ```

5. **Use with SQL file generation**:
   - Refactor with associated SQL queries stored in a specified file.
   ```bash
   python3 -m acore_spellscript_refactor.main input_file output_file --skip 1200 --sql_file $REV_SQL
   ```

6. **Commit changes**:
   - Add the `--commit` flag to save changes with an optional SQL file for database updates.
   ```bash
   python3 -m acore_spellscript_refactor.main input_file --commit --sql_file $REV_SQL
   ```

#### Using `discover`

The `discover` module finds `.cpp` files and creates commits and SQL files as necessary.

##### Example Usage

1. **Commit all discovered files**:
   - Specify a `.sql` file for database changes, or allow `discover` to auto-create one by omitting `--sql_file`
   ```bash
   python3 -m acore_spellscript_refactor.discover --commit --sql_file $REV_SQL
   ```

2. **Run on all scripts in a directory**:
   - Set the working directory to `azerothcore-wotlk/src/server/scripts/***/scripts_folder` and recursively discover `.cpp` files.
   ```bash
   python3 -m acore_spellscript_refactor.discover --commit --recursive --sql_file $REV_SQL
   ```

3. **Run on all scripts**:
   - Set the working directory to `azerothcore-wotlk/src/server/scripts` and recursively discover `.cpp` files.
   ```bash
   python3 -m acore_spellscript_refactor.discover --commit --recursive --sql_file $REV_SQL
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
