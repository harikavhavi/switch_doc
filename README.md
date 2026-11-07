# PromiseGate

**An evidence gate for customer-facing release notes, inside a Switch room.**

Release notes often promise more than the release delivers. A support lead
might say CSV export is available on all plans, even though QA only verified
Pro. PromiseGate brings the draft, the failed checks, the human scope decision
and the final release note into one Mattermost thread.

Built for **Best Business Workflow** at Flip the Switch.

## What happens

1. The release owner posts draft copy in Mattermost. Switch routes the mention
   and room context to a dedicated Codex agent.
2. The agent maps the wording to claim IDs and calls a Python checker. In the
   sample release, Free-plan CSV export and Excel export both fail their checks.
   The agent reports the failures in the thread and asks the owner how to proceed.
3. The owner narrows the scope to Pro CSV. The agent reruns the checker and asks
   the owner to approve the exact revision of the evidence and claims.
4. The owner approves that revision in the thread. The checker revalidates the
   inputs before writing the Markdown release note. The agent replies with the
   final wording and receipt path.

Switch supplies the room, the chat bridge, agent addressing and the
conversation that carries the owner’s decisions. The Python process handles
evidence and revision validation. It can be tested in isolation.

## Run it in Switch

You'll need Python 3.10+, Switch Console with a local server or an existing
server, and a signed-in agent provider. The demo uses Codex and local Mattermost.
On Windows, start Docker Desktop and wait for **Engine running** before
setting up a new local Switch server. Switch's native Windows server can
run without Docker, but it skips bundled Mattermost. If you already use a
native server, select a connected team chat when running the template.

1. Follow the [Switch quickstart](https://docs.switchagents.ai/switch-rooms/getting-started).
   Confirm that **Settings → Agent providers** shows Codex as **Signed in**,
   then keep Switch Console open.
2. In **Templates**, select **Import template** and import
   [promisegate.template.yaml](switch/promisegate.template.yaml). Run it with
   the repository root as the working directory and your Mattermost
   connection as the team chat connector. This creates the room and reviewer
   together. Continue at step 4. For manual setup, open **Your Agents** and
   select the **+** card. Name the agent
   `promise-review`, choose **This computer**, set **Directory** to the root of
   this repository, choose Codex, and paste
   [the agent instructions](switch/agent-instructions.md) into **Agent
   instructions**. Use the default owner-scoped addressing. Save the agent.
3. In **Your Rooms**, create a private Mattermost room called `release-desk`
   with yourself and `promise-review`. For an existing room, use **Add to
   room** on the agent’s page. Open the room in Mattermost. See the official
   [room setup guide](https://docs.switchagents.ai/switch-rooms/getting-started/create-a-room).
4. Send the three messages in [DEMO.md](DEMO.md), waiting for the agent’s reply
   between messages. Use the actual agent handle displayed in Mattermost.
   Approve any appropriate local file or command prompts after reviewing them.
5. Open the Markdown file in `receipts/` and compare it with the agent’s reply.
   The release note should contain exactly one Pro CSV claim and the approved
   revision.

## Run the checker locally

```sh
python -m unittest -v
python gate.py review
python gate.py review --claims case/revised-claims.json
```

The first review returns `BLOCKED`. The second returns `READY FOR HUMAN`.
To exercise receipt generation from the terminal, pass the second review’s
full revision to the publish command.

```sh
python gate.py publish --claims case/revised-claims.json --revision <full-revision>
```

## Scope and evidence

The repository ships a synthetic release and an explicit catalog of approved
wording and required check IDs. Teams can replace the catalog and check
results with their own evidence. Claim mapping is the agent’s job, so the
owner reviews the exact wording before approving. Missing checks fail closed.
Changing a check, the evidence catalog, or the claim list changes the revision.

The prototype runs one review at a time in an owner-scoped room. Switch
addressing and the agent instructions govern who can approve in chat. The
local CLI checks revision integrity and treats the caller as trusted. Its only
publish action is creating a local Markdown receipt. Real customer
announcements and deployments are outside this prototype.
