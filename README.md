# JSEE

**JSEE** is a lightweight CLI tool for extracting endpoints, secrets, and filesystem paths from JavaScript files, URLs, or full webpages.

It’s built for security researchers, bug bounty hunters, and anyone who wants to quickly understand what a frontend is leaking under the hood.

It helps you spot things like:

1. hidden API endpoints
2. hardcoded secrets and tokens
3. internal paths and config leaks

**Basically**: quick recon for JS-heavy targets.

# What it does

**JSEE** scans JavaScript sources and extracts:

1. Endpoints (fetch, axios, XHR, frameworks, etc.)
2. Secrets (API keys, tokens, credentials, cloud keys)
3. Paths (local files, imports, configs, internal routes)

It uses regex-based pattern matching, so it’s fast and works offline.

# Usage

Run it with a target:

``` bash
python JSEE.py <target>
```

### Target types

You can pass:

1. A webpage URL
2. A direct JS file URL
3. A local JS file

# Examples:

``` bash
python JSEE.py https://example.com
python JSEE.py https://example.com/app.js
python JSEE.py ./file.js
```

# Pattern system

**JSEE** is fully pattern-driven.

You can extend it by editing:

``` bash
patterns/endpoint.json
patterns/secret.json
patterns/path.json
```

Each file contains regex rules grouped by category.

# Why this exists

Most modern apps hide their logic in JS bundles.

Endpoints, secrets, and internal routes are often still there — just buried.

**JSEE** is a fast way to pull that surface data out during:

1. bug bounty recon
2. manual JS analysis
3. API discovery
4. frontend attack surface mapping
5. Contributing

# Contribution

1. Fork it
2. Add better regex patterns or new extraction types
3. Test on real-world JS files
4. Open a PR

Keep it **simple**. Keep it **useful**.

# Disclaimer

JSEE is for educational and security research purposes only.

Only use it on systems you own or have permission to test.

Unauthorized use can be illegal.