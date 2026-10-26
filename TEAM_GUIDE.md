# Team Guide — DEVASC Project Activity 3 (Option 2)

**IPv4/IPv6 Address Application**

| Deadline | What |
| --- | --- |
| **Mon, Oct 26, 2026 — 11:59 PM** | Final code merged on GitHub + completed rubric submitted |
| **Tue, Oct 27, 2026** | Presentation (10–15 minutes), all four members speak |

---

## 1. Team and responsibilities

| Member | Role | Owns |
| --- | --- | --- |
| **Matthew** | Scrum Leader | Base application, GitHub repository setup |
| **Asher** | Developer | Feature A (IP Lookup & Analysis), code reviews and merging, GitHub rubric section, live demo setup |
| **Chylle** | Recorder / Developer | Feature B (Formatted Output & Export), rubric document, backlog, team reflection, presentation deck |
| **Shane** | Lead Presenter | Main speaker, presentation script, rehearsal, final QA run on his own laptop |

---

## 2. What is already done

The base application is complete and on the `main` branch:

- Menu-driven Python app (`python main.py`)
- Public **IPv4** lookup (ipify), public **IPv6** lookup (api6.ipify)
- Full details: **location, ISP, ASN, country code, timezone** (ipapi.co)
- Error handling: no internet, timeouts, rate limits, networks without IPv6
- 8 offline unit tests (`python -m unittest -v`)
- README, `requirements.txt`, `.gitignore`

**Do not rewrite the base.** Build on top of it.

---

## 3. Setup (everyone, ~5 minutes)

1. Accept the GitHub collaborator invite (check your email or github.com/notifications).
2. Clone and install:

```bash
git clone <REPO-URL>
cd ip-address-app
pip install -r requirements.txt
```

3. Check that it works:

```bash
python -m unittest -v     # should say OK (8 tests)
python main.py            # try options 1, 2, 3, then q
```

> Option 2 saying **"Not available on this network"** is normal. Most PH home and school networks don't have IPv6. Try mobile data if you want to see a real IPv6 address.

---

## 4. How the code is organized

| File | Purpose | Rule |
| --- | --- | --- |
| `main.py` | Menu loop + one small `option_...()` function per feature | Register your feature with **one line** in `MENU` |
| `api_client.py` | All REST API calls. Returns data, **never prints** | Raise `IPLookupError` when something fails |
| `display.py` | Everything that prints to the screen | All formatting changes go here |
| `config.py` | API URLs, timeout, headers, app name | No hard-coded URLs anywhere else |
| `test_api_client.py` | Offline tests with fake API responses | Add tests for new logic |

**Adding a menu option** — the only change you need in `main.py`:

```python
def option_lookup_ip():
    """Look up details for any IP the user enters."""
    ...

MENU = {
    "1": ("Show my public IPv4 address", option_show_ipv4),
    "2": ("Show my public IPv6 address", option_show_ipv6),
    "3": ("Show full IP details (location, ISP, ASN)", option_show_details),
    "4": ("Look up any IP address", option_lookup_ip),   # <- your line
}
```

**Menu numbers are reserved so branches don't clash:**
- `"4"` → Asher (Lookup any IP)
- `"5"` → Chylle (Export results)

Any error raised as `api_client.IPLookupError` is already caught by `main()` and shown as `[ERROR] ...`, so you don't need your own try/except for API failures.

---

## 5. GitHub workflow (follow exactly — this is graded)

### Branches

| Branch | Owner |
| --- | --- |
| `main` | Protected. Only changes through Pull Requests |
| `feature/ip-lookup` | Asher |
| `feature/formatted-output` | Chylle |

### Steps

```bash
# 1. Start from the latest main
git checkout main
git pull

# 2. Create your branch
git checkout -b feature/<your-branch>

# 3. Work, then commit in small steps with clear messages
git add .
git commit -m "Add IP validation using ipaddress module"

# 4. Push your branch
git push -u origin feature/<your-branch>
```

5. On GitHub, open a **Pull Request** into `main`. Title: what the feature does. Description: what changed + how you tested it.
6. **Request a review** from a teammate (Asher ↔ Chylle review each other).
7. Reviewer pulls the branch, runs the tests and the app, leaves **at least one comment**, then approves.
8. Merge with **"Squash and merge"** or **"Merge pull request"**. Delete the branch afterward.

