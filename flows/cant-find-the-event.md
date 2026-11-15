# Flow: Can't find the event

**Phase:** Kickoff rush · **Modes:** elevated, surge · **Goal:** member on the event page in one turn

```mermaid
flowchart TD
    A[Member: where is the event?] --> B{Event started?}
    B -- not yet --> C[Start time in member's time zone<br/>+ Remind Me]
    B -- yes --> D{Available in member's region?}
    D -- yes --> E[Where it is on home screen<br/>+ search term]
    D -- no --> F[Plain explanation<br/>no workaround suggestions]
    E --> G{Found it?}
    G -- no --> H{Plan includes live?}
    H -- yes --> I[Check app version<br/>one step]
    H -- no --> J[Explain plan, link to plans<br/>no hard sell]
```

## Turns

**Before start**
> **Agent:** It starts at 8:00 PM your time, about 25 minutes from now. Search for the event name, or tap Remind Me on its page and we'll notify you when it starts.

**Not available in region**
> **Agent:** This event isn't available in your country, so it won't appear in your app. I'm sorry I can't change that.

## Design notes

- **Region availability:** state it plainly from the rights record. Never hint at workarounds.
- **"Is it included in my plan?"** comes from the plans API. If the answer is "no," explain once and link to plans. No pressure language at kickoff.
- **Search term:** give the exact title as it appears in the app in the member's locale, from the event record.

## Measure

- One-turn resolution rate (target: ≥ 80%)
- "Not available in region" contacts, by country (feeds the event FAQ and banner)
