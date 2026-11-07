# Record the PromiseGate demo

Record the live Mattermost room and the final local Markdown receipt. Start
with the agent already attached. Trim the waits between replies.

| Time | On screen | Narration |
| --- | --- | --- |
| 0:00–0:15 | Mattermost channel and the registered agent in Switch Console | “What happens when our release notes promise more than QA verified? PromiseGate lets a team catch that in the release channel before the copy goes out.” |
| 0:15–0:45 | Send message 1. Show the agent’s two failures and check IDs. | “Switch passes the draft to our Codex reviewer. The checker finds that Free-plan CSV export and Excel export are unsupported.” |
| 0:45–1:10 | Send message 2. Show the exact revised copy and revision. | “I choose what we’re comfortable promising. The reviewer narrows the copy to Pro CSV and gives me an exact revision to approve.” |
| 1:10–1:40 | Send message 3. Open the receipt returned by the agent. | “The checker revalidates the revision and writes a release note with the evidence IDs. Switch keeps the evidence, decision and approval in the same conversation.” |

## Messages to send

1. `@promise-review Review this draft for export-2.8.0: Workspace admins on every plan can export reports as CSV. Pro workspace admins can also export Excel workbooks.`
2. In the same thread, send `@promise-review Limit CSV export to Pro workspace admins and remove the Excel claim. Show me the exact copy to approve.`
3. In the same thread, copy the agent’s exact `@promise-review approve <full revision>` message and send it.

## Submission description

PromiseGate helps release teams prevent unsupported customer promises.
Switch connects Mattermost to a Codex reviewer, which checks proposed claims
against a release evidence manifest. The owner chooses what to remove or
narrow and approves a specific revision in the thread. A deterministic
checker then produces a Markdown release note with a record of the checks
that support the final wording.

## Submit

Push this directory to a GitHub repository you control and ensure judges can
open it. Record and upload the live demo and verify the video link. Enter
**Best Business Workflow** with the repo, README and video via the organizer’s
[manual submission page](https://www.wemakedevs.org/hackathons/switch/submit)
before **November 7, 2026 at 11:59 p.m. IST**.
