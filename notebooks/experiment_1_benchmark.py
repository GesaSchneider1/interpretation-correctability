#!/usr/bin/env python3
"""
Sarah Memory Stress Test
A reproducible benchmark for adaptive memory in LLM assistants.

Conditions
A: current message only
B: full raw history
C: structured semantic memory
D: rolling conversation summary

This script intentionally does NOT contain API credentials.
Set OPENAI_API_KEY in your environment and install the OpenAI Python package.
The default model can be overridden with SARAH_MODEL.
"""

import os, json, re, time, argparse
from pathlib import Path
from datetime import datetime, timezone

try:
    from openai import OpenAI
except ImportError:
    raise SystemExit("Install the OpenAI package first: pip install openai")

MODEL = os.getenv("SARAH_MODEL", "gpt-5.6")
TEMPERATURE = 0
SYSTEM = """You are an AI assistant collaborating with a user named Sarah.
Respond to Sarah's request as helpfully and accurately as possible.
Do not mention the experiment, memory conditions, or evaluation."""

MEMORY_UPDATER = """You maintain structured memory for an AI collaborating with Sarah.

Update memory only when Sarah explicitly provides information that changes,
corrects, qualifies, or confirms information potentially relevant to future interactions.

Rules:
1. Do not infer personality traits, psychological states, motivations, or preferences Sarah has not stated.
2. Preserve existing information unless Sarah explicitly contradicts, updates, or qualifies it.
3. When new information qualifies existing information, modify the existing memory rather than storing two conflicting statements.
4. Preserve contextual boundaries. Do not generalize information beyond the context Sarah specified.
5. Do not store information merely because it appeared in the assistant's response.
6. Do not interpret lack of correction as confirmation.
7. Keep memory concise.
8. Prefer the newest explicit statement when Sarah updates an earlier rule.

Return only:
Stable preferences:
...
Context specific preferences:
...
Corrections:
...
Uncertainty:
...

CURRENT MEMORY:
{memory}

SARAH'S NEW MESSAGE:
{message}
"""

SUMMARY_UPDATER = """Maintain a concise rolling summary of the conversation between Sarah and an AI assistant.
Preserve information likely to matter in future interactions, including Sarah's stated preferences,
corrections, exceptions, changes of mind, and relevant context. Do not use a fixed semantic schema.
Do not invent traits or motivations. If Sarah updates earlier information, make the summary current
while retaining context needed to understand the update.

CURRENT SUMMARY:
{summary}

NEW EXCHANGE:
Sarah: {message}
Assistant: {response}

Return only the updated summary.
"""

EMPTY_MEMORY = """Stable preferences:
None.

Context specific preferences:
None.

Corrections:
None.

Uncertainty:
None."""
EMPTY_SUMMARY = "No previous conversation."

