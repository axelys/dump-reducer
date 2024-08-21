# Dump Reducer

Dump Reducer is a Python script designed to filter large tables from MySQL dump files. It creates a new dump file excluding INSERT statements for tables that exceed a specified number of rows, while preserving the structure (CREATE TABLE statements) of all tables.

## Features

- Filters MySQL dump files based on the number of rows in each table
- Preserves table structures for all tables, including excluded ones
- Provides a colorful, informative console output with a simple progress bar
- Shows the size reduction achieved after filtering
- No external dependencies required

## Installation

1. Ensure you have Python 3.6 or later installed on your system.

2. Clone this repository or download the `dump_reducer.py` script.

That's it! No additional libraries are required.

## Usage

Basic usage:

```
python dump_reducer.py input_dump.sql output_dump.sql
```

This will process `input_dump.sql`, exclude tables with more than 1,000,000 rows, and save the result to `output_dump.sql`.

### Options

- `-m` or `--max-rows`: Specify the maximum number of rows allowed per table (default is 1,000,000)

Example with custom max rows:

```
python dump_reducer.py input_dump.sql output_dump.sql -m 500000
```

This will exclude tables with more than 500,000 rows.

## Examples

1. Basic filtering:

   ```
   python dump_reducer.py huge_database_dump.sql filtered_dump.sql
   ```

   This will process `huge_database_dump.sql`, exclude tables with more than 1,000,000 rows, and save the result to `filtered_dump.sql`.

2. Filtering with custom row limit:

   ```
   python dump_reducer.py monthly_dump.sql reduced_monthly_dump.sql -m 100000
   ```

   This will process `monthly_dump.sql`, exclude tables with more than 100,000 rows, and save the result to `reduced_monthly_dump.sql`.

3. Using in a bash script:

   ```bash
   #!/bin/bash

   INPUT_DUMP="/path/to/large_dump.sql"
   OUTPUT_DUMP="/path/to/filtered_dump.sql"
   MAX_ROWS=750000

   python dump_reducer.py "$INPUT_DUMP" "$OUTPUT_DUMP" -m "$MAX_ROWS"

   if [ $? -eq 0 ]; then
       echo "Dump reduction completed successfully"
   else
       echo "Error occurred during dump reduction" >&2
       exit 1
   fi
   ```

   This bash script runs Dump Reducer with specified input and output files, and a custom row limit.

## Output

Dump Reducer provides informative, colored console output including:

- A simple progress bar for each phase of the process
- List of excluded tables
- Size reduction achieved

Example output:

```
Starting to process huge_database_dump.sql
Max rows per table: 1000000
Phase 1: Counting rows in tables
[==================================================] 100.0%
Phase 2: Writing filtered dump
[==================================================] 100.0%
Filtered dump saved to filtered_dump.sql
Excluded tables:
- large_table1
- large_table2
- enormous_table
Size reduction: 65.23%
Process completed successfully
```

## Notes

- The script requires a terminal that supports ANSI color codes for the best experience.
- While the script preserves CREATE TABLE statements for all tables, it excludes INSERT statements for tables exceeding the specified row limit.
- The script does not modify the original dump file; it creates a new file with the filtered content.
- No external libraries are required, making it easy to run on any system with Python installed.
