# jev-typesafe-usecases

Jev is a model that does not write sentences. You give it some context (the **state**) and one or more short questions. It gives back a typed answer your code can branch on: a label, a score, or a yes/no probability.

A normal chatbot is the wrong tool for those small judgments. It is slow, and the answer arrives as a paragraph you still have to parse. Jev is built for the judgment. When a reply, a summary, or an explanation is needed, these notebooks call OpenAI. Your Python then decides what happens next.

TypeSafe, the company behind Jev, calls this a System One model: fast judgment, not a conversation.

## The three questions

| Question | You ask | You get | Use it when |
| --- | --- | --- | --- |
| **Choice** | Which of these options? | a label, a probability for each option, and a confidence | the answer picks a code path |
| **Score** | Where is this on a scale? | a number along your levels, plus confidence | the answer is a spectrum |
| **Noul** | Is this statement true? | one probability from 0 to 1 | the answer is a yes or no |

All questions in one call see the same state and run together. Asking five questions costs little more than asking one.

A Noul of `0.5` means the model is split between yes and no. It does not mean "medium." Use a Score for a spectrum.

Confidence (on Choice and Score) tells you whether to act automatically. A low-stakes lookup can accept a lower bar than a refund or a delete.

## How the pieces fit

- **Jev decides.** Routing, risk, "is this refund eligible," "which tool."
- **OpenAI writes.** A shopper reply, a field extraction, a sentence of copy. Only the cells marked **needs OpenAI** do this.
- **Your code routes.** Thresholds live in the notebook, next to the questions, so you can see them.

## The sample shop

Every notebook uses the same fake company, **Northwind Outfitters**.

- `data/shop.db` is a SQLite file: customers, orders, order lines, products, support tickets, emails, and incidents. Maya Chen was charged twice on order `A-104`. Luis Ortega's tent (`A-118`) is late. There is an open checkout incident, `INC-14`.
- `data/fixtures/` holds pull requests, alerts, logs, invoices, a short contract, feedback, and leads.
- `data/corpus/` is a handful of short policy pages, including one note with a hidden instruction so the safety notebook has something to catch.

Rebuild the database any time:

```bash
uv run python data/build_sample_db.py
```

Nothing here calls a live store, GitHub, or MCP server. Tool calls are small Python functions over the SQLite file.

## Setup

You need Python 3.10+ and [uv](https://docs.astral.sh/uv/).

```bash
uv sync --all-groups
uv run python -m ipykernel install --sys-prefix --name jev-typesafe-usecases --display-name "jev-typesafe-usecases"
copy .env.example .env
```

Add two keys to `.env`:

```
TYPESAFE_API_KEY=your_key_here
OPENAI_API_KEY=your_key_here
```

Open any notebook with the `jev-typesafe-usecases` kernel. If a key is missing, that cell prints `skipped` and the rest of the notebook still runs.

## Notebooks

| Notebook | What it decides | Needs OpenAI |
| --- | --- | --- |
| [00_primitives](notebooks/00_primitives.ipynb) | One ticket, three questions: urgent, team, severity | no |
| [01_agent_control_loop](notebooks/01_agent_control_loop.ipynb) | Which model, which tool, whether the call is safe, whether the task is done | no |
| [02_safety_guardrails](notebooks/02_safety_guardrails.ipynb) | Block, review, or pass a message; check a citation | yes, for one drafted reply |
| [03_retrieval_and_rag](notebooks/03_retrieval_and_rag.ipynb) | Which policy page answers the question, and whether to retrieve at all | no |
| [04_extraction](notebooks/04_extraction.ipynb) | Check extracted fields, pick a span, read a date as choices | yes, for one extraction |
| [05_classification_and_routing](notebooks/05_classification_and_routing.ipynb) | Intent, priority, category, inbox action | no |
| [06_engineering_workflows](notebooks/06_engineering_workflows.ipynb) | PR risk, incident severity, review features | no |
| [07_governance](notebooks/07_governance.ipynb) | Where data may go, how sensitive a document is, which scopes a turn needs | no |
| [08_multi_agent](notebooks/08_multi_agent.ipynb) | Loops, handoffs, plan steps, disagreeing answers | no |
| [09_devops_and_data](notebooks/09_devops_and_data.ipynb) | CI cause, log severity, migrations, data quality | no |
| [10_security_and_compliance](notebooks/10_security_and_compliance.ipynb) | Outbound data, access requests, phishing signals | no |
| [11_product_and_content](notebooks/11_product_and_content.ipynb) | Themes, brand voice, translations, alt text | yes, for one optional sentence |
| [12_customer_operations](notebooks/12_customer_operations.ipynb) | Refunds, disputes, contract clauses, leads | no |
| [13_simulation](notebooks/13_simulation.ipynb) | A legal move, or a device command from a closed list | no |
| [14_structured_questions](notebooks/14_structured_questions.ipynb) | The same judgments with JSON inside the question | no |

Start with `00_primitives`. Each later notebook is one part of the use-case cookbook, with a short section per use case.