### If the second PR has a conflict

The first PR to merge wins. The second person does:

```bash
git checkout main
git pull
git checkout feature/<your-branch>
git merge main
# fix conflicts (usually just the MENU dict and requirements.txt — keep BOTH lines)
git add .
git commit -m "Merge main into feature branch"
git push
```

**Take screenshots as you go** (Chylle needs them for the rubric and deck): branch list, an open PR, a review comment, an approval, the merge, the commit history, the collaborators page.

---

## 6. Feature A — IP Lookup & Analysis (Asher)

**Branch:** `feature/ip-lookup` · **Menu key:** `"4"`

**What it does:** the user types any IPv4 or IPv6 address and gets its details plus a technical analysis.

### Requirements

- [ ] Prompt: `Enter an IP address: `
- [ ] Validate with Python's built-in `ipaddress` module. Invalid input → `[ERROR] '<input>' is not a valid IP address.`
- [ ] Show an **analysis** block:
  - IP version (IPv4 / IPv6)
  - Type: Public / Private / Loopback / Link-local / Multicast / Reserved
  - IPv4 only: address class (A, B, C, D, E)
- [ ] For **public** IPs only, call the existing `api_client.get_ip_details(ip)` and show it with `display.show_details()`. For private IPs, print that location lookup isn't possible for private addresses (don't call the API).
- [ ] Put the analysis logic in a new function, e.g. `analyze_ip(ip_string)` in a new file `ip_analysis.py`, returning a dict (no printing).
- [ ] Add tests in `test_ip_analysis.py`, at minimum: `8.8.8.8` (public, class A), `192.168.1.1` (private, class C), `127.0.0.1` (loopback), `2001:4860:4860::8888` (IPv6 public), `abc` (invalid).
- [ ] Docstrings and comments on every new function.

### Hints

```python
import ipaddress
ip = ipaddress.ip_address("192.168.1.1")
ip.version        # 4
ip.is_private     # True
ip.is_loopback, ip.is_link_local, ip.is_multicast, ip.is_reserved
int(str(ip).split(".")[0])   # first octet -> class: 0-127 A, 128-191 B, 192-223 C, 224-239 D, 240-255 E
```

### Asher's other tasks
- [ ] Review and merge Chylle's PR
- [ ] Run the full test suite on merged `main`
- [ ] Fill in the **GitHub section** of the rubric (Section 9 has the draft)
- [ ] Prepare the **demo laptop** for the presentation (Section 11)

---

## 7. Feature B — Formatted Output & Export (Chylle)

**Branch:** `feature/formatted-output` · **Menu key:** `"5"`

**What it does:** makes the output readable for technicians and lets them save results.

### Requirements

- [ ] Add `rich` to `requirements.txt` (`rich>=13`)
- [ ] In `display.py`, upgrade:
  - `show_header()` → colored banner/panel
  - `show_details()` → two-column table (Field | Value), title "IP Details"
  - `show_ip()` → green for an address, yellow for "Not available"
  - `show_error()` → red text
  - Keep **the same function names and parameters** so `main.py` and Asher's feature keep working without changes.
- [ ] New menu option `"5"`: **Export my IP details**
  - Fetch IPv4, IPv6 and details (same calls as option 3)
  - Save to `exports/ip_report_<YYYYMMDD_HHMMSS>.json` **and** `.csv`
  - Create the `exports/` folder if missing (`os.makedirs("exports", exist_ok=True)`)
  - Print the saved file paths
- [ ] Put export logic in a new file `exporter.py` (functions `export_json(data)` and `export_csv(data)` returning the file path)
- [ ] Docstrings and comments on every new function

### Hints

```python
from rich.console import Console
from rich.table import Table

console = Console()
table = Table(title="IP Details")
table.add_column("Field", style="cyan")
table.add_column("Value", style="white")
table.add_row("ASN", "AS9299")
console.print(table)
```

### Chylle's other tasks
- [ ] Review and comment on Asher's PR
- [ ] Complete the **rubric document** (Section 9)
- [ ] Write the **backlog** and **team reflection** (Sections 10 and 12)
- [ ] Build the **presentation deck** (Section 11) and send it to Shane by **Oct 27, 8:00 AM**
- [ ] Update the README team table and feature list after merging

