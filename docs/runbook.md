# Live event support runbook

How the virtual agent and the human support team prepare for, run, and wrap up a tier-1 live event.

## Roles

| Role | During the event |
|---|---|
| **CS operations lead** | Owns the surge mode. Changes modes based on the dashboard and the incident commander. |
| **Incident commander** (engineering) | Declares and resolves incidents. Owns the incident record (scope, ETA). |
| **Conversation designer on call** | Watches live transcripts, approves message changes, flags agent failures. |
| **Localization on call** | Approves any new or changed message in launch locales. |
| **Human support leads** | Manage the protected queue and callbacks. |

## Before the event

### T-7 days
- [ ] Event record complete: title per locale, start time, regions, plans that include it, replay availability
- [ ] Event FAQ written and loaded as retrievable help content in every launch locale
- [ ] Fast-path flows tested against the event record (sign-in, can't find it, payment, buffering)
- [ ] Incident message templates approved in every launch locale (see below)
- [ ] Golden-set items for this event's intents added and passing (see golden-dataset-kit)
- [ ] Human staffing plan by language and hour, including the protected payments lane

### T-24 hours
- [ ] Dry run: switch a test environment through every mode; confirm the agent's behavior changes
- [ ] Banner copy approved in every locale for elevated, surge, and incident
- [ ] Callback scheduling capacity confirmed for the 24 hours after the event

### T-60 minutes
- [ ] Mode → **elevated**
- [ ] Banner live
- [ ] Conversation designer watching live transcripts

## During the event

| Signal | Action | Who |
|---|---|---|
| Contact rate > 2x baseline | Confirm **elevated** | CS ops lead |
| Contact rate > 5x baseline, or human wait > 10 min | Switch to **surge** | CS ops lead |
| Incident declared | Switch to **incident**; confirm incident message is live in every locale within 5 minutes | CS ops lead + localization |
| Cluster of unresolved buffering reports in one region/device, no incident yet | Send the cluster to the incident commander | Conversation designer |
| Agent behaving wrong (troubleshooting during incident, inventing ETAs) | Pull transcript, fix config or message, notify CS ops | Conversation designer |
| Incident resolved | Update message to "fixed, restart the stream"; step down to **surge** or **elevated** | CS ops lead |

**Mode changes are human decisions.** The dashboard recommends; a person switches. A wrongly declared incident tells millions of members the problem is on our side when it isn't.

## Incident message templates

Pre-approved in every launch locale. Only the bracketed slots change during the event, and slot values come from the incident record.

**Active**
> We're having a problem with the live stream right now that's affecting some members [in your area | on some TVs]. It's on our side, and our team is working on it. You don't need to restart anything.

**Active, with ETA** (only if the incident record has one)
> ... We expect it to be fixed in about [minutes] minutes.

**Resolved**
> The problem with the live stream is fixed. If it's still not playing, back out of the event and start it again.

## After the event

- [ ] Step down to **normal** when contact rate is back under 2x baseline
- [ ] Callback queue worked oldest-first; completion tracked
- [ ] Replay banner live (if applicable)
- [ ] Post-event review scheduled within 3 business days (see [post-event-review.md](post-event-review.md))
