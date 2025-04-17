# The Model Context Protocol

The Model Context Protocol (MCP) is a protocol designed to facilitate the interaction between AI agents and their environment. It provides a structured way for agents to communicate, share information, and collaborate on tasks. The MCP is particularly useful in scenarios where multiple agents need to work together to achieve a common goal.

The use of MCP servers may involve risks, article "[MCP Servers are not safe](https://medium.com/data-science-in-your-pocket/mcp-servers-are-not-safe-bfbc2bb7aef8)" illustrates what they are and how to mitigate them.

## Existing MCP Servers

- [ModelContextProtocol](https://github.com/modelcontextprotocolservers)
- [Playwright MCP](https://github.com/microsoft/playwright-mcp)
- [Selenium MCP](https://github.com/angiejones/mcp-selenium)

## Test
This section aims to test the MCP protocol and its implementation in various environments. 
It includes a set of tests that can be run to ensure that the protocol is functioning as expected.

### Servers

#### UI Automation

There are two approaches to the problem: in one case, we proceed with a screenshot of the surface and try to identify the elements by analyzing the image; in the other case, we search the HTML code using XPath or something similar.
  

- [Playwright MCP](servers/playwright-mcp.md): A server that allows AI agents to interact with the Playwright framework for web automation tasks.
- [Selenium MCP](servers/selenium-mcp.md): A server that allows AI agents to interact with the Selenium framework for web automation tasks.

### Environment Automation

### Database Automation

