"""cost_tracker.py — Token budget enforcer"""
import tiktoken

class BudgetExceededError(Exception):
    pass

class TokenBudget:
    COST_PER_1K = {"gpt-4o": 0.005, "gpt-4o-mini": 0.00015}

    def __init__(self, max_tokens: int = 80_000, model: str = "gpt-4o"):
        self.max_tokens = max_tokens
        self.model = model
        self.used = 0
        self._enc = tiktoken.encoding_for_model("gpt-4o")

    def count(self, text: str) -> int:
        return len(self._enc.encode(text))

    def add(self, text: str):
        n = self.count(text)
        self.used += n
        if self.used > self.max_tokens:
            raise BudgetExceededError(f"Token budget exceeded: {self.used}/{self.max_tokens}")

    def summary(self) -> dict:
        return {"used_tokens": self.used, "max_tokens": self.max_tokens,
                "pct_used": round(self.used / self.max_tokens * 100, 1)}

    def estimated_cost(self) -> str:
        rate = self.COST_PER_1K.get(self.model, 0.005)
        cost = (self.used / 1000) * rate
        return f"${cost:.4f}"

    def __enter__(self): return self
    def __exit__(self, *_): pass
