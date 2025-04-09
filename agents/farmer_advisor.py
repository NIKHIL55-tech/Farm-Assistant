from agents.base_agent import BaseAgent

class FarmerAdvisor(BaseAgent):
    def process_message(self, sender, message):
        # Sample processing
        print(f"[{self.name}] Advice based on land & preference: Try millets or pulses for sustainability.")
