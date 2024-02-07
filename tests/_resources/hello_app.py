import sys


app = globals()["app"]

print(f"Hello {app}")
for arg in sys.argv:
    print(f" - {arg}")
