# Playwright MCP

## Home

[Project page](https://github.com/microsoft/playwright-mcp)

## Install Playwright MCP

Prerequisite: Node.js and npm must be installed.

```bash
npm install -g @playwright/mcp@latest 
```

## Using Claude Coding (MacOS, Ubuntu Linux)

Note: Reliable and fast.

1. Connect to the Playwright MCP server using the command:
```bash
claude mcp add playwright -s project npx @playwright/mcp@latest
```
2. Start Claude Coding
```bash
claude
```

3. Describe the task you want to automate.
```bash
Navigate to website "https://www.crealogix.com" using the browser. 
If a dialog having a button "ACCEPT ALL" appears click on "ONLY FUNCTIONAL COOKIES". 
If EN appears on the menu bar, open the drop-down and select DE and click on it.
```

## Use Visual Studio Code (unreliable)

In 50% of the cases, the copilot agent suggests how to code the task instead to execute it.
Even with different prompt techniques there is no way to keep the Copilot focused on the operation with the Playwright MCP.

Prerequisite: Visual Studio Code 1.99.2+ and GitHub Copilot 1.301.0+ must be installed.

1. Connect to the Playwright MCP server using the command:
```pwsh 
code --add-mcp '{\"name\":\"playwright\",\"command\":\"npx\",\"args\":[\"@playwright/mcp@latest\"]}'
```
2. Start Visual Studio Code

3. Select the Copilot agent mode
   - Click on the Copilot icon in the activity bar on the left side of the window.
   - Select "Copilot Agent" from the dropdown menu.

4. Describe the task you want to automate.
```
Navigate to website "https://www.crealogix.com" using the "safari" browser. 
If a dialog having a button "ACCEPT ALL" appears click on "ONLY FUNCTIONAL COOKIES". 
If EN appears on the menu bar, open the drop-down and select DE and click on it.
```
