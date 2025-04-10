from core.coordinator import Coordinator

class DummyAgent:
    def __init__(self, name):
        self.name = name

    def run(self, message):
        return {"economic": 70, "environmental": 50}

def test_coordinator_conflict_resolution():
    agents = [DummyAgent("A1"), DummyAgent("A2")]
    weights = {"economic": 0.6, "environmental": 0.4}
    coord = Coordinator(agents, weights)

    recs = coord.collect_recommendations({})
    resolved = coord.resolve_conflicts(recs)

    assert "economic" in resolved
    assert "environmental" in resolved
