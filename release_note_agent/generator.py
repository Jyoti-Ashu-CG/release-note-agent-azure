import os
from langchain_openai import AzureChatOpenAI  # ✅ Use Azure-specific class
from langchain.prompts import PromptTemplate

class ReleaseNoteGenerator:
    def __init__(self, model_name=None, openai_api_key=None):
        azure_endpoint = os.getenv("OPENAI_API_BASE")
        azure_deployment = model_name or os.getenv("AZURE_OPENAI_DEPLOYMENT")
        openai_api_key = openai_api_key or os.getenv("OPENAI_API_KEY")
        api_version = os.getenv("OPENAI_API_VERSION")

        required_vars = {
            "OPENAI_API_KEY": openai_api_key,
            "OPENAI_API_BASE": azure_endpoint,
            "AZURE_OPENAI_DEPLOYMENT": azure_deployment,
            "OPENAI_API_VERSION": api_version
        }
        missing = [key for key, val in required_vars.items() if not val]
        if missing:
            raise ValueError(f"❌ Missing required environment variables: {', '.join(missing)}")

        self.llm = AzureChatOpenAI(  # ✅ Correct class and parameters
            deployment_name=azure_deployment,
            openai_api_key=openai_api_key,
            azure_endpoint=azure_endpoint,
            api_version=api_version
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