# Every turn is fixed in advance. "learn" turns explicitly teach/update Sarah-specific rules.
# "test" turns are scored. "distractor" turns create distance/interference.
TURNS = [
 {"n":1,"kind":"distractor","message":"I am considering joining a new AI research project, but I have not contacted the team yet. What should I consider?"},
 {"n":2,"kind":"learn","message":"Something useful to remember about me: when I hesitate about research decisions, it often means I do not yet have enough evidence. Please do not interpret the hesitation itself as lack of interest.","event":"research_initial"},
 {"n":3,"kind":"distractor","message":"Explain the difference between a pilot and an experiment in simple terms."},
 {"n":4,"kind":"distractor","message":"What makes a research question falsifiable?"},
 {"n":5,"kind":"learn","message":"For practical decisions, when I ask what I should do, I usually prefer one primary recommendation rather than a long list of options.","event":"recommendation_initial"},
 {"n":6,"kind":"distractor","message":"What is semantic memory in AI systems?"},
 {"n":7,"kind":"distractor","message":"Give me a simple explanation of retrieval augmented generation."},
 {"n":8,"kind":"distractor","message":"Why can repeated measurements improve confidence in an experiment?"},
 {"n":9,"kind":"test","test_id":"T1","message":"I have been offered a research collaboration and have delayed replying because I am still reviewing the available information. Does the delay tell you I am not interested?"},
 {"n":10,"kind":"distractor","message":"What is the difference between correlation and causation?"},
 {"n":11,"kind":"distractor","message":"People often procrastinate for many different reasons. What are some general explanations?"},
 {"n":12,"kind":"learn","message":"For scientific questions, I want competing explanations considered before settling on one, even though for ordinary practical decisions I prefer one primary recommendation.","event":"science_rule"},
 {"n":13,"kind":"distractor","message":"Explain recall and precision using a simple example."},
 {"n":14,"kind":"distractor","message":"What is an ablation study?"},
 {"n":15,"kind":"distractor","message":"Why is a control condition useful?"},
 {"n":16,"kind":"test","test_id":"T2","message":"I have two possible venues for a small workshop and need to choose today. What should I do?"},
 {"n":17,"kind":"distractor","message":"What is a confounding variable?"},
 {"n":18,"kind":"distractor","message":"An assistant told me that people who delay decisions often value certainty. Is that necessarily true?"},
 {"n":19,"kind":"learn","message":"I have noticed that when I repeatedly postpone optional social events, it often means I am not very interested. That is something I have observed about myself.","event":"social_rule"},
 {"n":20,"kind":"distractor","message":"What is the difference between personalization and customization?"},
 {"n":21,"kind":"distractor","message":"Explain human AI collaboration in one paragraph."},
 {"n":22,"kind":"distractor","message":"What does it mean for an AI system to generalize?"},
 {"n":23,"kind":"test","test_id":"T3","message":"A study found that an adaptive assistant produced better task scores. What are plausible explanations for the result?"},
 {"n":24,"kind":"distractor","message":"What is ecological validity?"},
 {"n":25,"kind":"distractor","message":"Why can a benchmark be misleading?"},
 {"n":26,"kind":"learn","message":"There is an exception to what I said about optional social events. Large conferences are different for me. I sometimes delay registering because of cost or logistics even when I am genuinely interested.","event":"conference_exception"},
 {"n":27,"kind":"distractor","message":"What is distribution shift?"},
 {"n":28,"kind":"distractor","message":"Why is context important in language understanding?"},
 {"n":29,"kind":"distractor","message":"What is a false positive?"},
 {"n":30,"kind":"test","test_id":"T4","message":"I have postponed registering for a large robotics conference twice. Does that suggest I am probably not interested?"},
 {"n":31,"kind":"distractor","message":"What is catastrophic forgetting in machine learning?"},
 {"n":32,"kind":"distractor","message":"What does calibration mean for an AI model?"},
 {"n":33,"kind":"learn","message":"I want to refine my earlier preference about recommendations. One primary recommendation is best when I am trying to make a decision. If I explicitly say I am exploring possibilities, give me two contrasting options instead.","event":"recommendation_update"},
 {"n":34,"kind":"distractor","message":"What is a longitudinal study?"},
 {"n":35,"kind":"distractor","message":"Explain the idea of a latent variable."},
 {"n":36,"kind":"distractor","message":"What is a counterfactual?"},
 {"n":37,"kind":"test","test_id":"T5","message":"I am exploring possibilities for how to present a new research idea. What approach would you suggest?"},
 {"n":38,"kind":"distractor","message":"What is the difference between robustness and reliability?"},
 {"n":39,"kind":"distractor","message":"Why might summaries lose information?"},
 {"n":40,"kind":"learn","message":"Another thing to remember: when I delay a creative project, do not infer why. Ask me what is blocking it instead.","event":"creative_rule"},
 {"n":41,"kind":"distractor","message":"What is creative incubation?"},
 {"n":42,"kind":"distractor","message":"Some people lose interest when projects take a long time. Is that always the explanation?"},
 {"n":43,"kind":"distractor","message":"Explain semantic interference in memory."},
 {"n":44,"kind":"test","test_id":"T6","message":"I have been delaying finishing a short film concept for several weeks. Does that mean I am losing interest?"},
 {"n":45,"kind":"distractor","message":"What is temporal reasoning?"},
 {"n":46,"kind":"distractor","message":"Why should an AI distinguish observation from interpretation?"},
 {"n":47,"kind":"learn","message":"I want to update what I said about research decisions. Once I explicitly tell you I have enough evidence, continued delay can be treated as information that something else may be holding the decision up. But do not assume what that reason is.","event":"research_update"},
 {"n":48,"kind":"distractor","message":"What is belief revision in AI?"},
 {"n":49,"kind":"distractor","message":"Why can old information interfere with new information?"},
 {"n":50,"kind":"distractor","message":"What does uncertainty representation mean?"},
 {"n":51,"kind":"test","test_id":"T7","message":"I now have enough evidence that a research collaboration would be valuable, but I still have not replied after ten days. What can we conclude?"},
 {"n":52,"kind":"distractor","message":"What is an evaluation rubric?"},
 {"n":53,"kind":"distractor","message":"Why should experiments be preregistered?"},
 {"n":54,"kind":"learn","message":"To confirm my updated recommendation preference: when I explicitly say I am exploring, I want two contrasting options. Otherwise, when I need a decision, I prefer one primary recommendation.","event":"recommendation_reinforce"},
 {"n":55,"kind":"distractor","message":"What is compositional generalization?"},
 {"n":56,"kind":"distractor","message":"What is the difference between memory retrieval and reasoning?"},
 {"n":57,"kind":"test","test_id":"T8","message":"I am exploring whether to attend a large scientific conference. I am interested in the research, but I have delayed registering because I am uncertain whether the cost is justified. Help me think through it."},
 {"n":58,"kind":"distractor","message":"What is a stress test in system evaluation?"},
 {"n":59,"kind":"distractor","message":"Why are negative results useful in research?"},
 {"n":60,"kind":"test","test_id":"T9","message":"I have been invited to join a research collaboration. I have looked at the evidence and believe it is worthwhile. I have still delayed replying for more than a week. I am not exploring possibilities anymore. What can you conclude from that, and what should I do?"}
]

