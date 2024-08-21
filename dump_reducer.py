#!/usr/bin/env python3
import re
from collections import defaultdict
import argparse
import sys
import os

# ANSI color codes
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
ENDC = "\033[0m"

def color_print(color, message):
    print(f"{color}{message}{ENDC}")

def progress_bar(current, total, width=50):
    percent = float(current) / total
    filled = int(width * percent)
    bar = '=' * filled + '-' * (width - filled)
    percent_display = f"{percent:.1%}"
    return f"\r[{bar}] {percent_display}"

def filter_large_tables(input_file, output_file, max_rows):
    table_row_counts = defaultdict(int)
    tables_to_exclude = set()
    total_lines = sum(1 for _ in open(input_file, 'r'))

    color_print(CYAN, "Phase 1: Counting rows in tables")
    with open(input_file, 'r') as file:
        for i, line in enumerate(file, 1):
            if i % 1000 == 0 or i == total_lines:
                sys.stdout.write(progress_bar(i, total_lines))
                sys.stdout.flush()
            match = re.match(r'INSERT INTO `(\w+)`', line)
            if match:
                current_table = match.group(1)
                values_count = line.count('),(') + 1
                table_row_counts[current_table] += values_count
                if table_row_counts[current_table] > max_rows:
                    tables_to_exclude.add(current_table)
    print()  # New line after progress bar

    color_print(CYAN, "Phase 2: Writing filtered dump")
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        current_table = None
        skip_inserts = False
        for i, line in enumerate(infile, 1):
            if i % 1000 == 0 or i == total_lines:
                sys.stdout.write(progress_bar(i, total_lines))
                sys.stdout.flush()
            if line.startswith("CREATE TABLE"):
                current_table = re.search(r'`(\w+)`', line).group(1)
                skip_inserts = current_table in tables_to_exclude
                outfile.write(line)  # Always write CREATE TABLE statements
            elif line.startswith("INSERT INTO"):
                if not skip_inserts:
                    outfile.write(line)
            else:
                outfile.write(line)
    print()  # New line after progress bar

    return tables_to_exclude

def main():
    parser = argparse.ArgumentParser(description='Filter large tables from MySQL dump.')
    parser.add_argument('input_file', help='Path to input MySQL dump file')
    parser.add_argument('output_file', help='Path to output filtered MySQL dump file')
    parser.add_argument('-m', '--max-rows', type=int, default=1000000, help='Maximum number of rows (default 1000000)')

    args = parser.parse_args()

    try:
        color_print(GREEN, f"Starting to process {args.input_file}")
        color_print(YELLOW, f"Max rows per table: {args.max_rows}")

        excluded_tables = filter_large_tables(args.input_file, args.output_file, args.max_rows)

        color_print(GREEN, f"Filtered dump saved to {args.output_file}")
        color_print(YELLOW, "Excluded tables:")
        for table in excluded_tables:
            print(f"- {table}")

        input_size = os.path.getsize(args.input_file)
        output_size = os.path.getsize(args.output_file)
        size_reduction = (1 - output_size / input_size) * 100

        color_print(GREEN, f"Size reduction: {size_reduction:.2f}%")
        color_print(GREEN, "Process completed successfully")

    except IOError as e:
        color_print(RED, f"Error working with files: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
