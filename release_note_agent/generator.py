import os
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate

class ReleaseNoteGenerator:
    def __init__(self, model_name=None, openai_api_key=None):
        # Use standard Azure OpenAI environment variables
        azure_endpoint = os.getenv("OPENAI_API_BASE")  # e.g. https://YOUR-RESOURCE.openai.azure.com/
        azure_deployment = model_name or os.getenv("AZURE_OPENAI_DEPLOYMENT")
        openai_api_key = openai_api_key or os.getenv("OPENAI_API_KEY")

        if not azure_endpoint or not azure_deployment or not openai_api_key:
            raise ValueError(
                "Azure OpenAI environment variables missing! "
                "Set OPENAI_API_KEY, OPENAI_API_BASE, and AZURE_OPENAI_DEPLOYMENT_NAME."
            )
        
        required_vars = {
            "OPENAI_API_KEY": openai_api_key,
            "OPENAI_API_BASE": azure_endpoint,
            "AZURE_OPENAI_DEPLOYMENT_NAME": azure_deployment,
            "OPENAI_API_VERSION": os.getenv("OPENAI_API_VERSION")
        }

        missing = [key for key, val in required_vars.items() if not val]
        if missing:
            raise ValueError(f"Missing required environment variables: {', '.join(missing)}")


        self.llm = ChatOpenAI(
            model=azure_deployment,
            openai_api_key=openai_api_key,
            base_url=azure_endpoint,
            model_kwargs={"api_version": os.getenv("OPENAI_API_VERSION")}  # ✅ Correct way

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