# Security Policy

## Supported Versions

We issue security patches and updates for the following versions of **remembrandt**:

| Version | Supported          |
| ------- | ------------------ |
| 0.1.x   | :white_check_mark: |
| < 0.1   | :x:                |

---

## 🔒 Reporting a Vulnerability

We take the security of `remembrandt` seriously. If you discover or suspect a security vulnerability in this project, please report it to us promptly so we can address it.

### Reporting Process

1. **Do NOT report security vulnerabilities in public GitHub issues or public discussions.**
2. Send an email to **security@remembrandt.dev** (or submit a GitHub Private Vulnerability Report via the "Security" tab of the repository if available).
3. Include detailed information in your report:
   * Description of the vulnerability and its potential impact.
   * Steps to reproduce the issue (including sample code, terminal commands, or crafted memory entries).
   * Any suggested remediations or patches, if available.

### Response Timeframe & SLA

* **Acknowledgment**: We aim to acknowledge receipt of your vulnerability report within **48 hours**.
* **Assessment & Status Updates**: We will investigate and provide status updates at least every **5 business days** until resolution.
* **Fix & Release**: Once resolved, a patched version will be released, and advisory credit will be given (unless anonymity is requested).

---

## 🛡️ Security Considerations for `remembrandt` Users & Agents

`remembrandt` manages persistent memory for AI coding agents by storing structured Markdown and JSON entries in the local `.remembrandt/` directory.

When using `remembrandt` in your projects:

1. **Sensitive Data & Secrets**: Never store passwords, API keys, private tokens, or PII in `remembrandt` memory entries (`remembrandt remember`). Memory files are plain text and may be committed to version control.
2. **Version Control Strategy**: Ensure `.remembrandt/` configuration matches your team's privacy model. If memory entries contain internal project notes, confirm repository access control before committing.
3. **Execution Safety**: `remembrandt` is a standard CLI with zero runtime dependencies. It does not execute arbitrary code embedded inside memory entries. However, agents parsing `MEMORY.md` should treat memory content as plain data.

---

## 🎖️ Security Hall of Fame

We gratefully appreciate security researchers and community members who responsibly disclose security issues to us.
