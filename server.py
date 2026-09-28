"""Minimal read-only MCP tool for the DIALX experiment lab."""

import re

from mcp.server.fastmcp import FastMCP


mcp = FastMCP(
    "Experiment Delay Lab",
    host="0.0.0.0",
    port=8000,
    stateless_http=True,
    json_response=True,
)


@mcp.tool()
def calculate_experiment_delay(actual_start: str) -> str:
    """Calculate whole minutes late versus the experiment's 09:15 daily start.

    actual_start: Local clock time in 24-hour HH:MM format, e.g. 10:07.
    This tool performs only a calculation; it does not check files or jobs.
    """
    if not re.fullmatch(r"(?:[01][0-9]|2[0-3]):[0-5][0-9]", actual_start):
        raise ValueError("actual_start must be in 24-hour HH:MM format")

    hour, minute = map(int, actual_start.split(":"))
    scheduled_minutes = 9 * 60 + 15
    actual_minutes = hour * 60 + minute
    delay = max(0, actual_minutes - scheduled_minutes)
    return (
        f"שעת תחילת סבב מתוכננת: 09:15; שעת התחלה שנמסרה: {actual_start}; "
        f"איחור: {delay} דקות. החישוב מבוסס על השעה שנמסרה, ללא בדיקת מערכת."
    )


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
