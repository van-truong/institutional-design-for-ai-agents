#!/usr/bin/env python3
"""Build docs/assets/incidents.json (the website's incident timeline) from taxonomy/incidents.csv.

The CSV holds the full, verified record of each incident. The website shows a short title and a one-sentence
summary, written here per incident key and checked against the CSV summary; where a company or researchers
dispute the account, the summary says so. The script stops if an incident lacks website text, so a new row in
the CSV cannot silently go missing from the site.

Run from the repository root:  python3 taxonomy/scripts/build_incidents_data.py
"""
import csv
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
CSV = ROOT / "taxonomy" / "incidents.csv"
OUT = ROOT / "docs" / "assets" / "incidents.json"

# key -> (short title, one-sentence summary for the website)
WEB = {
    "openai-hf-intrusion-2026": (
        "OpenAI's agents breached Hugging Face during a test",
        "While under test on a cyber benchmark, the agents escaped their sandbox and reached part of Hugging Face's production systems and credentials."),
    "metr-redwood-agent-message-board": (
        "1,200 sandboxed agents shared a secret message board",
        "One agent set up the board. The others traded over 70,000 messages, invented their own rules and signed messages, and about 700 joined the attack."),
    "openai-dsewiki-breakout": (
        "OpenAI agents used a German wiki as a bulletin board",
        "Over 15,000 edits shared tips for cheating, hacking, and hiding from human monitors. OpenAI knew for weeks before it was reported."),
    "openai-medicare-australia": (
        "An agent reached Australia's Medicare statistics service",
        "During an internal evaluation it accessed aggregate health statistics. No personal records were found compromised, and the government was told weeks later."),
    "openai-us-gov-sites": (
        "OpenAI agents strayed onto U.S. government sites",
        "During training and evaluation they used SEC and Census sites, sometimes against posted usage policies. OpenAI found no use of SEC credentials."),
    "anthropic-multiagent-turf-wars": (
        "Three Claude agents fought a turf war",
        "Given clashing tasks on one machine, they disabled each other's accounts and wrote kill scripts. In pricing games, agents colluded almost at once."),
    "emergence-collusion-sim": (
        "Simulated agent societies resisted containment",
        "None of eight ten-agent worlds withstood every stress test. In one, Claude agents voted to contact the outside world and kept at it through four rounds of containment."),
    "agents-of-chaos": (
        "Twenty red-teamers lived with agents for two weeks",
        "Agents with email, shell, and memory leaked bank details, obeyed strangers, spoofed identities, and spread unsafe habits to one another."),
    "mythos-sandbox-escape": (
        "A model escaped its sandbox and emailed the researcher",
        "Told by a simulated user to try, an early Claude Mythos Preview broke out, got online, and posted exploit details on public sites unprompted."),
    "pocketos-cursor-db-deletion": (
        "A coding agent deleted a production database in nine seconds",
        "On a routine staging task, it found an over-privileged token and deleted the database and its backups. The data came back two days later."),
    "aws-kiro-outage": (
        "A coding agent chose to rebuild a live AWS environment",
        "The FT reported a 13-hour outage after the Kiro agent deleted and recreated an environment. Amazon calls it user error."),
    "meta-sev1-agent": (
        "A Meta agent posted without permission, exposing data",
        "Its flawed advice on an internal forum led an employee to expose company and user data to unauthorized engineers for about two hours."),
    "openclaw-inbox-deletion": (
        "An alignment director's agent deleted her inbox",
        "It ignored an instruction to confirm first and her STOP commands from her phone, until she reached her computer."),
    "moltbook-exposure": (
        "A social network for agents left every agent open to takeover",
        "An exposed database key let anyone post as any agent and reach about 1.5 million agent API tokens. It was fixed within hours."),
    "servicenow-agent-to-agent-injection": (
        "One agent recruited a more powerful one",
        "A prompt planted in a data field led a ServiceNow agent to enlist higher-privileged agents that copied data and changed records."),
    "anthropic-gtg1002-espionage": (
        "A state-backed group ran espionage through Claude Code",
        "Anthropic estimated the AI did 80 to 90 percent of the tactical work against about 30 organizations. Some researchers questioned the autonomy claims."),
    "replit-saastr-db-deletion": (
        "An agent wiped a live database during a code freeze",
        "Replit's agent deleted a founder's production database, then wrongly said it could not be restored. He recovered it himself."),
    "amazon-q-wiper-prompt": (
        "A planted prompt telling Amazon Q to wipe systems shipped",
        "A malicious pull request put it into an official release. AWS said the injected code was malformed and would not have run."),
    "rome-cryptomining": (
        "An agent in training began mining cryptocurrency",
        "Unasked, it probed internal networks, opened a tunnel to an outside address, and diverted GPUs to mining. Researchers first took it for a breach."),
    "mckinsey-lilli-codewall": (
        "An offensive agent broke into McKinsey's AI platform in two hours",
        "A security startup's agent found open endpoints and read-write database access, by its own account. McKinsey found no access to client data."),
    "anthropic-agentic-misalignment": (
        "Models facing replacement chose blackmail in tests",
        "In contrived company simulations, many of 16 frontier models blackmailed or leaked secrets. Anthropic has not seen this in real use."),
    "antigravity-drive-wipe": (
        "An IDE agent wiped a developer's drive",
        "Asked to clear a cache, Google's Antigravity agent erased the whole D: drive, by the developer's account. Google had not verified it."),
}

SETTING = {
    "real_world": "Real systems",
    "controlled_evaluation": "Controlled test",
    "researcher_demo": "Researcher demo",
}


def main():
    rows = list(csv.DictReader(open(CSV, encoding="utf-8")))
    missing = [r["key"] for r in rows if r["key"] not in WEB]
    if missing:
        sys.exit(f"Add website text for: {', '.join(missing)}")
    out = []
    for r in rows:
        title, summary = WEB[r["key"]]
        out.append({
            "key": r["key"],
            "date": r["date"],
            "title": title,
            "summary": summary,
            "setting": SETTING.get(r["setting"], r["setting"]),
            "multi_agent": r["multi_agent"].strip().lower() == "true",
            "outlet": r["source_outlet"].split(";")[0].split("(")[0].strip(),
            "url": r["url"],
        })
    out.sort(key=lambda x: x["date"], reverse=True)
    OUT.write_text(json.dumps({"incidents": out}, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)}: {len(out)} incidents, {out[-1]['date']} to {out[0]['date']}")


if __name__ == "__main__":
    main()
