from automathon import NFA

nfae = NFA(
    {"ic0", "0_s0", "0_s1", "fc0", "1_s0", "1_s1", "2_s0", "2_s1"},
    {"a", "b", "c"},
    {
        "ic0": {"": {"0_s0", "fc0"}},
        "0_s0": {"a": {"0_s1"}},
        "0_s1": {"": {"0_s0", "fc0"}},
        "fc0": {"": {"1_s0"}},
        "1_s0": {"b": {"1_s1"}},
        "1_s1": {"": {"ic0", "2_s0"}},
        "2_s0": {"c": {"2_s1"}},
        "2_s1": {},
    },
    "ic0",
    {"2_s1"},
)

nfae.view("NFAe Visualization")

nfa = NFA(
    {"S0", "S1", "S2", "S3"},
    {"a", "b", "c"},
    {
        "S0": {"a": {"S1"}, "b": {"S2"}},
        "S1": {"a": {"S1"}, "b": {"S2"}},
        "S2": {"a": {"S1"}, "b": {"S2"}, "c": {"S3"}},
        "S3": {},
    },
    "S0",
    {"S3"},
)

nfa.view("NFA Visualization")


nfam = NFA(
    {"s0", "s1", "s2"},
    {"a", "b", "c"},
    {
        "s0": {"a": {"s0"}, "b": {"s1"}},
        "s1": {"a": {"s0"}, "b": {"s1"}, "c": {"s2"}},
        "s2": {},
    },
    "s0",
    {"s2"},
)

nfam.view("NFAm Visualization")
