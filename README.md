# AI Hype Audit

A small, local command-line tool that flags selected rhetorical signals in
AI-related text, such as catastrophic language, certainty, urgency, and broad
claims about scale.

The project is inspired by concerns that public discussion of AI can lean on
fear-driven or exaggerated framing. It is designed to help readers notice
wording—not to decide whether a claim is true, false, or well-supported.

## Features

- Analyzes text pasted directly into the command.
- Reads UTF-8 text files or standard input.
- Reports detected phrases, categories, and a heuristic index.
- Supports JSON output for scripting.
- Runs locally and uses only the Python standard library.

## Requirements

- Python 3.11 or newer
- Bash for the setup script

## Setup

```bash
git clone https://github.com/swordenkisk/ai-hype-audit.git
cd ai-hype-audit
chmod +x scripts/setup.sh
./scripts/setup.sh
```

## Usage

Analyze text directly:

```bash
ai-hype-audit --text "The report says this outcome is inevitable."
```

Analyze a file:

```bash
ai-hype-audit --file ./article.txt
```

Read from standard input:

```bash
cat ./article.txt | ai-hype-audit --stdin
```

Print JSON:

```bash
ai-hype-audit --text "The report says this outcome is inevitable." --json
```

Run tests:

```bash
python -m unittest discover -s tests
```

## Interpreting results

The index is a simple heuristic based on matches from the phrase list,
adjusted for text length. A higher score means the analyzer found more of its
listed signals relative to the amount of text.

It is **not** a probability, scientific measurement, factuality score, or
assessment of the author's intent. The phrase list is deliberately visible in
`src/aihype/analyzer.py` so it can be reviewed and changed.

## Limitations

- Phrase matching misses wording that is not on the current list.
- A flagged phrase may be justified in context, quoted, or used critically.
- The tool does not check sources, evidence, or factual claims.
- The score should not be used to rank authors or organizations.

## Configuration and APIs

No API key, `.env` file, or external service is required. Input text is
processed locally by the command-line program.

## License

MIT
