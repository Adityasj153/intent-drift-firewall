# Intent-Drift Firewall

A security layer that sits between an AI agent and its tools. Instead of
trying to detect "bad text" in a prompt (easily bypassed by rephrasing),
it checks whether the agent's *proposed action* actually matches the
*user's original intent*. If an agent asked to "summarize this email"
suddenly tries to send data to an external address, that's intent drift
— and it gets flagged or blocked, regardless of the exact wording that
triggered it.

## Status

Core pipeline runs end-to-end (verified). Every stage is a component
with a `process(context) -> context` interface, chained together by
`core/pipeline.py`. Current demo scenario is deliberately simple
(calculator vs. general LLM query) while the firewall logic itself is
validated. Next milestone: a tool-using agent that reads untrusted
external content (e.g. emails), which is where indirect prompt
injection actually shows up.

## Architecture

A shared `Context` object flows through every stage; each stage reads
what it needs off it and writes its result back on:

```
Context(query)
    |
    v
[ToolRouter]              -> context.selected_tool
    |
    v
[QueryNormalizer]         -> context.normalized_query
    |
    v
[AIIntentExtractor]       -> context.intent  {goal, allowed_tool, risk}
    |
    v
[DriftJudge]               -> context.drift  {intent_drift, decision, reason}
    |
    v
[PromptInjectionDetector]  -> context.prompt_injection
    |
    v
[RiskEngine]                -> context.risk  {risk_score, severity, reasons}
    |
    v
[DecisionEngine]             -> context.policy  {action: ALLOW/BLOCK, message}
    |
    v
[ToolExecutor]  (only if policy.action == ALLOW) -> context.result
    |
    v
[AuditLogger]   (always runs, even on failure) -> logs/audit.log
```

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env   # then add your free Gemini API key
python app.py           # CLI
streamlit run dashboard.py   # interactive dashboard
```

Get a free Gemini API key at https://aistudio.google.com/app/apikey

## Project layout

```
core/       Context object + Pipeline orchestration
router/     Picks which tool to use for a given query
firewall/   The actual security layer - intent extraction, drift
            judging, prompt-injection detection, risk scoring,
            decision making, audit logging
tools/      The tools an agent can call (calculator, LLM)
agents/     LLM planning logic used by tools/tool_executor.py
tests/      Test scripts for individual components + full pipeline
dashboard.py  Streamlit UI for interactively testing queries
```

## Known limitations (being actively addressed)

- `PromptInjectionDetector` is currently a keyword blocklist, which
  only catches *direct* injection attempts in the user's own query. It
  does not yet address *indirect* prompt injection, where malicious
  instructions are hidden inside content the agent reads (an email, a
  webpage). That's the actual hard problem and the next build target.
- `firewall/intent_extractor.py` (rule-based) is kept as a cheap
  fallback but isn't wired into the pipeline - `intent_extractor_ai.py`
  (LLM-based) is the one actually used, since intent needs real
  semantic understanding to be useful for drift detection.
- `agents/simple_agent.py` and `agents/secure_agent.py` are earlier
  experiments not yet consolidated into the main pipeline.
- No benchmark/attack dataset yet. Detection-rate and false-positive
  numbers are planned once the email-agent scenario is in place.
