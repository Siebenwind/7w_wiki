#!/usr/bin/env python3
import uuid
import datetime

def get_iso_now():
    return datetime.datetime.now().astimezone().isoformat()

def generate_uuid():
    return str(uuid.uuid4())

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "time":
        print(get_iso_now())
    else:
        print(generate_uuid())
