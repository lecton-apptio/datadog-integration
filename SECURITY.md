# Security Policy

## Supported Versions

We release patches for security vulnerabilities. Currently supported versions:

| Version | Supported          |
| ------- | ------------------ |
| 0.1.x   | :white_check_mark: |

## Reporting a Vulnerability

We take the security of datadog-integration seriously. If you believe you have found a security vulnerability, please report it to us as described below.

**Please do not report security vulnerabilities through public GitHub issues.**

Instead, please report them via email to: lecton@apptio.com

You should receive a response within 48 hours. If for some reason you do not, please follow up via email to ensure we received your original message.

Please include the following information in your report:

- Type of issue (e.g., buffer overflow, SQL injection, cross-site scripting, etc.)
- Full paths of source file(s) related to the manifestation of the issue
- The location of the affected source code (tag/branch/commit or direct URL)
- Any special configuration required to reproduce the issue
- Step-by-step instructions to reproduce the issue
- Proof-of-concept or exploit code (if possible)
- Impact of the issue, including how an attacker might exploit it

This information will help us triage your report more quickly.

## Security Best Practices

When using this library:

1. **Never commit credentials**: Always use environment variables or secure secret management systems
2. **Use `.env` files carefully**: Ensure `.env` files are in `.gitignore` and never committed to version control
3. **Rotate keys regularly**: Regularly rotate your Datadog API and Application keys
4. **Limit key permissions**: Use the principle of least privilege when creating Datadog keys
5. **Monitor key usage**: Regularly audit which keys are being used and by whom
6. **Secure your environment**: Ensure the systems running this library are properly secured

## Disclosure Policy

When we receive a security bug report, we will:

1. Confirm the problem and determine the affected versions
2. Audit code to find any similar problems
3. Prepare fixes for all supported releases
4. Release new security fix versions as soon as possible

## Comments on this Policy

If you have suggestions on how this process could be improved, please submit a pull request or open an issue to discuss.