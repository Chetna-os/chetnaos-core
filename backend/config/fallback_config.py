# Central configuration for fallback behavior

FALLBACK_CONFIG = {
    "max_uncertainty": 0.6,
    "max_cost_per_task": 5.0,  # dollars / credits
    "max_runtime_sec": 30,
    "levels": {
        0: "HARD_STOP",
        1: "DEGRADE",
        2: "HUMAN_HANDOFF",
        3: "REFLECTION",
        4: "RECOVERY"
    },
    "default_level": 1,
    "human_required_levels": [2, 3],
}
