# Routing

Read this when the skill is called with no command and no request, when the writer types `help`, or when the writer asks which command to use.

## The menu

Show these four parts, in this order, and nothing else. The parts and their order are fixed so that `help` has the same shape every time it is run; only the next steps in part 2 follow the workspace.

**1. The purpose line,** as written, with the plugin's name:

> Positionary upgrades your writing for a brand: prep, draft, edit, finalize, eliminate AI slop!

**2. Two or three next steps worth taking,** chosen from what the workspace shows. Lead with them; the list below is the fallback. For each: one line saying why, then the command in a fenced code block that holds the command and nothing else, so the writer can copy it. Put the sentence before the block, never inside it. One command per block.

To tell which applies, use `list_workspaces` and, when a workspace is settled or the sign-in reaches only one, one `read_knowledge` call with `topic: "voice"`; `list_workspace_pages` with `status: "draft"` and `limit: 1`. Reason from what you find; there is no score to obey:

| What you find | Suggest |
|---|---|
| The sign-in reaches no workspace you can check, or the workspace is new to this skill | `/positionary init` |
| The workspace has a voice document | `/positionary write` |
| A draft changed recently | `/positionary write` |

Never suggest a command that is not built: when fewer than two built commands fit, show only those that do. Never run one unasked: a suggestion is a suggestion. These next steps are this reply's suggestion, so nothing is added after part 4.

**3. The commands, by pack.** Show the lines below in groups: the shared commands first, with no pack's name above them, and `help` last among them; then each pack, under its name in bold on a line of its own, in the order of the "Packs:" line in the Commands section of `SKILL.md`. Take each line's pack and kind from its command's row in the Commands table, where a pack of `shared` is in every pack and a utility is shared. Within a group, show its lines in the Commands table's order, which is by kind. Each line stands on a line of its own, with no bullets and nothing added. Each is the command as a person types it, in code:

<!-- help-lines -->
`/positionary init` set up or switch your workspace
`/positionary voice` set how your brand sounds
`/positionary venue [name the venue, such as Reddit or Upwork]`
`/positionary outline [the piece to plan]`
`/positionary write [describe what you want to write]`
`/positionary feedback [what]`
`/positionary scan` find openings worth your time today
`/positionary check` find where your brand contradicts itself
`/positionary foundations` see what your workspace is missing
`/positionary help` show this list
<!-- /help-lines -->

These lines are written here, once, when a command is built. Do not derive a line from the Commands table, and do not show a command that has no line here.

- A command that takes words is shown with its bracket, which says in plain language what to type, and nothing after it.
- A command that takes no words is followed by a few plain words, six at most.
- New lines go in the Commands table's order, after `init` and before the utilities.

Each group ends with one line, as plain text and never in a code block, that starts "Coming:" and names the group's commands and utilities that are not built yet, in the Commands table's order, separated by commas:

> Coming: <command>, <command>, document.

Leave a group's line out when everything in it is built. A pack with no line above still shows its name and its "Coming:" line. Do not describe the unbuilt commands here; the writer who types one is told it is not built and offered the nearest one that works.

**4. One line for the packs the workspace lacks.** A pack is what a workspace is granted, by the id the "Packs:" line gives it. When the Admin says which packs the workspace has, part 3 shows the shared commands and those packs only, and this one line, as plain text, names every other pack by its name, in the "Packs:" line's order, and never their commands:

> Other packs: <pack>, <pack>.

Leave it out when the workspace has every pack. The Admin says which packs the workspace has only when what it returns for the workspace, from `list_workspaces` or a read Setup already made, names pack ids the "Packs:" line declares. When the Admin cannot say which packs the workspace has, part 3 shows every pack and this line is left out. Never guess a workspace's packs from its name, its site or its pages.

Run nothing until the writer picks.

## Which command