---

## 8. Timeline

| When (Oct 26–27) | Who | What |
| --- | --- | --- |
| By **7:30 PM** | All | Accept invite, clone, run tests (Section 3) |
| By **9:30 PM** | Asher, Chylle | Features coded and pushed, PRs opened |
| By **10:30 PM** | Asher, Chylle | Cross-review, fix comments, merge both PRs |
| By **11:00 PM** | Shane | Pull merged `main`, run full QA checklist (below), report bugs in group chat |
| By **11:30 PM** | Chylle, Asher | Rubric complete, screenshots attached |
| **11:59 PM** | Chylle | **Submit** rubric + GitHub link |
| Oct 27, **8:00 AM** | Chylle | Deck sent to everyone |
| Oct 27, before class | All | One full timed rehearsal (aim for 12–13 min) |

Post a short update in the group chat when you finish each item: `DONE: <task>` or `BLOCKED: <task> — <reason>`.

### QA checklist (Shane, on merged `main`)

- [ ] `pip install -r requirements.txt` works on a fresh clone
- [ ] `python -m unittest -v` → all tests pass
- [ ] Option 1 shows IPv4
- [ ] Option 2 shows IPv6 or "Not available on this network" (no crash)
- [ ] Option 3 shows the details table with ISP, ASN, country code
- [ ] Option 4: `8.8.8.8`, `192.168.1.1`, `127.0.0.1`, `2001:4860:4860::8888`, `hello` all behave correctly
- [ ] Option 5 creates JSON and CSV files in `exports/` that open correctly
- [ ] Invalid menu choice → error message, menu shows again
- [ ] Wi-Fi off → error message, no crash
- [ ] `q` quits cleanly; Ctrl+C quits cleanly

---

## 9. Rubric answers (drafts — edit and paste)

**Owner: Chylle** (except the GitHub section: **Asher**)

### Social coding selection
**Option 2: New application – IPv4/IPv6 Address Application**

**Reasons:** We chose to build a new application instead of enhancing an existing one. That let us design the code structure ourselves, from a modular layout to error handling and tests. It also fits our networking background: IPv4/IPv6 addressing, ISPs and ASNs tie directly to our CCNA coursework, and the app is useful to network technicians.

**Description and objectives:** A Python command-line tool that shows network technicians the computer's current public addressing information. Its objectives are to:
1. Retrieve the public IPv4 and IPv6 addresses through REST APIs (ipify).
2. Show geolocation, ISP, ASN and country code (ipapi.co).
3. Let the user look up and classify any IP address (version, public/private, class).
4. Present results in clear, color-formatted tables and export them to JSON/CSV.
5. Handle network and API errors without crashing.

### Team member roles and skillsets

| Team member | Role/Knowledge/Skillset |
| --- | --- |
| Matthew | Scrum Leader. Built the base application and set up the GitHub repository. CCNA networking, Python, Agile/Scrum. |
| Asher | Developer. Built IP Lookup & Analysis; handled code reviews and merges. Python, backend logic, testing. |
| Chylle | Recorder / Developer. Built Formatted Output & Export; documentation and presentation. UI/UX, documentation. |
| Shane | Lead Presenter / QA. Led the presentation and final quality-assurance testing. Communication, testing. |

### Strategy / project plan
The Scrum Leader first built and pushed a modular base application with separate files for API calls, display, configuration and tests. Each developer then built one feature on its own GitHub branch and added it to the menu with a single registration line, which kept merge conflicts small. All changes went through pull requests reviewed by a teammate before merging. The Lead Presenter ran the final QA checklist on the merged code, and the Recorder handled documentation, the rubric and the deck. Progress was tracked through task status updates in the team group chat.

### Using GitHub for collaboration — **Asher**
**Repository link:** `<paste link>`

- **Create branches:** The base application was pushed to `main`, which was protected so changes could only come in through pull requests. Each developer created a feature branch from `main` (`feature/ip-lookup`, `feature/formatted-output`) and committed their work there.
- **Add team members:** The Scrum Leader created the repository and invited all members as collaborators through Settings → Collaborators. Each member accepted the invite and cloned the repository.
- **Pull requests, code review, merge:** Each developer pushed their branch and opened a pull request into `main` describing the change and how it was tested. A teammate pulled the branch, ran the unit tests and the app, left review comments and approved it. After approval the PR was merged and the branch deleted. `<Add: any conflict you resolved and how.>`

