# IPv4/IPv6 Address Application

DEVASC Project Activity 3 (Option 2). A Python command-line prototype that shows network technicians the computer's current **public IPv4 and IPv6 addresses**, plus **geolocation, ISP, ASN, and country code**.

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
| `display.py` | All screen output | Formatting changes go here |
| `config.py` | URLs, timeout, headers, app name | No hard-coded URLs elsewhere |
| `test_api_client.py` | Offline tests with mocked API responses | Add a test for new API functions |

## How to add a feature

1. Pull the latest `main` and create your branch: `git checkout -b feature/<your-feature>`
2. Put API logic in `api_client.py`, printing in `display.py`, and a small `option_...()` function in `main.py`.
3. Register it in `MENU` in `main.py`, e.g. `"4": ("Look up any IP or domain", option_lookup_ip),`
4. Run `python -m unittest -v` and try the app.
5. Push and open a Pull Request into `main`. At least one teammate reviews before merging.

## Notes and known limits

- Many home and school networks have **no IPv6**. The app shows "Not available on this network" instead of crashing.
- ipapi.co rate-limits free use. If you hit it, the app shows a rate-limit message; wait and retry.
- Errors (no internet, timeout, bad response) are caught and shown as `[ERROR] ...` messages.

## Team

| Member | Role |
| --- | --- |
| Matthew | Scrum Leader, base application, repository setup |
| Asher | Developer — IP Lookup & Analysis, code review/merge |
| Chylle | Recorder / Developer — Formatted Output & Export, documentation |
| Shane | Lead Presenter, QA |

See **[TEAM_GUIDE.md](TEAM_GUIDE.md)** for the full workflow, tasks and timeline.
