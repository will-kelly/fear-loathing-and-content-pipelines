# Start here

A walkthrough for your first piece. Budget 30 minutes, most of it reading.

## Before you start: read these three files, in this order

1. [`sources/about-kestrel.md`](sources/about-kestrel.md). Two minutes. Notice the "don't" lines. Notice there's a name at the top.
2. [`checklist.md`](checklist.md). Two minutes. Five questions. Notice who's allowed to answer them.
3. [`example/`](example/), files 01 through 04. Ten minutes. One piece going through the whole thing, including a round that failed.

If you only read one, read the example.

## Set up the Project

1. In Claude, make a new Project.
2. Paste `project-instructions.md` (everything below the line) into the instructions.
3. Upload `sources/about-kestrel.md` and `checklist.md` as knowledge.

## Run the example yourself

Open a chat in the Project. Type:

> New piece

The AI asks for the request form. Paste the one from `example/01-request.md`. Or, to see the pipeline push back, paste Dana's original message instead:

> Can we get a LinkedIn post up about the SOC 2 thing? Mention we're certified and pricing. Also the ISO one if we can.

Watch what it does with "certified" and "ISO." It doesn't argue. It points at the source file.

Then give it the real form. You'll get a draft with tags. Read the "Things I couldn't source" section first; that's where the decisions are.

Then it shows you the checklist. Answer honestly. If there's a `[?]` in the draft, question 2 is a no. Say so and watch round 2 come back.

## Now do a real one

Pick something small and true. A LinkedIn post. An internal email. Something where the source file already has what you need.

1. Fill in `templates/request.md`. If you can't write the "Point" line, stop. That's the pipeline telling you the task isn't bounded yet.
2. Say "new piece" and paste the form.
3. Read the draft's `[?]` list before you read the draft.
4. Answer the checklist. Not you if you asked for the piece; someone else.
5. Five yes: strip the tags, ship it, log it.

## The three things people get wrong the first week

**They answer their own checklist.** The requester and the checker have to be different people. Otherwise question 5 ("would you sign it") is always yes, because you already did.

**They fix the draft by hand.** It's faster for one sentence. Then the tags are wrong, and the next person doesn't know which facts were checked. Tell the AI what to change; let it retag.

**They add facts to the draft that aren't in the source.** "It's true, I know it is." Maybe. Put it in the source file first. Then it's true for every piece, not just this one, and someone owns it.

More in [`docs/common-mistakes.md`](docs/common-mistakes.md).

## When this starts feeling small

Good. That's the plan. [`docs/graduating.md`](docs/graduating.md) shows what each piece turns into in the full pipeline.
