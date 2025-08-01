import os
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate

class ReleaseNoteGenerator:
    def __init__(self, model_name=None, openai_api_key=None):
        # Read Azure OpenAI environment variables
        azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        azure_deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")
        azure_api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2023-05-15")
        openai_api_key = openai_api_key or os.getenv("AZURE_OPENAI_API_KEY")

        # If using Azure, pass endpoint, deployment, and api_version
        # For LangChain's ChatOpenAI: 
        # - model = deployment name (not model name like "gpt-3.5-turbo")
        # - base_url = azure endpoint
        # - api_version = azure api version
        # - openai_api_key = azure key
        # - azure = True

        self.llm = ChatOpenAI(
            model=azure_deployment,
            openai_api_key=openai_api_key,
            base_url=azure_endpoint,
            api_version=azure_api_version,
            azure=True
        )
        self.prompt = PromptTemplate(
            input_variables=["commits"],
            template="""
You are a professional release note generator. Given the following commit messages and pull request descriptions, generate a structured release note.

Organize the content into the following sections:
- ✨ Features
- 🐛 Bug Fixes
- 🛠️ Improvements
- 📚 Documentation

Use clear, concise language suitable for developers and stakeholders.

Commits and PRs:
{commits}

Release Notes:
"""
        )
        self.chain = self.prompt | self.llm

    def generate(self, commits: str) -> str:
        return self.chain.invoke({"commits": commits})