---

## 10. Backlog (future enhancements)

**Owner: Chylle** — use this list in the rubric and on the backlog slide.

1. GUI or web dashboard (Tkinter or Flask)
2. Map view using latitude/longitude
3. Lookup history saved locally
4. Bulk lookup from a text file of IP addresses
5. Backup API when ipapi.co is rate-limited (e.g. ip-api.com)
6. Reverse DNS and WHOIS lookup
7. Subnet calculator (CIDR, subnet mask, host range)
8. Command-line arguments for scripting (e.g. `python main.py --ipv4`)

---

## 11. Presentation (10–15 minutes)

**Deck: Chylle** · **Lead speaker: Shane** · Everyone speaks.

| # | Slide | Speaker | Time |
| --- | --- | --- | --- |
| 1 | Title + team members and roles | Shane | 0:30 |
| 2 | The problem & why we chose Option 2 | Shane | 1:00 |
| 3 | Team roles & Scrum strategy | **Matthew** | 1:30 |
| 4 | APIs used (ipify, ipapi.co) and what each returns | Shane | 1:00 |
| 5 | Features + why we chose each one | Shane | 1:30 |
| 6 | Code structure & documentation (file table, `MENU` pattern) | **Asher** | 1:30 |
| 7 | GitHub workflow (branches, PRs, reviews — screenshots) | **Asher** | 1:00 |
| 8 | **Live demo** (options 1→5) | Shane (Asher at the keyboard) | 2:30 |
| 9 | Backlog / future enhancements | Shane | 0:45 |
| 10 | Reflection: issues, solutions, lessons | **Chylle** | 1:30 |
| 11 | Team activities & dynamics | **Chylle** | 1:00 |
| 12 | Closing + Q&A | Shane | 0:30 |
| | **Total** | | **~13:15** |

### Demo prep (Asher)
- Fresh pull of `main`, dependencies installed, terminal font enlarged.
- Run each option once before presenting (wakes up the APIs, confirms internet).
- **Backup:** screenshots of every option in the deck's appendix in case the venue Wi-Fi or ipapi.co fails. If ipapi.co rate-limits during the demo, Shane says so and switches to the screenshots — the error message itself shows our error handling works.

### Talking points for Shane (features slide)
- **IPv4 + IPv6:** technicians need both; the app clearly says when IPv6 isn't available instead of crashing.
- **ISP + ASN + location:** identifies who routes the traffic — useful when troubleshooting with a provider.
- **Lookup any IP:** technicians check other addresses, not just their own; the analysis catches private/loopback addresses instantly.
- **Formatted tables:** faster to read during troubleshooting.
- **Export:** results can be attached to tickets or reports.

---

## 12. Team reflection (Chylle collects, everyone contributes)

Each member sends Chylle 2–3 sentences per question by **11:00 PM**. Chylle combines them for the rubric and slides 10–11.

1. What did you enjoy about working as a team? What worked well?
2. What team problems did you encounter and how did you resolve them?
3. What technical problems did you encounter and how did you resolve them?
4. How was each member held accountable individually and as a team?
5. What was the team's decision-making process?
6. Overall, how were the team dynamics, and what lessons did you learn?

**Good examples to mention (if they happen):** IPv6 not available on school/home networks; ipapi.co rate limits; merge conflicts in `MENU` or `requirements.txt`; accountability through PR reviews and `DONE/BLOCKED` updates; working within a one-day deadline.

---

## 13. Troubleshooting

| Problem | Fix |
| --- | --- |
| `ModuleNotFoundError: requests` / `rich` | `pip install -r requirements.txt` |
| `pip` not found | Use `python -m pip install -r requirements.txt` |
| IPv6 "Not available" | Normal. Try mobile data/hotspot to see a real one |
| `API rate limit reached` | ipapi.co free limit hit. Wait, or switch network |
| `git push` rejected | `git pull` first, fix any conflicts, push again |
| Can't push to `main` | Correct — it's protected. Push your branch and open a PR |
| Conflict in `MENU` | Keep **both** menu lines, then commit |
| Colors look broken on Windows | Use Windows Terminal or VS Code terminal instead of old cmd |
