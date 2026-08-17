# Team charter

## How we work

**The specification is the referee.** When two of us disagree on what a
story means, we read it before arguing. If it is silent, the product
owner decides and the specification is updated — in that order.

**Disagreement is settled in ten minutes or escalated.** Two people
debating an approach for half an hour costs more than either approach
being wrong. Ten minutes, then the hat owner decides, and the loser
implements it without sulking.

**We say we are stuck within the hour.** Not at the standup the next
morning. On a {{DEV_DAYS}}-day project, a day lost is a measurable share
of the capacity.

**We do not silently reduce the scope.** Cutting a story is a team
decision, recorded on the board. Delivering half a story and calling it
done is how a demo breaks live.

**Nobody breaks `main` and goes to lunch.** If CI goes red, either it is
fixed or the commit is reverted before you leave.

## Communication

| Channel | For | Expected response |
|---|---|---|
| Team chat | Everything by default | Within the hour, working hours |
| Pull request | Anything about code | 4 hours, working hours |
| Voice / in person | Anything blocked for more than an hour | Immediately |
| Issue comments | Decisions that must survive the project | No response expected — it is the archive |

**Asynchronous by default, synchronous when blocked.** A question that
does not block anybody goes in the chat; a question that blocks you goes
in a call.

**A decision taken in a call is written down** in the issue or in an
ADR. If it only exists in someone's memory, it will be re-litigated
later in the week.

## Working hours

Fill in the hours each person is genuinely available, and the hard
limits — transport, care, another commitment. A team that pretends
everybody is available until midnight plans on a fiction.

| Name | Hours | Hard limits |
|---|---|---|
| _to fill in_ | | |

## What we do not do

- We do not push directly to `main`.
- We do not merge our own PR without a review.
- We do not add a dependency without saying so.
- We do not present a hypothesis as a fact — not in the code, not to
  whoever is judging the work.
