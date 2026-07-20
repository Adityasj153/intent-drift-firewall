# Intent-Drift Firewall

A security layer that sits between an AI agent and its tools. Instead of
trying to detect "bad text" in a prompt (easily bypassed by rephrasing),
it checks whether the agent's *proposed action* actually matches the
*user's original intent*. If an agent asked to "summarize this email"
suddenly tries to send data to an external address, that's intent drift
— and it gets flagged or blocked, regardless of the exact wording that
triggered it.

## Status

Early-stage / actively being built. The core pipeline (router -> drift
judge -> risk engine -> decision engine) runs end-to-end. The current demo
scenario is deliberately simple (calculator vs. general LLM query) while
the firewall logic itself is validated. The next milestone is wiring in
a tool-using agent that reads untrusted external content (e.g. emails),
which is where indirect prompt injection actually shows up.

## Architecture

```
User query
    |
    v
[ToolRouter]        -> picks a tool (calculator / llm)
    |
    v
[DriftJudge]         -> LLM-as-judge: does the tool match the intent?
    |
    v
[PromptInjectionDetector] -> rule-based check for direct injection phrases
    |
    v
[RiskEngine]          -> combines drift + injection + tool into a risk score
    |
    v
[DecisionEngine]       -> ALLOW or BLOCK based on severity
    |
    v
Tool executes (if allowed)
```

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env   # then add your free Gemini API key
python app.py
```

Get a free Gemini API key at https://aistudio.google.com/app/apikey

## Project layout

```
agents/     Agent implementations (LLM planning logic)
router/     Picks which tool to use for a given query
firewall/   The actual security layer - intent extraction, drift
            judging, prompt-injection detection, risk scoring,
            decision making
tools/      The tools an agent can call (calculator, LLM)
tests/      Test scripts for individual components
```

## Known limitations (being actively addressed)

- `PromptInjectionDetector` is currently a keyword blocklist, which
  only catches *direct* injection attempts in the user's own query. It
  does not yet address *indirect* prompt injection, where malicious
  instructions are hidden inside content the agent reads (an email, a
  webpage). That's the actual hard problem and the next build target.
- `agents/simple_agent.py`, `agents/secure_agent.py`, and
  `agents/gemini_agent.py` are experiments from earlier iterations and
  aren't all wired into the main pipeline yet - consolidating these.
- No benchmark/attack dataset yet. Detection-rate and false-positive
  numbers are planned once the email-agent scenario is in place.
