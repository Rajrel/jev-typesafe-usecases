# Reference

These notebooks follow two local guides and the current TypeSafe and LangChain docs.

## Official docs

- Jev introduction: https://docs.typesafe.ai
- Primitives: https://docs.typesafe.ai/primitives
- Patterns: https://docs.typesafe.ai/patterns
- Known rough edges for `jev-1.13`: https://docs.typesafe.ai/model-jaggedness/jev-1.13
- LangChain integration: https://docs.langchain.com/oss/python/integrations/providers/typesafe

## Call shape

Current `langchain-typesafe` wants both values on each call:

```python
response = classifier.invoke({"state": state, "questions": questions})
```

`TypeSafeClassifier` is constructed with the model id (`JEV_MODEL`, default `jev-latest`). Questions are not stored on the classifier. The cookbook at the repo root still shows the older constructor style. Use the notebooks, not that snippet, when you copy code.

`Choice` and `Score` include `confidence`. `Noul` does not. The probability is the whole answer. A score's `legend` is a dict of level index to the rubric text you passed in.

## Notebook map

| Notebook | Cookbook part | Use cases |
| --- | --- | --- |
| `00_primitives.ipynb` | Guide sections 1–3 | hello world |
| `01_agent_control_loop.ipynb` | A. Agent control loop | 1–9 |
| `02_safety_guardrails.ipynb` | B. Safety, guardrails, verification | 10–13 |
| `03_retrieval_and_rag.ipynb` | C. Retrieval and RAG | 14–17 |
| `04_extraction.ipynb` | D. Extraction and structuring | 18–22 |
| `05_classification_and_routing.ipynb` | E. Classification and routing | 23–27 |
| `06_engineering_workflows.ipynb` | F. Engineering and operations | 28–30 |
| `07_governance.ipynb` | G. Enterprise governance | 31–36 |
| `08_multi_agent.ipynb` | H. Multi-agent internals | 37–42 |
| `09_devops_and_data.ipynb` | I. DevOps, SRE, and data | 43–48 |
| `10_security_and_compliance.ipynb` | J. Security and compliance | 49–53 |
| `11_product_and_content.ipynb` | K. Product, UX, and content | 54–58 |
| `12_customer_operations.ipynb` | L. Customer and business operations | 59–63 |
| `13_simulation.ipynb` | M. Simulation and real-time | 64–65 |
| `14_structured_questions.ipynb` | N. JSON in instructions and criteria | 66–72 |

## What we left out on purpose

Jev is a poor fit for counting, arithmetic, and date math. The date notebook extracts month, day, and year as Choices, then Python compares them. Refund windows use `days_since_purchase`, which the sample database already stores as a number.

Jev does not write text. Generation stays with OpenAI.

These notebooks do not score people on protected traits, credit, hiring, or housing.
