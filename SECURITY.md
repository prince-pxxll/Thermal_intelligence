# Security Policy

## Supported Versions

| Version | Supported |
|---------|-----------|
| main / 0.x | ✅ |

This project is pre-1.0; only the `main` branch receives security fixes.

## Reporting a Vulnerability

Please **do not** open a public GitHub issue for security vulnerabilities.

Instead:

1. Email the maintainers (see repository contact) with a description of the issue,
   steps to reproduce, and potential impact.
2. Allow up to 5 business days for an initial response.
3. We'll coordinate a disclosure timeline with you once the issue is confirmed.

## Scope

Relevant concerns include, but are not limited to:

- Credential or API key leakage (e.g. FIRMS API keys, cloud storage credentials)
- Injection vulnerabilities in the `api/` FastAPI service
- Insecure deserialization in pipeline or model-loading code
- Dependency vulnerabilities with a known exploit path

## Out of Scope

- Issues requiring physical access to a maintainer's machine
- Vulnerabilities in third-party services this project merely calls (e.g. NASA FIRMS,
  OpenStreetMap) — please report those upstream

Thank you for helping keep this project and its users safe.
