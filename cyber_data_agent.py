import pandas as pd
import numpy as np

from typing import List, Dict, Any
from dataclasses import dataclass

from pydantic import BaseModel, Field
from agents import Agent, RunContext, Tool, AgentResponse

df = pd.read_csv('~/Downloads/cleaned_data.csv')

@dataclass
class Deps:
    df: pd.DataFrame

agent = Agent(
        model="gpt-3.5-turbo",
        system_prompt="You are a cybersecurity data analysis agent. You will be provided with a dataset of attempted logins to a honeypot. Your task is to analyze the data and provide insights. You will be provided with a list of questions, and you should answer them based on the data provided.",
        deps_type=Deps,
        retries=10,
        )

@agent.tool
async def query_df(ctx: RunContext[Deps], query: str) -> str:
    """
    Query the dataframe with a given query string.
    """
    try:
        return str(pd.eval(query, target=ctx.deps.df))
    except Exception as e:
        raise ModelRetry(f"Error executing query: {e}") from e

def ask_agent(question):
    deps = Deps(df)
    print(question)
    res = agent.run_sync(question, deps=deps)
    print(response.new_message()[-1].content)
    print("--------------------")







