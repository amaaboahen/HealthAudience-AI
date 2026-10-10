# HealthAudience AI
## Project Background, Purpose & Design Rationale

HealthAudience AI is an interactive healthcare audience analytics portfolio project. It demonstrates how audience characteristics and campaign engagement can be turned into clear segments, visual insights, and practical outreach experiments.

**[Explore the live demo](https://healthaudience-ai.streamlit.app/)** · **[Read the setup and methodology guide](README.md)**

The application uses synthetic data and transparent descriptive rules. Its purpose is to support an explainable approach to campaign planning, with no medical predictions or LLM-generated insights.

## Why I Chose This Project

I wanted to explore the intersection of healthcare, business analytics, and AI-assisted development. Healthcare outreach offered a concrete problem: how can an organization understand different audiences and decide which communication approaches to test?

My goal was to build something that connects analysis to a decision. A user should be able to select an audience, understand its engagement patterns, and leave with a specific experiment to consider. That shaped the project's filters, explainable segments, and recommendations.

I also wanted to take a project from an idea to a working application using OpenAI Codex as an agentic coding tool. The project gave me a way to explore AI-assisted development while keeping the application's logic visible and understandable.

## The Problem It Addresses

An outreach team may have information about consumers' regions, age groups, service interests, preferred channels, and previous campaign responses. A spreadsheet can hold those records, but it may take additional work to answer questions such as:

- Which audience groups are engaged, and which may benefit from a different approach?
- What communication channels and service interests are most common in a selected audience?
- What would be a reasonable next campaign experiment?
- How can someone share the analysis and the assumptions behind it?

Sending the same message through the same channel to everyone can overlook meaningful differences. HealthAudience AI demonstrates a workflow for exploring those differences and turning them into testable campaign ideas. It does not connect to CRM systems, combine external data sources, or measure the effectiveness of an actual campaign.

## How the Application Works

### 1. Start with a reproducible synthetic audience

The bundled sample contains 500 fictional consumer records generated with seed 42. Each record includes an identifier, age group, region, stated service interest, preferred communication channel, engagement score, and campaign response.

The engagement score is an arbitrary indicator from 0 to 100. The generator deliberately makes responses more likely at higher scores so the demonstration has useful patterns to explore. Those patterns are designed into the sample and are not findings about a real population.

Users can also upload synthetic CSV files that follow the documented schema. The application validates required fields, accepted categories, unique identifiers, score ranges, and file and row limits. Upload confirmation is a user assertion; it does not automatically detect personal or health information.

### 2. Explore a selected audience

Sidebar filters cover region, age group, service interest, preferred channel, audience segment, and engagement range. The same selection drives the metrics, six interactive charts, recommendations, and exports.

Four metrics summarize the selected audience:

- **Audience size:** Number of selected consumers.
- **Mean engagement:** Arithmetic mean of their engagement scores.
- **Response rate:** Percentage whose response is Clicked or Registered.
- **Registration rate:** Percentage whose response is Registered.

Both rates use all selected consumers as the denominator. Registration represents a campaign action, not a medical outcome.

### 3. Apply explainable behavioral segments

Every record belongs to exactly one segment:

- **Active responders:** Engagement score of at least 70 and a campaign response of Clicked or Registered.
- **Engaged explorers:** Engagement score of at least 40, excluding Active responders.
- **Re-engagement audience:** Engagement score below 40, regardless of campaign response.

These rules make the classification easy to inspect. For example, a consumer with a score of 75 and No response belongs to Engaged explorers, while a consumer with a score of 35 and Registered belongs to the Re-engagement audience. The labels describe the chosen rules rather than diagnosing a person's needs or predicting future behavior.

### 4. Suggest outreach experiments

The application identifies the most common preferred channel and stated service interest in the filtered audience, then suggests relevant campaign experiments. It also provides a fixed suggested action for each segment present:

- Test a registration invitation for Active responders, with a holdout group for comparison.
- Test useful service information with an easy next step for Engaged explorers.
- Test a low-frequency preference check for the Re-engagement audience, honoring opt-outs.

The recommendations include counts and proportions to show their basis. Audiences with fewer than 30 records receive a caution about drawing broad conclusions. These are deterministic suggestions for experiments, not predictions of campaign lift or guaranteed outcomes.

### 5. Export the analysis

Users can download the filtered records as a CSV and an audience summary as a plain-text report. The report includes the data source, filter context, metrics, segment rules, suggested experiments, and limitations, making the analysis easier to discuss or revisit.

## What Makes My Approach Distinctive

The project's distinction is the combination of features and design choices, rather than a claim that the underlying techniques are new.

**A direct path from data to a proposed action.** The dashboard connects audience patterns to specific outreach experiments, giving users a starting point for campaign planning.

**Visible reasoning.** Segment thresholds, metric denominators, and recommendation rules are explicit. A user can explain how an output was produced without needing to interpret a complex model.

**Consistency across the workflow.** Charts, recommendations, records, and reports reflect the same filtered audience. Exports retain the context needed to understand the results.

**A bounded healthcare demonstration.** Synthetic records make it possible to explore healthcare outreach concepts without requiring real patient data. The interface and reports keep the scope and limitations visible.

**An accessible business focus.** The application brings exploration, explanation, and sharing into one Streamlit interface, with no credentials, database, or paid services required to run the prototype.

## Technical Approach and the Role of Codex

The application is built with Python, Streamlit, Pandas, and Plotly:

- [`app.py`](app.py) provides the interface, filters, charts, and downloads.
- [`audience.py`](audience.py) contains data generation, validation, segmentation, metrics, recommendations, and report generation.
- [`data/sample_audience.csv`](data/sample_audience.csv) provides the reproducible demonstration dataset.
- [`tests/`](tests/) contains automated checks for data logic and Streamlit behavior.

I used OpenAI Codex as the agentic coding tool during development. That development workflow is separate from the application's runtime behavior: the dashboard uses deterministic Python rules and does not call an LLM or use a trained predictive model.

The repository includes tests for reproducibility, validation errors, segment boundaries, metric calculations, empty audiences, exports, dashboard filtering, and upload handling. The upload tests inject a file object; they do not exercise the native browser file picker. The [README](README.md#tests-and-reproducibility) explains how to run the suite.

## Lessons from the Project

This project reinforced the importance of defining the business question before selecting the technology. Choosing understandable metrics and segment rules helped keep each feature tied to a clear purpose.

It also highlighted how much context matters. A percentage needs a denominator, a segment needs a definition, and a recommendation needs an explanation of what supports it. Those details make a dashboard easier to evaluate and discuss.

AI-assisted development made this a useful opportunity to practice turning requirements into an application. Human direction, review, and validation remain part of that process, especially when deciding what the results can reasonably claim.

## Limitations and Future Directions

HealthAudience AI is a portfolio prototype for descriptive campaign planning. The fictional sample does not represent a real population, and its associations do not establish causation. It does not infer medical conditions, predict health outcomes, send outreach, or demonstrate improvements in real campaign performance.

Possible next steps include audience comparison features, measurement of actual campaign experiments, and a natural-language interface for asking questions about the data. Predictive modeling would require suitable data and careful validation; it is not part of the current application.

Any use with real healthcare information would require additional privacy, consent, security, accessibility, and governance work. The synthetic-upload checkbox alone is not a privacy safeguard or evidence of regulatory compliance.

## Project Links

- [Live application](https://healthaudience-ai.streamlit.app/)
- [GitHub repository](https://github.com/amaaboahen/HealthAudience-AI)
- [README: setup, CSV schema, methodology, and tests](README.md)
