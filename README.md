# ETF Flow MCP

An MCP server that delivers crypto ETF flow data to power AI agents' decision-making.

<a href="https://glama.ai/mcp/servers/@kukapay/etf-flow-mcp">
  <img width="380" height="200" src="https://glama.ai/mcp/servers/@kukapay/etf-flow-mcp/badge" alt="etf-flow-mcp MCP server" />
</a>

[![Discord](https://img.shields.io/discord/1353556181251133481?cacheSeconds=3600)](https://discord.gg/aRnuu2eJ)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)

## Features

- **Unified Tool**: The `get_etf_flow` tool dynamically fetches historical ETF flow data for BTC or ETH.
- **Markdown Table Output**: Leverages pivot tables to present data with ETF tickers as columns, dates as rows, and a total column for summed flows.
- **Prompt Guidance**: Includes a prompt (`etf_flow_prompt`) to streamline LLM interactions for user-friendly queries.

## Prerequisites

- **Python**: Version 3.10 or higher.
- **uv**: A fast Python package and project manager ([install instructions](https://github.com/astral-sh/uv)).
- **CoinGlass API Key**: Obtain a key from [CoinGlass](https://www.coinglass.com/).
- **Claude Desktop**: Optional, for interactive querying.
- **Git**: For cloning the repository.

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/kukapay/etf-flow-mcp.git
   cd etf-flow-mcp
   ```

2. **Set Up with uv**:
   Install dependencies using `uv`:
   ```bash
   uv sync
   ```

## Usage

### Integrating with Claude Desktop

1. **Configure Claude Desktop**:
   Add the server to `claude_desktop_config.json` (located in `~/Library/Application Support/Claude` on macOS or `%APPDATA%\Claude` on Windows):
   ```json
   {
     "mcpServers": {
       "etf-flow-mcp": {
         "command": "uv",
         "args": ["--directory", "/absolute/path/to/etf-flow-mcp", "run", "etf-flow-mcp"],
         "env": { "COINGLASS_API_KEY": "your_coinglass_api_key_here" }
       }
     }
   }
   ```
   Replace `/absolute/path/to/etf-flow-mcp/cli.py` with the full path to `cli.py`.

2. **Restart Claude Desktop**:
   Verify the hammer icon appears in the Claude Desktop UI to confirm the server is loaded.

3. **Query Examples**:
   - "Show me the latest BTC ETF flow data in a table"
   - "Get the ETH ETF flow history"

### Example Output

- **BTC ETF Flow**:
  ```markdown
  | Date       | GBTC      | IBIT      | FBTC      | ARKB      | BITB      | BTCO     | HODL     | BRRR     | EZBC     | BTCW     | Total     |
  |------------|-----------|-----------|-----------|-----------|-----------|----------|----------|----------|----------|----------|-----------|
  | 2025-04-24 | 0         | 327300000 | 0         | 97700000  | 10200000  | 7750000  | 0        | 0        | 0        | 0        | 442200000 |
  | 2025-04-23 | 0         | 643200000 | 124400000 | 129500000 | -15200000 | 0        | 5300000  | 0        | 0        | 0        | 917700000 |
  | 2025-04-22 | 65100000  | 193500000 | 253800000 | 267100000 | 76700000  | 18300000 | 6500000  | 0        | 10600000 | 0        | 912700000 |
  | 2025-04-21 | 36600000  | 41600000  | 88100000  | 116100000 | 45100000  | 0        | 11700000 | 0        | 10100000 | 0        | 381300000 |
  | 2025-04-18 | 0         | 0         | 0         | 0         | 0         | 0        | 0        | 0        | 0        | 0        | 0         |
  ```

- **ETH ETF Flow**:
  ```markdown
  | Date       | ETHE      | GETH     | ETHA      | ETHW     | FETH      | ETHV     | EZET     | CETH     | QETH     | Total     |
  |------------|-----------|----------|-----------|----------|-----------|----------|----------|----------|----------|-----------|
  | 2025-04-24 | -6600000  | 18300000 | 40000000  | 5100000  | 0         | 2600000  | 0        | 4100000  | 0        | 63550000  |
  | 2025-04-23 | 0         | 6400000  | -30300000 | 0        | 0         | 0        | 0        | 0        | 0        | -23900000  |
  | 2025-04-22 | 0         | 0        | 0         | 6100000  | 32700000  | 0        | 0        | 0        | 0        | 38800000  |
  | 2025-04-21 | -25400000 | 0        | 0         | 0        | 0         | 0        | 0        | 0        | 0        | -25400000  |
  | 2025-04-18 | 0         | 0        | 0         | 0        | 0         | 0        | 0        | 0        | 0        | 0         |
  | 2025-04-17 | 0         | 0        | 0         | 0        | 0         | 0        | 0        | 0        | 0        | 0         |
  ```

## License

This project is licensed under the [MIT License](LICENSE).