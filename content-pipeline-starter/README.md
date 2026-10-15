# Content pipeline starter

The smallest content pipeline that still has the three things that matter: a source you trust, a task with edges, and a person who says yes.

This is the entry-level companion to the talk **"Fear, Loathing, and AI Content Pipelines"** (All Day AI, October 22, 2026). If you've never built one of these, start here. The full version with five gates, blind reviewers, and a metrics script is in the [governed-content-pipeline](../governed-content-pipeline) repo. You'll graduate to it when this one starts feeling small.

## What you get

```
sources/about-kestrel.md     One file. The only place the AI is allowed to get facts.
checklist.md                 One gate. Five yes/no questions a person answers before anything ships.
log.md                       One table. Every piece, who approved it, and when.
project-instructions.md      Paste this into a Claude Project. That's the whole agent.
templates/                   A request form and a draft layout.
example/                     One piece, start to finish, so you can see what "done" looks like.
docs/                        Why each piece exists, the mistakes everyone makes, and how to graduate.
```

No scripts. No JSON. No subagents. Everything is a markdown file you can read in a browser.

## The three steps

```
1. Ask       You fill in templates/request.md. Half a page.
2. Draft     The AI writes from sources/ only, and tags every fact so you can see where it came from.
3. Check     You answer five yes/no questions in checklist.md. All yes: it ships, you log it. Any no: back to step 2.
```

That's it. No step is optional, and no step is long.

## Set it up in 10 minutes

1. In Claude, create a new Project. Call it whatever you like.
2. Open `project-instructions.md`, copy everything below the line, paste it into the Project's instructions.
3. Upload `sources/about-kestrel.md` and `checklist.md` to the Project's knowledge.
4. Start a chat and type: **"New piece"**. The agent will ask you for the request form.

Then read [`START-HERE.md`](START-HERE.md), which walks you through your first piece with the example.

## Why it's built this way

The fear people have about AI content ("can I trust this?") comes from two things: the AI pulling facts from places nobody vouches for, and the AI being asked to do things nobody can check. The loathing ("why does this take so long?") comes from two other things: decisions nobody can see, and work nobody measures.

This starter kit answers all four with the smallest possible move:

| Fear or loathing | The smallest fix | Where it lives |
|---|---|---|
| Ungoverned sources | One source file, one named owner | `sources/about-kestrel.md` |
| Unbounded tasks | A request form that says what "correct" means | `templates/request.md` |
| Invisible decisions | One checklist, one person, yes or no | `checklist.md` |
| Unmeasured work | A table with dates in it | `log.md` |

The model is the easy part. You could swap it for a different one tomorrow and nothing in this folder would change.

## When to graduate

When any of these happen, you've outgrown the starter kit:

- You have more than three source files and nobody's sure which one wins.
- The person doing the checklist is also the person who asked for the piece.
- You want to know how long pieces take, not just whether they shipped.
- Someone said "just change one word" after the checklist was done.

[`docs/graduating.md`](docs/graduating.md) maps each piece here to its grown-up version.

## License

MIT. Rename the company and go.
