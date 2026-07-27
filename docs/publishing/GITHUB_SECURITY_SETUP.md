# GitHub Security Setup Guide

**Purpose:** Step-by-step instructions for enabling GitHub security features to protect your repository.

---

## Prerequisites

- GitHub repository exists: `Cbaird26/MQGT-SCF` (or your repository name)
- Admin access to repository settings
- GitHub account with appropriate permissions

---

## Step 1: Enable Secret Scanning

**What it does:** Automatically scans your repository for exposed secrets and alerts you.

**Steps:**

1. Go to your repository on GitHub
2. Click **Settings** → **Security** → **Code security and analysis**
3. Under **Secret scanning**, click **Enable**
4. (Optional) Enable **Push protection** to block commits containing secrets

**Result:** GitHub will scan your repository and alert you if any secrets are found.

---

## Step 2: Enable Push Protection

**What it does:** Blocks commits that contain secrets before they're pushed.

**Steps:**

1. In repository **Settings** → **Security** → **Code security and analysis**
2. Under **Secret scanning**, enable **Push protection**
3. Choose which secret types to protect (recommended: all)

**Result:** Commits containing secrets will be blocked automatically.

---

## Step 3: Enable Dependabot Alerts

**What it does:** Alerts you to vulnerabilities in your dependencies.

**Steps:**

1. In repository **Settings** → **Security** → **Code security and analysis**
2. Under **Dependabot alerts**, click **Enable**
3. (Optional) Enable **Dependabot security updates** for automatic patches

**Result:** You'll receive alerts when vulnerabilities are found in dependencies.

---

## Step 4: Review Security Alerts

**Where to check:**

1. Repository **Security** tab → **Secret scanning** (for exposed secrets)
2. Repository **Security** tab → **Dependabot** (for dependency vulnerabilities)
3. Email notifications (if enabled)

**What to do:**

- If secrets found: Rotate credentials immediately
- If vulnerabilities found: Review and apply patches
- If false positives: Dismiss alerts with explanation

---

## Step 5: Verify Repository Visibility

**Check current visibility:**

1. Go to repository **Settings** → **General**
2. Scroll to **Danger Zone** → **Change repository visibility**
3. Verify current setting (Public/Private)

**To change visibility:**

1. Click **Change visibility**
2. Select desired visibility (Public/Private)
3. Confirm change

**Note:** Making a repository private removes it from public search results but does not delete existing clones or forks.

---

## Step 6: Set Up Branch Protection (Optional)

**What it does:** Requires pull request reviews before merging to main branch.

**Steps:**

1. Repository **Settings** → **Branches**
2. Click **Add rule** for `main` branch
3. Enable:
   - **Require pull request reviews before merging**
   - **Require status checks to pass before merging**
   - **Include administrators**

**Result:** Prevents direct pushes to main branch, requiring review.

---

## Verification Checklist

After setup, verify:

- [ ] Secret scanning enabled
- [ ] Push protection enabled (optional but recommended)
- [ ] Dependabot alerts enabled
- [ ] Repository visibility verified
- [ ] Security alerts reviewed (check Security tab)
- [ ] Email notifications configured (if desired)

---

## Troubleshooting

**Secret scanning not finding secrets:**
- Secrets may be in git history (scan entire history)
- Use `gitleaks` or similar tool for local scanning
- Check `.gitignore` to ensure secrets aren't committed

**Push protection blocking legitimate commits:**
- Review the detected pattern
- If false positive, adjust patterns or disable for specific secret types
- Use environment variables instead of hardcoded secrets

**Dependabot alerts not appearing:**
- Ensure dependencies are in `requirements.txt`, `pyproject.toml`, or similar
- Check that dependency files are committed to repository
- Verify Dependabot is enabled in repository settings

---

## Related Documentation

- `SECURITY_AUDIT_REPORT.md` - Security audit results
- `VAULT_POLICY.md` - Content security policy
- `SECURITY.md` - Security reporting process
- `scripts/hooks/pre-commit` - Local secret detection

---

**Last Updated:** 2026-01-20
