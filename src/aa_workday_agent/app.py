from __future__ import annotations

import asyncio
import logging
import sys
from pathlib import Path

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from azure.ai.agentserver.agentframework import from_agent_framework

from aa_workday_agent.agent import build_agent


logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s")
LOGGER = logging.getLogger("aa_workday_agent")


async def main() -> None:
    async with build_agent() as agent:
        LOGGER.info("Starting AA Workday Team Agent HTTP server")
        await from_agent_framework(agent).run_async()


if __name__ == "__main__":
    asyncio.run(main())