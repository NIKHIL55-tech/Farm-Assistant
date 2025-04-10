# core/coordinator.py
class Coordinator:
    def __init__(self, agents, weights):
        self.agents = agents
        self.weights = weights  # e.g., {"economic": 0.6, "environmental": 0.4}

    def collect_recommendations(self, message):
        results = {}
        for agent in self.agents:
            response = agent.run(message)
            if response:
                results[agent.name] = response
        return results

    def resolve_conflicts(self, recommendations):
        # Simple weighted scoring mechanism
        score_map = {}
        for agent, rec in recommendations.items():
            for key, val in rec.items():
                score_map[key] = score_map.get(key, 0) + val * self.weights.get(key, 1)
        return score_map
