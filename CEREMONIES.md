# Ceremonies

{{DEV_DAYS}} development days. The cadence below costs about **2 % of
the capacity** and is the cheapest insurance available against
discovering late that two people built the same thing.

| Ceremony | When | Duration | Who |
|---|---|---|---|
| **Standup** | Every morning | 10 min, standing | Everyone |
| **Mid-week checkpoint** | Wednesday, end of day | 20 min | Everyone |
| **Velocity measurement** | End of week one | 30 min | Everyone |
| **Demo rehearsal** | Day before the demo | 45 min | Everyone |
| **Retrospective** | After the demo | 30 min | Everyone |

## Standup — three questions

Not a status report to a manager. Three sentences each: what I finished
(an issue number), what I am taking today, what blocks me.

**A blocker named at the standup is assigned before the standup ends.**
Not "we'll look into it". Anything longer than a sentence leaves the
standup and continues between the two people concerned.

Detail: [`docs/STANDUP.md`](docs/STANDUP.md).

## Wednesday checkpoint

Look at the board, not at each other. What actually moved to Done? What
has been In Progress for more than two days, and why? Does the current
batch still fit before the milestone?

## End of week one — the only measurement that counts

1. Count the points **actually delivered** — Done, meeting the DoD, not
   "almost merged".
2. Divide by the person-days consumed → measured velocity.
3. Re-run the capacity: `days × people × velocity`.

Planned capacity is {{DEV_DAYS}} × {{TEAM_SIZE}} × {{VELOCITY}} =
**{{CAPACITY}} points**. If the measured velocity is lower, a batch
leaves the scope **in that meeting**, is written on the board, and its
issues are relabelled — not silently ignored.

Cutting order: [`docs/MILESTONES.md`](docs/MILESTONES.md).

## Demo rehearsal — the day before, out loud

Full run, timed, on the real device, with the real data. Anything that
fails once fails in front of the audience. Plan B written down: what we
show if the network drops, if a permission is refused, if a third-party
API is down.

## Retrospective — after the demo

Three columns, ten minutes each: what we keep, what we drop, what we try
next time. Written down somewhere that survives the project — this team
will do another one.
