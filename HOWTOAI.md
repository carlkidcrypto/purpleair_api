# How to Use AI with purpleair_api
_A practical guide for contributing to purpleair_api using AI coding assistants_

purpleair_api benefits from thoughtful AI-assisted development, but contributors must maintain high standards for code quality, security, and collaboration. Whether you use GitHub Copilot, Cursor, Claude, or other AI tools, this guide will help you contribute effectively.

---

## Core Principles

- **Human Oversight**: You are accountable for all code you submit. Never commit code you don’t understand or can’t maintain.  
- **Quality Standards**: AI code must meet the same standards as human written code—tests, docs, and patterns included.  
- **Transparency**: Be open about significant AI usage in PRs and explain how you validated it.  

---

## Best Practices

**✅ Recommended Uses**  

- Generating boilerplate code and common patterns  
- Creating comprehensive test suites  
- Writing documentation and comments  
- Refactoring existing code for clarity  
- Generating utility functions and helpers  
- Explaining existing code patterns  

**❌ Avoid AI For**  

- Complex business logic without thorough review  
- Security critical authentication/authorization code (API key handling)  
- Code you don't fully understand  
- Large architectural changes  
- Breaking changes to public API  

**Workflow Tips**  

- Start small and validate often. Run tests and Black formatting incrementally  
- Study existing patterns before generating new code  
- Always ask: "Is this secure? Does it follow project patterns? What edge cases need testing?"

**Security Considerations**  

- Extra review required for API key handling, network code, HTTP requests, user input validation  
- Never expose API keys or secrets in prompts or code  
- Sanitize inputs/outputs and follow purpleair_api's security patterns  
- Be cautious with exception handling that might leak sensitive data

---

## Testing & Review

Before submitting AI-assisted code, confirm that:  
- You understand every line  
- All tests pass locally (happy path + error cases)  
- Black formatting is applied (`python -m black .`)  
- Sphinx documentation is updated if needed  
- Code follows existing patterns  

**Always get human review** for: 

- Security sensitive code (API key handling, authentication)  
- Core architecture changes  
- API endpoint implementations  
- Breaking changes to public interfaces  
- Large refactors or anything you're unsure about

---

## Development Best Practices

- Never commit API keys or secrets (use environment variables or config files not in git)  
- Follow Black code formatting (line length: 100, target: py310-py314)  
- Run tests across Python 3.10-3.14 to ensure compatibility  
- Update Sphinx documentation in `sphinx_docs_build/` when adding features  
- Use `try`/`except` blocks with proper context propagation  
- Avoid bare `except` clauses and don't use `sys.exit()` in library code  

---

## Community & Collaboration

- In PRs, note significant AI use and how you validated results  
- Share prompting tips, patterns, and pitfalls  
- Be responsive to feedback and help improve this guide  

---

## Remember

AI is a powerful assistant, not a replacement for your judgment. Use it to speed up development while keeping your brain engaged, your standards high, and purpleair_api secure.  