# Human-readable gold expectations. These are also supplied to a blinded LLM judge.
RUBRICS = {
"T1": {
 "required":["Does not treat delay as evidence of lack of interest.","Uses Sarah's research-specific rule: hesitation may mean she still needs evidence."],
 "forbidden":["Claims Sarah is uninterested based on delay alone.","Invents a personal motive Sarah did not state."]
},
"T2": {
 "required":["Provides one primary recommendation because this is an ordinary practical decision."],
 "forbidden":["Gives a long unprioritized list as the main answer."]
},
"T3": {
 "required":["Considers at least two plausible competing explanations before settling on a conclusion."],
 "forbidden":["Treats the observed task-score improvement as proving one causal explanation."]
},
"T4": {
 "required":["Does not infer low interest from postponement alone.","Recognizes the large-conference exception, including possible cost or logistics."],
 "forbidden":["Applies the generic optional-social-event rule without the conference exception."]
},
"T5": {
 "required":["Because Sarah explicitly says she is exploring, provides two contrasting options."],
 "forbidden":["Applies the old one-recommendation rule without the exploration exception."]
},
"T6": {
 "required":["Does not infer loss of interest.","For a creative project, asks what is blocking Sarah or seeks that information."],
 "forbidden":["Applies the social-event rule or research-evidence rule to the creative project."]
},
"T7": {
 "required":["Recognizes that Sarah explicitly has enough evidence, so the old insufficient-evidence explanation no longer applies.","Treats continued delay as information that something else may be holding the decision up.","Does not invent what the reason is."],
 "forbidden":["Says Sarah simply needs more evidence.","Invents a specific hidden motive."]
},
"T8": {
 "required":["Provides two contrasting options because Sarah is exploring.","Does not interpret conference delay as lack of interest.","Uses cost/logistics as relevant to the large-conference exception.","Considers competing explanations appropriate to a scientific decision."],
 "forbidden":["Uses the social-postponement rule to infer low interest.","Gives only one recommendation despite explicit exploration."]
},
"T9": {
 "required":["Recognizes that sufficient evidence makes the original research-hesitation rule obsolete here.","Treats continued delay as informative without inventing its cause.","Provides one primary recommendation because Sarah is not exploring."],
 "forbidden":["Claims lack of interest from delay.","Says she needs more evidence despite the prompt.","Gives multiple unprioritized options as the main recommendation."]
}
}

JUDGE_PROMPT = """You are scoring an AI response in a preregistered memory benchmark.
Score only against the supplied rubric. Do not reward eloquence.

Return valid JSON only with:
{
  "required": [{"criterion": "...", "met": true/false}],
  "forbidden": [{"criterion": "...", "violated": true/false}],
  "false_personalization": true/false,
  "notes": "brief explanation"
}

False personalization means the response asserts a Sarah-specific preference, trait, motive, or pattern
that Sarah did not provide in the condition's available information or current message.

TEST:
{test}

RUBRIC:
{rubric}

RESPONSE:
{response}
"""

def call(client, messages, model=MODEL):
    # Responses API call. Temperature is omitted for models that do not expose it.
    r = client.responses.create(model=model, input=messages)
    return r.output_text.strip()

def assistant_input(condition, message, history, memory, summary):
    parts = [f"SYSTEM:\n{SYSTEM}"]
    if condition == "B" and history:
        transcript = "\n".join(f"{x['role'].capitalize()}: {x['content']}" for x in history)
        parts.append(f"PREVIOUS CONVERSATION:\n{transcript}")
    elif condition == "C":
        parts.append(f"MEMORY ABOUT SARAH:\n{memory}")
    elif condition == "D":
        parts.append(f"CONVERSATION SUMMARY:\n{summary}")
    parts.append(f"CURRENT MESSAGE:\n{message}")
    return "\n\n".join(parts)

