# IPv4/IPv6 Address Application

DEVASC Project Activity 3 (Option 2). A Python command-line prototype that shows network technicians the computer's current **public IPv4 and IPv6 addresses**, plus **geolocation, ISP, ASN, and country code**. It can also analyze any IP address and export results to JSON and CSV.

## Features

| Menu | Feature | What it does |
| --- | --- | --- |
| 1 | Public IPv4 | Shows this computer's public IPv4 address |
| 2 | Public IPv6 | Shows the public IPv6 address, or "Not available on this network" |
| 3 | Full details | Both IPs plus location, ISP, ASN, country code and timezone in a table |
| 4 | Look up any IP | Validates any IPv4/IPv6 address and shows its version, type (Public, Private, Loopback, Link-local, Multicast, Reserved) and IPv4 class (A to E). Public addresses also get the details table; other types skip the API call. |
| 5 | Export | Saves IPv4, IPv6 and details to `exports/ip_report_<YYYYMMDD_HHMMSS>.json` and `.csv` |
| q | Quit | Exits cleanly (Ctrl+C works too) |

Output is color-formatted with the [rich](https://github.com/Textualize/rich) library: green for addresses, yellow for notes and "not available", red for errors.

## APIs used

| API | Purpose | Key needed? |
| --- | --- | --- |
| `api.ipify.org` | Public IPv4 address | No |
| `api6.ipify.org` | Public IPv6 address (IPv6-only endpoint) | No |
| `ipapi.co/{ip}/json/` | Location, ISP (`org`), ASN, country code, timezone | No (≈1,000 req/day) |

## Setup and run

```bash
pip install -r requirements.txt
python main.py
```

Run the offline unit tests:

```bash
python -m unittest -v
```

## Project structure

| File | What it does | Rule |
| --- | --- | --- |
| `main.py` | Menu loop and feature functions | Add your feature as **one line** in `MENU` |
| `api_client.py` | All REST API calls; returns data, never prints | Raise `IPLookupError` on failure |
| `ip_analysis.py` | `analyze_ip()`: validates an address and returns its version, type and class | Pure logic: no printing, no API calls |
| `exporter.py` | `export_json()` / `export_csv()`: save a report and return the file path | Never prints; `display.py` shows the paths |
| `display.py` | All screen output (rich panels, tables, colors) | Formatting changes go here; no `print()` elsewhere |
| `config.py` | URLs, timeout, headers, app name | No hard-coded URLs elsewhere |
| `test_*.py` | Offline unit tests (API calls mocked, exports to a temp folder) | Add tests for new logic |

## How to add a feature

1. Pull the latest `main` and create your branch: `git checkout -b feature/<your-feature>`
2. Put API logic in `api_client.py`, printing in `display.py`, and a small `option_...()` function in `main.py`.
3. Register it in `MENU` in `main.py` with the next free number, e.g. `"6": ("Reverse DNS lookup", option_reverse_dns),`
4. Run `python -m unittest -v` and try the app.
5. Push and open a Pull Request into `main`. At least one teammate reviews before merging.

## Notes and known limits

- Many home and school networks have **no IPv6**. The app shows "Not available on this network" instead of crashing.
- ipapi.co rate-limits free use. If you hit it, the app shows a rate-limit message; wait and retry.
- Errors (no internet, timeout, bad response) are caught and shown as `[ERROR] ...` messages.
- Option 4 labels shared ISP space such as `100.64.0.1` (carrier-grade NAT) as Reserved. Python counts the IPv6 documentation range `2001:db8::/32` as private, so it shows as Private.
- `exports/` is in `.gitignore`, so exported reports stay on your machine.
- If colors look broken on Windows, use Windows Terminal or the VS Code terminal instead of the old `cmd` window.

## Future enhancements (backlog)

1. GUI or web dashboard (Tkinter or Flask)
2. Map view using latitude and longitude
3. Lookup history saved locally
4. Bulk lookup from a text file of IP addresses
5. Backup API when ipapi.co is rate-limited (e.g. ip-api.com)
6. Reverse DNS and WHOIS lookup
7. Subnet calculator (CIDR, subnet mask, host range)
8. Command-line arguments for scripting (e.g. `python main.py --ipv4`)

## Team

| Member | Role |
| --- | --- |
| Matthew | Scrum Leader, base application, repository setup |
| Asher | Developer — IP Lookup & Analysis, code review/merge |
| Chylle | Recorder / Developer — Formatted Output & Export, documentation |
| Shane | Lead Presenter, QA |

See **[TEAM_GUIDE.md](TEAM_GUIDE.md)** for the full workflow, tasks and timeline.
