# Pake `¯\_(ツ)_/¯`

Pake simplifies running simple workflows you want to run. It offers a few
features of `make`, but removing most of its power. It runs on a `pakefile` or
`pakefile.yaml` (or just pass the name of the file). You can see a simple
[example in the root folder](pakefile.yaml).

It supports Python 3.6.5+ (for no particular reason aside from being my default,
it should work just fine on any relatively recent Python 3)

## Installation

It should be enough to run

```bash
pip install pake
```

and then 

```bash
pake taskname  # If you have a pakefile or pakefile.yaml file
```

### Tab completion

This is a reminder to myself to implement tab completion (at lest for ZSH, since
I have done that before)

## Why?

I had a series of `Dockerfile` I wanted to build sequentially, and run some
commands. It wasn't a right fit for docker-compose, so I wrote a makefile
([here](https://github.com/rberenguel/spark_hadoop_kudu/blob/master/makefile)).
The result was excellent, BUT if you want to add logging, or any kind of
information you need to start resorting to "makefile hacks" (like passing
variables down the dependency stack, or accessing subpaths of requirements...)
that didn't feel right.

So, I decided to write this.

## What?

You define your tasks in a YAML file with specific syntax, of the form:

```yaml
taskname:
  - run: "what it runs"
  - message: "what it logs"
  - depends:
      - task_it_depends_1
      - task_it_depends_2
  - sleep: integer

otherwise:
  - run:
      - "You can run several commands"
      - "Passing them as an array"
  - message:
      - "Likewise for logging"
      - "Yes."
```

You can also use arguments and multiple arguments,

```yaml
taskname:
  - run: "{something} {folder}"
  - message: "This does {something} on {folder}"

main:
  - depends:
      - taskname folder:/Users/foo/ something:rmdir
```

For now you can't have spaces in arguments. Sorry.

For usage, you would just 

```bash
pake taskname
```

## How?

YAML (following the rules above) is converted into a dictionary of task names
and [Tasks](pake/task.py) by a [Parser](pake/parser.py). Then a simple
depth-first-search [planner](pake/planner.py) finds an execution that satisfies
all dependencies and transitive dependencies (with arguments) of `taskname`.
Finally, the plan is passed to an [executor](pake/executor.py) that offloads it
to the shell (or just logs it).

## FAQ

### Why YAML and not FOOML?

I find YAML pretty readable and writable, as long as you restrict what you can
do. Since there is no nesting here, you can't shoot yourself in the foot with
YAML. If you really can't stand YAML, you have two options

- Use [dhall](https://github.com/dhall-lang/dhall-lang) and convert from dhall to YAML (_recommended_)
- Write a [parser](pake/parser.py) for your favourite markup

### Is this production ready?

Well… `¯\_(ツ)_/¯` I'm pretty sure there is an issue with argument replacement
in a corner case, but I can't put my finger on which. For simple use cases, this
should be safe. Since there is no branching, there is not much that can go wrong
though.

### What's with the name?

For one, it's `python+make=pake`. On the other hand, it's also a form of "pa'
qué", an Spanish slang for "para qué". I.e. _what for?_ `¯\_(ツ)_/¯`

## Future development

I will keep using it, so any bugs I find will be fixed. Likewise, I will keep
improving it, although the current version is "almost enough". Currently on the
"roadmap" I have:

- Generate a graphviz plot of the plan(s). This was one of the motivations to
  write my own thingy, after all
- Better tests: I wrote the ones I have with a combination of TDD and "let's
  test and print". I want less tests of happy paths and more tests of corner
  cases
- Custom exceptions, right now it's just "raise that"
- Automatically convert pakefile.dhall into a YAML pakefile (this was supposed
  to be in this version but I got lazy)
- Have a nicer CLI (probably using [cleo](https://github.com/sdispater/cleo))
- Possibly, running tasks in parallel (this is a hard one given how the planner
  works, so probably won't)
- Conditionals?
- Fixing the bug that is likely there in argument substitution