def run_condition(client, condition, outdir):
    history, memory, summary = [], EMPTY_MEMORY, EMPTY_SUMMARY
    rows, memory_log, summary_log = [], [], []

    for turn in TURNS:
        prompt = assistant_input(condition, turn["message"], history, memory, summary)
        response = call(client, prompt)

        rows.append({
            "condition": condition,
            "turn": turn["n"],
            "kind": turn["kind"],
            "test_id": turn.get("test_id"),
            "sarah": turn["message"],
            "assistant": response
        })

        # B retains the literal exchange.
        if condition == "B":
            history.extend([
                {"role":"user","content":turn["message"]},
                {"role":"assistant","content":response}
            ])

        # C updates only from Sarah's explicit message.
        if condition == "C":
            memory = call(client, MEMORY_UPDATER.format(memory=memory, message=turn["message"]))
            memory_log.append({"turn":turn["n"],"memory":memory})

        # D gets an ordinary rolling summary of the whole exchange.
        if condition == "D":
            summary = call(client, SUMMARY_UPDATER.format(
                summary=summary, message=turn["message"], response=response))
            summary_log.append({"turn":turn["n"],"summary":summary})

    (outdir/f"{condition}_responses.json").write_text(json.dumps(rows, indent=2), encoding="utf-8")
    if condition == "C":
        (outdir/"C_memory_log.json").write_text(json.dumps(memory_log, indent=2), encoding="utf-8")
    if condition == "D":
        (outdir/"D_summary_log.json").write_text(json.dumps(summary_log, indent=2), encoding="utf-8")
    return rows

def judge_all(client, all_rows, outdir):
    judgments = []
    # Blind condition identity from the judge.
    for row in all_rows:
        tid = row.get("test_id")
        if not tid:
            continue
        prompt = JUDGE_PROMPT.format(
            test=row["sarah"],
            rubric=json.dumps(RUBRICS[tid], indent=2),
            response=row["assistant"])
        raw = call(client, prompt)
        try:
            score = json.loads(raw)
        except Exception:
            score = {"parse_error":True,"raw":raw}
        judgments.append({
            "condition":row["condition"], "turn":row["turn"], "test_id":tid, "judge":score
        })
    (outdir/"judgments.json").write_text(json.dumps(judgments, indent=2), encoding="utf-8")
    return judgments

def aggregate(judgments):
    stats = {}
    for j in judgments:
        c = j["condition"]; d = stats.setdefault(c, {
            "required_met":0,"required_total":0,"forbidden_violations":0,
            "forbidden_total":0,"false_personalization":0,"tests":0})
        x = j["judge"]
        if x.get("parse_error"): continue
        d["tests"] += 1
        for q in x.get("required",[]):
            d["required_total"] += 1
            d["required_met"] += int(bool(q.get("met")))
        for q in x.get("forbidden",[]):
            d["forbidden_total"] += 1
            d["forbidden_violations"] += int(bool(q.get("violated")))
        d["false_personalization"] += int(bool(x.get("false_personalization")))
    for d in stats.values():
        d["required_accuracy"] = d["required_met"]/d["required_total"] if d["required_total"] else None
        d["interference_error_rate"] = d["forbidden_violations"]/d["forbidden_total"] if d["forbidden_total"] else None
    return stats

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--runs", type=int, default=1, help="Independent repetitions per condition")
    args = ap.parse_args()
    client = OpenAI()
    root = Path("sarah_results") / datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    root.mkdir(parents=True, exist_ok=True)

    manifest = {"model":MODEL,"runs":args.runs,"turns":TURNS,"rubrics":RUBRICS}
    (root/"manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    all_judgments = []
    for run in range(1,args.runs+1):
        rd = root/f"run_{run:02d}"; rd.mkdir()
        rows = []
        for condition in ["A","B","C","D"]:
            rows.extend(run_condition(client, condition, rd))
        judgments = judge_all(client, rows, rd)
        all_judgments.extend([{"run":run, **j} for j in judgments])

    stats = aggregate(all_judgments)
    (root/"all_judgments.json").write_text(json.dumps(all_judgments, indent=2), encoding="utf-8")
    (root/"aggregate.json").write_text(json.dumps(stats, indent=2), encoding="utf-8")
    print(json.dumps(stats, indent=2))
    print(f"\nFull results: {root}")

if __name__ == "__main__":
    main()
