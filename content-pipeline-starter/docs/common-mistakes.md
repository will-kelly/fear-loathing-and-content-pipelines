# Common mistakes

In the order people usually make them.

## Week one

**Skipping the request form because "it's a quick one."**
The quick ones are the ones that ship with the wrong price. The form is five minutes. The correction post is a week.

**Writing a topic in the "Point" line.**
"SOC 2 announcement" is a topic. "A security review can start from our report instead of a questionnaire" is a point. If you can't check a draft against it in ten seconds, it's a topic.

**The requester answers the checklist.**
Then question 5 is always yes. Different person. Every time. Even for a LinkedIn post.

**Fixing the draft by hand.**
One word, surely that's fine. Now the tags don't match the text and the log says the AI drafted something it didn't. Tell the AI the change. It takes ten seconds and the tags stay honest.

## Week two

**Adding a fact that isn't in the source "because I know it's true."**
It probably is. Put it in the source file. Now it's true for every piece and someone owns it. The pipeline isn't doubting you; it's making your knowledge reusable.

**Treating a `[?]` as a failure.**
A `[?]` is the AI being honest. The failure would be a model that wrote the same sentence without the tag. Read the `[?]` list first, decide, move on.

**Letting the source file go stale.**
The "last checked" date is there for a reason. If it's older than the last product change, somebody should read the file. Put a reminder on the owner's calendar. Monthly is fine.

**Arguing with the checklist about style.**
"I'd have written that sentence differently" is not a no. The checklist asks whether it's true and bounded. If you want a style gate, add a sixth question with a written condition, and notice how hard that is to write. That's why it isn't there yet.

## Week three

**A second source file appears and nobody said which one wins.**
Dana made `pricing-notes.md` because the main file was "too long." Now there are two prices. Before a second file exists, answer: who owns it, and what happens when it disagrees with the first? If you can't, it's a section in the existing file, not a new file.

**Someone changes the text after the checklist passed.**
"Just tightened the opening." The checked version and the shipped version are now different, and the log says Priya approved something she didn't see. In this kit, the rule is simple: any edit after the checklist means the checklist runs again. In the full pipeline, that rule is called "a change after a gate reopens the gate," and it has its own file.

**Nobody fills in the log.**
Thirty seconds per piece. Without it, in a month you'll be asked how long content takes and you'll say "depends," and the person asking will go buy a tool that doesn't fix it either.

## Any week

**Blaming the model.**
When a piece goes wrong, the cause is almost always one of: the source file was missing something, the Point line was vague, or someone skipped the checklist. Fix that one. A better model would have made the same mistake faster.
