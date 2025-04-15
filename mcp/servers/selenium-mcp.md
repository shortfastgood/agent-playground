# Selenium MCP

- [Project page](https://github.com/angiejones/mcp-selenium)

## Install Selenium MCP

Prerequisite: Node.js and npm must be installed.

```bash
npm install -g @angiejones/mcp-selenium 
```

## Using Claude Coding (MacOS)

1. Connect to the Playwright MCP server using the command:
```bash
claude mcp add selenium -s project npx -y @angiejones/mcp-selenium
```
2. Start Claude Coding
```bash
claude
```

3. Describe the task you want to automate.
```bash
Navigate to website "https://www.crealogix.com" using the "chrome" browser. 
If a dialog having a button "ACCEPT ALL" appears click on "ONLY FUNCTIONAL COOKIES". 
If EN appears on the menu bar, open the drop-down and select DE and click on it.
```

Note: The Selenium MCP is not as reliable as the Playwright MCP. Doesn't locate "ACCEPT ALL" nor "ONLY FUNCTIONAL COOKIES".