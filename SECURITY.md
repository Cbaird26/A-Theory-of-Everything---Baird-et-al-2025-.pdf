# Security Policy

## Supported Versions

Security updates are provided for the latest version of the repository. Older versions may not receive security patches.

## Reporting a Vulnerability

If you discover a security vulnerability in this repository, please report it responsibly:

**DO NOT** open a public issue or discussion.

**DO:**
1. Email security concerns to the repository maintainer
2. Include a detailed description of the vulnerability
3. Provide steps to reproduce (if applicable)
4. Allow reasonable time for the issue to be addressed before public disclosure

## Security Best Practices

### For Contributors

**Never commit:**
- API keys, tokens, passwords, or secrets
- SSH keys or private keys
- Personal health/genetic data
- Client information or confidential materials
- Restricted order materials (see `VAULT_POLICY.md`)

**Before committing:**
- Review staged files: `git diff --cached`
- Run pre-commit hooks: `git commit` (automatically runs)
- Verify no secrets: Check for `API_KEY`, `SECRET`, `TOKEN` patterns

### For Repository Maintainers

**Enable GitHub Security Features:**
- Secret scanning (Settings → Security → Secret scanning)
- Push protection (Settings → Security → Push protection)
- Dependabot alerts (Settings → Security → Dependabot)

**Regular Audits:**
- Review `SECURITY_AUDIT_REPORT.md` periodically
- Run secret scanning tools (e.g., `gitleaks`)
- Check GitHub secret scanning alerts

## Security Measures

This repository includes:

1. **Pre-commit Hook** (`scripts/hooks/pre-commit`)
   - Blocks restricted keywords and paths
   - Detects potential secrets
   - Prevents large file commits
   - Validates file types

2. **Gitignore** (`.gitignore`)
   - Excludes private data directories
   - Ignores environment files
   - Blocks sensitive file types

3. **Vault Policy** (`VAULT_POLICY.md`)
   - Defines restricted content
   - Documents allowed content
   - Provides security guidelines

## If You Accidentally Commit Secrets

1. **Immediately revoke/rotate** exposed credentials
2. **Remove from git history** using `git filter-repo`
3. **Force-push** cleaned history (coordinate with collaborators)
4. **Review** all commits since the leak

**See:** `SECURITY_AUDIT_REPORT.md` for detailed remediation steps.

---

**Last Updated:** 2026-01-20  
**Related:** `VAULT_POLICY.md`, `PRIVATE_VAULT_SAFETY_RULES.md`, `SECURITY_AUDIT_REPORT.md`
