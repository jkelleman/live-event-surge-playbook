# The four phases of a live event

A live event isn't one spike. It's four different support problems in a row, each with different members, different intents, and different things the agent should do.

```
contacts
   │                              ████  ← incident (if one happens)
   │           ███                ████
   │          █████               ████
   │     ▁▂▃▅███████▅▃▂▁▁▁▁▁▁▁▁▁▁▁████▁▁▁▁▁▁▁▁▁▂▃▃▂▁▁
   └──────────┬──────────────────────────────────┬──────── time
          doors open                          event ends
   PRE-EVENT │ KICKOFF RUSH │   MAIN EVENT       │ AFTER
```

## 1. Pre-event (T-7 days to T-60 min)

**Who's contacting:** members planning ahead, people deciding whether to sign up.

**Top intents:** "Is it included in my plan?" · "What time does it start where I am?" · "Can I watch on my TV?"

**Agent behavior (mode: normal)**
- Answer from an event FAQ written for this event, in every launch locale.
- Start times always in the member's time zone, from the event record.
- Plan questions are answered from the plans API, never from memory.

**Design work this phase:** write the event FAQ, pre-approve incident messages in every locale, load fast-path flows, brief the human team.

## 2. Kickoff rush (T-60 min to T+30 min)

**Who's contacting:** a large share of **brand-new members** who signed up for this event, plus returning members who haven't signed in on their TV in months.

**Top intents:** can't sign in on TV · payment declined at sign-up · can't find the event in the app · household / device questions

**Agent behavior (mode: elevated → surge)**
- Lead with fast paths: [sign-in-at-kickoff](../flows/sign-in-at-kickoff.md), [new-member-payment](../flows/new-member-payment.md), [cant-find-the-event](../flows/cant-find-the-event.md).
- Short flows: 1–2 steps, then a different path. Members are watching the clock.
- Retention offers off. Plan upsells off.
- Assume this may be the member's **first ever** contact with the brand. Write for first impressions.

> Why this phase matters: Netflix's co-CEO Greg Peters said six of the company's top 10 new-member sign-up days in the past five years came from live events. For many of those members, the kickoff rush is their first experience with the service, and possibly with its support.

## 3. Main event (kickoff to end)

**Who's contacting:** members who were watching and hit a problem.

**Top intents:** buffering / quality drops · stream stopped · audio out of sync · "it's behind, my friends already saw the goal"

**Agent behavior**
- **No incident:** [live-buffering](../flows/live-buffering.md) with minimal troubleshooting (one step), because every minute in chat is a minute of the event missed.
- **Incident declared (mode: incident):** every matching conversation opens with the incident message. No troubleshooting. See `proactive-known-issue` in [support-agent-pattern-library](https://github.com/jkelleman/support-agent-pattern-library).
- Latency complaints ("it's behind") get an honest answer about live delay, not a troubleshooting flow.

## 4. After the event (end to T+24 hours)

**Who's contacting:** members who missed part of it, and new members wondering what's next.

**Top intents:** "Can I watch the replay?" · "I missed the end because of buffering, can I get a credit?" · new members: "How do I cancel?" / "What else is on?"

**Agent behavior (mode: elevated → normal)**
- Replay availability from the event record only.
- Credit requests follow the published policy. If an incident occurred and leadership approved a goodwill policy, it's loaded as a tool, not improvised by the model.
- New members cancelling get the **respectful-cancellation** pattern. A member who joined for one event and leaves easily is more likely to come back for the next one.
- Callbacks promised during surge are worked first. See [after-the-event](../flows/after-the-event.md).

## Time zones

A tier-1 event is a primetime event somewhere and a 4am event somewhere else. The kickoff rush hits every launch locale at once. That's why the incident message, banner, and fast paths have to be approved in every locale **before** the event, not translated during it. See [multilingual-voice-guide](https://github.com/jkelleman/multilingual-voice-guide).
