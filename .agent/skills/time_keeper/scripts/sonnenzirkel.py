#!/usr/bin/env python3
import argparse
import sys

# Siebenwind Calendar Data
MONTHS = [
    "Sekar", "Oner", "Onar",  # Morsan (Winter)
    "Duler", "Dular", "Trier",  # Vitama (Spring)
    "Triar", "Querler", "Querlar",  # Astrael (Summer)
    "Carmer", "Carmar", "Seker"   # Bellum (Autumn)
]

SEASONS = {
    "Sekar": "Morsan", "Oner": "Morsan", "Onar": "Morsan",
    "Duler": "Vitama", "Dular": "Vitama", "Trier": "Vitama",
    "Triar": "Astrael", "Querler": "Astrael", "Querlar": "Astrael",
    "Carmer": "Bellum", "Carmar": "Bellum", "Seker": "Bellum"
}

# Approximate mapping: Index 0 (Sekar) corresponds to December
EARTH_MAP = {
    12: "Sekar", 1: "Oner", 2: "Onar",
    3: "Duler", 4: "Dular", 5: "Trier",
    6: "Triar", 7: "Querler", 8: "Querlar",
    9: "Carmer", 10: "Carmar", 11: "Seker"
}

def get_season(month_name):
    """Returns the season for a given month."""
    month_name = month_name.capitalize()
    return SEASONS.get(month_name, "Unknown Month")

def earth_to_7w(earth_month_index):
    """Converts Earth month (1-12) to Siebenwind month."""
    if 1 <= earth_month_index <= 12:
        return EARTH_MAP[earth_month_index]
    return "Invalid Earth Month"

def validate_date(day, month_name):
    """Validates if a date exists in the standard calendar (1-28 days)."""
    month_name = month_name.capitalize()
    if month_name not in MONTHS:
        return False, f"Invalid Month: {month_name}"
    
    try:
        day = int(day)
    except ValueError:
        return False, "Day must be a number"

    if 1 <= day <= 28:
        return True, "Valid Date"
    else:
        return False, "Day out of range (Standard months have 28 days)"

def main():
    parser = argparse.ArgumentParser(description="Siebenwind Time Keeper Utility")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Command: season <Month>
    parser_season = subparsers.add_parser("season", help="Get season for a month")
    parser_season.add_argument("month", type=str, help="Name of the month (e.g., Sekar)")

    # Command: convert <EarthMonthIndex>
    parser_convert = subparsers.add_parser("convert", help="Convert Earth month index to Siebenwind")
    parser_convert.add_argument("earth_month", type=int, help="Earth month index (1-12)")
    
    # Command: validate <Day> <Month>
    parser_validate = subparsers.add_parser("validate", help="Validate a Siebenwind date")
    parser_validate.add_argument("day", type=int, help="Day of the month")
    parser_validate.add_argument("month", type=str, help="Name of the month")

    # Command: list
    parser_list = subparsers.add_parser("list", help="List all months and seasons")

    args = parser.parse_args()

    if args.command == "season":
        print(get_season(args.month))
    elif args.command == "convert":
        print(earth_to_7w(args.earth_month))
    elif args.command == "validate":
        valid, msg = validate_date(args.day, args.month)
        print(f"{'VALID' if valid else 'INVALID'}: {msg}")
    elif args.command == "list":
        print(f"{'Month':<10} | {'Season':<10}")
        print("-" * 22)
        for m in MONTHS:
            print(f"{m:<10} | {SEASONS[m]:<10}")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
