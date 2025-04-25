import os
import httpx
from datetime import datetime
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP, Context
from mcp.types import PromptMessage, TextContent
from typing import List, Dict, Any
import pandas as pd

# Load environment variables from .env file
load_dotenv()

# Initialize FastMCP server
mcp = FastMCP("ETF-Flow-MCP", dependencies=["httpx", "python-dotenv", "pandas"])

# CoinGlass API configuration
COINGLASS_API_BASE = "https://open-api-v4.coinglass.com"
COINGLASS_API_KEY = os.getenv("COINGLASS_API_KEY")
if not COINGLASS_API_KEY:
    raise ValueError("COINGLASS_API_KEY not found in environment variables")

# Helper function to make CoinGlass API requests
async def fetch_coinglass_data(endpoint: str) -> Dict:
    """
    Make an HTTP GET request to the CoinGlass API.
    
    Args:
        endpoint (str): API endpoint (e.g., '/api/etf/bitcoin/flow-history')
    
    Returns:
        Dict: JSON response from the API
    """
    headers = {
        "accept": "application/json",
        "CG-API-KEY": COINGLASS_API_KEY
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"{COINGLASS_API_BASE}{endpoint}",
                headers=headers
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            raise Exception(f"API request failed: {str(e)}")

# Helper function to format data into a Markdown table using pandas pivot table
def format_to_markdown_table(data: List[Dict], coin: str) -> str:
    """
    Format ETF flow data into a Markdown table using pandas pivot table.
    
    Args:
        data (List[Dict]): List of ETF flow data entries
        coin (str): Cryptocurrency ('BTC' or 'ETH')
    
    Returns:
        str: Markdown table string
    """
    if not data:
        return f"No {coin} ETF flow data available"

    # Prepare data for pandas
    records = []
    for entry in data:
        timestamp = entry.get("timestamp")
        if not timestamp:
            continue
        date_str = datetime.fromtimestamp(timestamp / 1000).strftime("%Y-%m-%d")
        for etf in entry.get("etf_flows", []):
            ticker = etf.get("etf_ticker")
            flow = etf.get("change_usd")
            if ticker:
                records.append({
                    "Date": date_str,
                    "Ticker": ticker,
                    "Flow": flow
                })

    if not records:
        return f"No {coin} ETF flow data available"

    # Create DataFrame
    df = pd.DataFrame(records)

    # Create pivot table
    pivot = df.pivot_table(
        values="Flow",
        index="Date",
        columns="Ticker",
        aggfunc="sum",
        fill_value=0
    )

    # Sort dates in descending order
    pivot = pivot.sort_index(ascending=False)

    # Calculate total column
    pivot["Total"] = pivot.sum(axis=1)

    # Convert to Markdown table
    markdown = pivot.to_markdown(floatfmt=".0f")
    return markdown

# Tool to fetch ETF flow history for BTC or ETH
@mcp.tool()
async def get_etf_flow(coin: str, ctx: Context = None) -> str:
    """
    Fetch historical ETF flow data for BTC or ETH from CoinGlass API and return as a Markdown table.

    Parameters:
        coin (str): Cryptocurrency to query ('BTC' or 'ETH').

    Returns:
        str: Markdown table with ETF flow data (tickers as columns, dates as rows, with total column).
    """
    coin = coin.upper()
    if coin not in ["BTC", "ETH"]:
        return "Invalid coin specified. Please use 'BTC' or 'ETH'."

    ctx.info(f"Fetching {coin} ETF flow data")
    endpoint = f"/api/etf/{'bitcoin' if coin == 'BTC' else 'ethereum'}/flow-history"

    try:
        data = await fetch_coinglass_data(endpoint)
        if data.get("code") == "0" and data.get("data"):
            return format_to_markdown_table(data["data"], coin)
        else:
            return f"No {coin} ETF flow data available"
    except Exception as e:
        return f"Error fetching {coin} ETF flow: {str(e)}"

# Prompt to guide users in querying ETF flows
@mcp.prompt()
def etf_flow_prompt(coin: str) -> List[PromptMessage]:
    """
    Create a prompt for querying BTC or ETH ETF flow data.

    Args:
        coin (str): Cryptocurrency to query ('BTC' or 'ETH').

    Returns:
        List[PromptMessage]: List of prompt messages to guide LLM interaction.
    """
    coin = coin.upper()
    if coin not in ["BTC", "ETH"]:
        return [
            PromptMessage(
                role="user",
                content=TextContent(
                    type="text",
                    text="Invalid coin specified. Please use 'BTC' or 'ETH'."
                )
            )
        ]
    
    return [
        PromptMessage(
            role="user",
            content=TextContent(
                type="text",
                text=(
                    f"Fetch the historical {coin} ETF flow data. "
                    "Return the results in a Markdown table with tickers as columns, dates as rows in descending order, "
                    "and a total column summing all tickers."
                )
            )
        ),
        PromptMessage(
            role="assistant",
            content=TextContent(
                type="text",
                text=(
                    f"I will use the get_etf_flow tool to fetch the {coin} ETF flow data and format it as a Markdown table. "
                    "Please wait while I retrieve the information."
                )
            )
        )
    ]

# Main execution
def main() -> None:
    mcp.run()