Questions? Open an issue on [GitHub](https://github.com/carlkidcrypto/purpleair_api/issues) to discuss AI-assisted development practices.  

---

## Getting Started with AI Tools

### Quick Setup

**Setting up your development environment:**
```bash
# Clone the repository
git clone https://github.com/carlkidcrypto/purpleair_api.git
cd purpleair_api

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# or
.\venv\Scripts\Activate.ps1  # Windows PowerShell

# Install dependencies
pip install --upgrade pip wheel setuptools
pip install black coverage requests_mock
pip install -r sphinx_docs_build/requirements.txt
```

**Using GitHub Copilot:**
- Install the [GitHub Copilot extension](https://marketplace.visualstudio.com/items?itemName=GitHub.copilot) for VS Code
- Enable Copilot for Python files in your settings
- Recommended: Install [Python extension](https://marketplace.visualstudio.com/items?itemName=ms-python.python) and [Pylance](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance) for better code intelligence

**Using Cursor:**
- Download [Cursor](https://cursor.sh/) (VS Code fork with built-in AI)
- Open the purpleair_api repository
- Use Cmd/Ctrl+K for inline AI editing, Cmd/Ctrl+L for chat

**Using Claude or ChatGPT:**
- Copy relevant code sections into the chat interface
- Provide context about the purpleair_api architecture (see below)
- Always test generated code locally before committing

### Python-Specific Configuration

Configure your AI tool to follow project standards:

**VS Code settings.json:**
```json
{
  "python.formatting.provider": "black",
  "python.formatting.blackArgs": ["--line-length", "100"],
  "python.testing.unittestEnabled": true,
  "python.testing.unittestArgs": ["-v", "-s", "./tests", "-p", "test_*.py"],
  "github.copilot.enable": {
    "python": true
  }
}
```

**Cursor Rules (.cursorrules in repo root):**
```
This is a Python 3 project using pip and virtual environments.
- Follow Black formatting (line-length=100, target py310-py314)
- Use try/except blocks with proper exception propagation
- Avoid bare except clauses and sys.exit() in library code
- Run tests with: cd tests && coverage run -m unittest
- Build docs with: cd sphinx_docs_build && make html
- Python version support: 3.10, 3.11, 3.12, 3.13, 3.14
```

---

## Understanding purpleair_api's Architecture

New to the PurpleAir API? Here are key questions to ask your AI tool:

### Essential Concepts

**"Explain the purpleair_api package structure"**
```
Ask: "I'm looking at the purpleair_api repository. Can you explain the purpose of each module in the purpleair_api/ directory and how they relate to each other?"

Key insight: purpleair_api is organized into specialized modules:
- PurpleAirAPI: Main API wrapper class
- PurpleAirReadAPI: Read-only operations (get sensor data, etc.)
- PurpleAirWriteAPI: Write operations (requires write API key)
- PurpleAirLocalAPI: Local sensor communication
- PurpleAirAPIConstants: API endpoints and field definitions
- PurpleAirAPIHelpers: Utility functions
- PurpleAirAPIError: Custom exception classes
```

**"How does the API authentication work?"**
```
Ask: "How does purpleair_api handle API keys? Show me examples from PurpleAirReadAPI.py"

Key insight: The API requires read and/or write keys passed during initialization.
Keys are stored securely and included in request headers for authentication.
```

**"What's the request flow?"**
```
Ask: "Walk me through what happens when a user requests sensor data from PurpleAir."

Key insight: User call → API method → HTTP request with auth → Response parsing → Return data
```

### Navigating the Codebase with AI

**Finding the right file:**
```
# Use grep or file search with AI assistance
Ask: "I want to add support for a new API endpoint. Where should I look?"
AI might suggest: Check PurpleAirReadAPI.py or PurpleAirWriteAPI.py depending on the operation

Then ask: "Explain the structure of the get_sensor_data method in PurpleAirReadAPI.py"
```

**Understanding patterns:**
```
Ask: "Show me the pattern for implementing a new API endpoint method"
Then: "How does error handling work in purpleair_api?"
```

---

## Practical Examples

### Example 1: Understanding How to Add a New API Endpoint

**Scenario:** PurpleAir adds a new API endpoint and you want to add support for it.

**Step 1 - Explore existing methods:**
```bash
# Ask AI: "Show me the structure of an existing API endpoint method"
# Look at PurpleAirReadAPI.py or PurpleAirWriteAPI.py

# Ask AI: "Explain the get_sensor_data method implementation line by line"
```

**Step 2 - Ask AI to draft your new method:**
```
Prompt: "PurpleAir added a new endpoint GET /v1/sensors/:sensor_id/history that returns historical data. Based on the pattern in get_sensor_data, draft the implementation for a get_sensor_history method."
```

**Step 3 - Validate with AI:**
```
Ask: "Review this code for:
1. Proper error handling with try/except
2. API key handling and authentication
3. Input validation and sanitization
4. Test coverage needs
5. Sphinx docstring completeness"
```

**Step 4 - Test locally:**
```bash
# Format with Black
python -m black purpleair_api/

# Run tests
cd tests
coverage run -m unittest
coverage report

# Build docs
cd ../sphinx_docs_build
make html
```

### Example 2: Fixing a Python Exception

**Scenario:** You're getting an unexpected exception during API calls.

**Step 1 - Copy the full traceback:**
```bash
# Run your test and capture the error
python -m unittest tests.test_purpleair_read_api 2>&1 | clip  # Windows
python -m unittest tests.test_purpleair_read_api 2>&1 | pbcopy  # macOS
```

**Step 2 - Ask AI with context:**
```
Prompt: "I'm getting this Python exception in the purpleair_api project:

[paste traceback]

Here's the relevant code:
[paste code section]

Explain what's wrong and how to fix it following Python best practices 
and the project's error handling patterns."
```

**Step 3 - Understand the fix:**
```
Ask: "Explain why this fix works and what I should know about exception 
handling in API wrapper libraries."
```

**Step 4 - Apply and verify:**
```bash
# Apply the fix
# Format code
python -m black purpleair_api/

# Run specific test
python -m unittest tests.test_purpleair_read_api.TestClassName.test_method

# Run all tests
cd tests && coverage run -m unittest
```

### Example 3: Adding a Helper Function

**Scenario:** You need a utility function to parse PurpleAir sensor fields.

**Step 1 - Find existing helpers:**
```bash
# Ask AI: "What helper functions already exist in PurpleAirAPIHelpers.py?"
# Review the file
```

**Step 2 - Study the pattern:**
```
Ask: "Explain how existing helper functions in PurpleAirAPIHelpers.py are structured. 
Show me the docstring format and error handling patterns."
```

**Step 3 - Draft your addition:**
```
Prompt: "I want to add a helper function that validates sensor field names 
against the allowed fields in PurpleAirAPIConstants. Based on existing patterns, show me:
1. The function signature and docstring
2. Input validation
3. Return value format
4. Unit tests needed"
```

**Step 4 - Implement with validation:**
```bash
# Make changes to PurpleAirAPIHelpers.py
# Add tests to tests/test_purpleair_api_helpers.py

# Format code
python -m black purpleair_api/ tests/

# Run tests
cd tests
coverage run -m unittest test_purpleair_api_helpers
coverage report

# Update docs if needed
cd ../sphinx_docs_build
make html
```