| The writer wants to | Command |
|---|---|
| See every command | `help` |
| Choose or change the workspace, or see what it holds | `init` |
| Set up a new site, or give it its real domain | `provision` (not built yet) |
| Define the brand's positioning | `positioning` (not built yet) |
| Define what one reader hears | `messaging` (not built yet) |
| Set how the brand sounds | `voice` |
| Define the brand's terms, topics, FAQs and proof | `language` (not built yet) |
| Plan the site or the pieces to write next | `plan` (not built yet) |
| Choose where to take part or look for work | `venue` |
| Add a page | `new` (not built yet) |
| Connect a form, magnet or sign-in to a page | `attach` (not built yet) |
| Know whether the site can go live | `ready` (not built yet) |
| Take the site live | `go-live` (not built yet) |
| Know how the live site is doing | `health` (not built yet) |
| Bring the site up to the latest release | `update` (not built yet) |
| Move to a higher plan or add another pack | `upgrade` (not built yet) |
| Take a page or an item off the site | `disable` (not built yet) |
| Plan what a piece will say before writing it | `outline` |
| Write a new piece | `write` |
| Know whether a draft's words are working | `feedback` |
| Bring a draft that wanders back to its point | `refocus` (not built yet) |
| Reorder a draft so its argument flows | `restructure` (not built yet) |
| Back up the claims in a draft | `support` (not built yet) |
| Make a draft sound like the brand | `revoice` (not built yet) |
| Make a draft shorter without changing what it says | `tighten` (not built yet) |
| Get a draft ready to hand over | `final-check` (not built yet) |
| Write a piece's title and search description | `title` (not built yet) |
| Bring in a site, brand assets or a described look as a reference | `extract` (not built yet) |
| See options before choosing a look | `explore` (not built yet) |
| Settle the look | `choose` (not built yet) |
| Lay out a page: which sections it has and where each goes | `structure` (not built yet) |
| Set the site's colours, type and spacing | `theme` (not built yet) |
| Swap a placeholder for a real image | `image` (not built yet) |
| Add motion | `motion` (not built yet) |
| Know whether a page breaks a design rule | `inspect` (not built yet) |
| Know whether a page's design is working | `critique` (not built yet) |
| Know what to do today to promote the brand | `today` (not built yet) |
| Decide when and where content goes out | `schedule` (not built yet) |
| Plan a newsletter issue | `newsletter` (not built yet) |
| Find conversations worth joining today | `threads` (not built yet) |
| Find a trend, a job or a request for proposal to answer | `scan` |
| Get an answer to a thread or an opening written | `brief` (not built yet) |
| Record something that was posted or sent | `record` (not built yet) |
| Start a study of a business question by stating where the topic stands today | `assess` (not built yet) |
| Say what changed and what question it raises | `frame` (not built yet) |
| State the answer you expect before testing it | `hypothesize` (not built yet) |
| Test a hypothesis that is already recorded against sources | `research` (not built yet) |
| See the choices and what each gives up | `options` (not built yet) |
| Record a decision that has been made | `decide` (not built yet) |
| Present the answer, from an email to a formal presentation | `present` (not built yet) |
| Carry a decision into the documents it changes | `route` (not built yet) |
| Know whether the workspace is consistent | `check` |
| Know what the workspace is missing | `foundations` |
| Write the brand's documents from pages that already exist | `document` (not built yet) |

When the command is not built yet, say so and offer the nearest built one.

**A request that fits commands in two packs.** When a request in the writer's own words fits rows of two commands in different packs, as the Commands table gives each command's pack, ask one question that tells the two apart, in plain words about the work each would do, such as "Do you want me to check how the page reads, or how it looks?" Ask it as one sentence with one question mark, naming every kind of work the request fits, two or three, in that sentence; do not put each as a question of its own. Name neither the packs nor the commands to ask it, and ask about nothing else in the same reply. Run nothing until the writer answers, then follow the command the answer picks. A request that fits two commands in one pack, or a shared command and one in a pack, is routed as any other: when one row fits better, follow it; when it does not, ask once which is meant.
