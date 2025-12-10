# quick test snippet (run with python -m asyncio)
import asyncio
from backend.agents.sale_agent import SalesAgent

async def main():
    a = SalesAgent(client_id="demo", config={"project_info": {"name": "Kalpavriksha", "min_price": "25 Lakhs"}})
    r = await a.process("Hi, kitna price hai?", {})
    print(r)

asyncio.run(main())
      from backend.scientific_laws.law_engine import ScientificLawEngine

law_engine = ScientificLawEngine()
