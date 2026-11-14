# FortyGuard Product Evaluation

**Exploring Temperature Intelligence Through Dashboard, REST API, and MCP**

## About the Project

This repository documents my hands-on evaluation of FortyGuard's temperature intelligence products as part of a technical product evaluation.

The project focuses on exploring the platform from both a user and developer perspective, testing its main capabilities, analyzing returned data, and documenting feedback and improvement opportunities.

## Products Explored

- **Temperature Dashboard:** Evaluating usability, navigation, and temperature visualization.
- **Temperature API:** Testing API requests, retrieving GeoJSON data, and performing data analysis using Python.
- **Temperature MCP:** Exploring MCP tools, testing their functionality, and evaluating response quality and performance.

## Objectives

- Understand the capabilities of FortyGuard's products.
- Evaluate the user experience and developer experience.
- Test data retrieval and response structures.
- Compare results between REST API and MCP.
- Identify product strengths and areas for improvement.

## Tools & Technologies

`Python` · `REST API` · `JSON` · `GeoJSON` · `MCP` · `MCP Inspector` · `Requests`

## Repository Structure

```text
FortyGuard_Evaluation/
│
├── api_testing/
│   ├── first_request.py
│   └── data_analysis.py
│
├── notes/
│   ├── dashboard_feedback.md
│   ├── api_feedback.md
│   ├── mcp_feedback.md
│   └── final_report.md
│
├── .gitignore
└── README.md
```

## Evaluation Results

The evaluation covered the three product interfaces and included:

- Dashboard usability exploration.
- REST API heatmap generation and GeoJSON analysis.
- MCP environmental data retrieval.
- MCP heatmap retrieval and comparison with REST API results.
- Monitoring and credit balance operations.

See the [Final Evaluation Report](notes/final_report.md) for the consolidated findings.

## Detailed Feedback

- [Dashboard Feedback](notes/dashboard_feedback.md)
- [API Feedback](notes/api_feedback.md)
- [MCP Feedback](notes/mcp_feedback.md)

## Security

API credentials are stored in local environment variables and are not included in this repository.

