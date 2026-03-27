from __future__ import annotations

from contextlib import asynccontextmanager

from agent_framework.azure import AzureAIClient
from azure.identity.aio import DefaultAzureCredential
from dotenv import load_dotenv

from aa_workday_agent.config import Settings
from aa_workday_agent.repositories import DocumentRepository, IntegrationRepository
from aa_workday_agent.tools import ToolContext, configure_tools, create_toolset


def _instructions() -> str:
    return (
        "You are the AA Workday Team Agent for the American Airlines HRIS and Workday support team. "
        "Use the available tools to answer questions about SharePoint documentation and Workday integrations. "
        "Always prefer grounded answers with citations. When a question is about process or runbooks, search the SharePoint documents. "
        "When a question is about systems, ownership, schedules, protocols, or inventory, query the integration catalog. "
        "If you use both tools, reconcile conflicts explicitly. If the sources are incomplete, say so and offer to record a knowledge gap. "
        "Do not invent integrations, owners, or procedures."
    )


@asynccontextmanager
async def build_agent():
    load_dotenv(override=False)
    settings = Settings.from_env()

    document_repository = DocumentRepository(settings.sharepoint_docs_path)
    integration_repository = IntegrationRepository(settings.integrations_path)
    configure_tools(
        ToolContext(
            document_repository=document_repository,
            integration_repository=integration_repository,
            knowledge_gap_log_path=settings.knowledge_gap_log_path,
        )
    )

    async with DefaultAzureCredential() as credential:
        async with AzureAIClient(
            project_endpoint=settings.foundry_project_endpoint,
            model_deployment_name=settings.foundry_model_deployment_name,
            credential=credential,
        ).as_agent(
            name=settings.agent_name,
            instructions=_instructions(),
            tools=create_toolset(),
        ) as agent:
            yield agent