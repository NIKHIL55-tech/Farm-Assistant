from agents.base_agent import BaseAgent

class MarketResearcher(BaseAgent):
    def process_message(self, sender, message):
        # Sample market message processing
        print(f"[{self.name}] Market trend: Tomato prices are up in Telangana.")
