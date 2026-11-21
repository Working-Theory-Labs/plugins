# Positionary

Words that set a brand apart and draw its best-fit buyers in, written from the brand's own record in its site's Admin, with packs for the brand's site, its look, its promotion and its studies.

## Start here

**Claude Code.** Add the Working Theory catalog as a marketplace and install the plugin:

```
/plugin marketplace add working-theory-labs/plugins
/plugin install positionary@working-theory
```

**Claude apps.** Download the plugin from https://github.com/working-theory-labs/plugins/releases/latest/download/positionary.zip. In Claude, open Customize, then Plugins, choose Add plugin, then Upload plugin, and upload the zip. Uploading a newer version replaces the one you have. Then add your site's Admin as a custom connector, under Connectors.

The plugin's skill also appears under Skills. Do not delete it there; that removes the plugin.

Then type `/positionary help`. It lists every command. On a first visit to a workspace, run `/positionary init`: it confirms the site name and description and shows what the workspace holds. After that you can start with any command; it asks which workspace only when your sign-in reaches more than one.

When Claude first asks to use an Admin tool, choose "Always allow" for the tools that read and "Allow once" for the tools that save. The skill asks before every save, and "Allow once" keeps Claude asking too.

**Optional: one project per client.** To keep a client's conversations together, make a project in Claude and give it one instruction, "use workspace <name>". Put nothing else in it: the workspace holds the brand's record, and a copy in a project goes stale.

## Why

Most copy could be about any company. This skill writes only from what your brand has decided about itself: its positioning, its messaging, its voice, and the terms, questions and proof it has defined. Every piece is written for one reader, makes one point, and gives that reader one next step.

## What it does

Six commands work today:

- **`/positionary init`** picks the workspace and confirms its site details. (`connect`, its name in the first release, still works.)
- **`/positionary voice`** offers one paragraph two ways and records your pick as the brand's voice.
- **`/positionary outline`** offers two or three main points for a piece, waits for your pick, then shows the piece's argument on one board.
- **`/positionary write`** writes one very short web page in that voice and saves it to the workspace as a draft.
- **`/positionary venue`** studies one place to look for work, Upwork first, and saves what to search for there, the test for a good fit and your daily limits.
- **`/positionary scan`** finds today's openings at that venue, ranks them by fit and takes the ones you choose to a proposal. It sends nothing without your yes on that one proposal.

`/positionary help`, or `/positionary` on its own, lists the commands by pack, marks the ones not built yet, and suggests which to run next. It runs nothing until you pick.

**Packs.** The commands come in five packs, and a workspace is granted the packs it has bought: **Site** sets up and runs the brand's site, **Writing** writes its words, **Design** gives the site its look, **Promotion** puts its content in front of the right people each day, and **Study** answers one business question with its proof. The workspace commands, `init`, `help`, `check`, `foundations` and `document`, are in every pack. Today the commands that work are in the Writing pack, with `venue` and `scan` in the Promotion pack; the others arrive as they are built.

You do not need to know a command's name. Say what you want done, and it picks the command that fits. When a request could mean work in two packs, such as "is the home page working?", it asks one question to tell them apart and does nothing until you answer.

The full set, by where you are in the work:

| Kind | Commands |
|---|---|
| Prepare | `init`, `provision`, `positioning`, `messaging`, `voice`, `language`, `plan`, `venue` |
| Build | `new`, `attach` |
| Launch | `ready`, `go-live` |
| Run | `health`, `update`, `upgrade`, `disable` |
| Draft | `outline`, `write` |
| Edit | `feedback`, `refocus`, `restructure`, `support`, `revoice`, `tighten` |
| Finalize | `final-check`, `title` |
| Direction | `extract`, `explore`, `choose` |
| Compose | `structure` |
| Codify | `theme` |
| Enrich | `image`, `motion` |
| Review | `inspect`, `critique` |
| Daily | `today` |
| Calendar | `schedule`, `newsletter` |
| Engage | `threads` |
| Signal | `scan` |
| Respond | `brief`, `record` |
| Question | `assess`, `frame`, `hypothesize` |
| Test | `research` |
| Answer | `options`, `decide`, `present`, `route` |

Four utilities sit outside the kinds, in every pack. `/positionary help` lists the commands. `/positionary check` reports where the brand is inconsistent with itself; today it is an outline and cannot yet say a workspace passed. `/positionary foundations` shows what a workspace should have and what is missing. `/positionary document` will write each pack's documents from the workspace's finished state, such as the brand's positioning, messaging and voice from pages that already exist; it is not built yet.

The Writing pack is built to work on pages, posts, magnets, press releases, pitches, proposals and profiles. A pitch can be written as a deck, a one-page document, a script or an email. A proposal can be written as a document, a deck or in a platform's own fields. A profile is written in a platform's own fields, such as LinkedIn or Upwork. Today `write` handles a short page; the rest arrive as their commands are built.

## What you need

- **A site with an Admin,** and a workspace in it for the brand you are writing for.
- **A sign-in that can edit that workspace's content.**
- **The Admin connected to Claude.** The Admin's owner has the connection address. In Claude Code, add it as an MCP server. In the Claude apps, add it as a custom connector.
- **Access to this plugin.**

## What it will and will not do

- **It saves drafts by default.** It publishes one thing only when you ask for it to go live and your sign-in is allowed to publish. No command does that yet, so today you publish in the Admin.
- **It asks before each save,** and tells you what it is about to save and where.
- **Its Writing pack writes words, not layout.** A page's sections, images and layout belong to the Design pack, which is not built yet; until it is, they are set in the Admin.
- **It keeps nothing about a client on your computer.** The workspace is the record. A file you upload or keep in a local folder is a working copy.
- **It works in one workspace at a time.** If you ask for a write in another workspace, it asks you to confirm the switch.
- **It does not invent.** A claim with nothing behind it in the brand's record is cut or asked about.

## Where it runs

Claude Code, Cowork and claude.ai. The same skill folder serves all three. It needs no program on your computer.

## When something is wrong

| You see | What it means |
|---|---|
| "No Admin is connected" | Claude cannot reach your site's Admin. Add the connection, then run `/positionary` again |
| It asks which workspace you mean | A save was refused because this conversation is set to a different workspace. Say which one you want |
| "That command is not built yet" | The command is planned. It will offer the nearest one that works |
| It asks which of two things you mean | Your request fits work in two packs, such as how a page reads and how it looks. Say which, and it starts |
| It lists documents that are missing | The workspace has no positioning, messaging or voice yet. It can still write, and it will say what it worked without |
| "… is part of the … pack, which this workspace does not have" | That command comes with a pack your workspace does not have yet. An owner of the workspace adds it in the Admin, then the command works |
| "This copy of the positionary plugin is version …" | Your copy of the plugin is older than that command now needs. In Claude Code, run `/plugin marketplace update working-theory`. In the Claude apps, upload the newest file from https://github.com/working-theory-labs/plugins/releases/latest/download/positionary.zip |
| It says a read failed | It could not load something from the Admin. It carries on with what it has and never fills the gap from memory |

## Subscription and support

This plugin is not open source. Use it only with a subscription or access granted by SalesSmyth. For help, ask whoever gave you access.
