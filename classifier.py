import pandas as pd
from typing import Iterable, Optional, Tuple

# ordered rules (priority; first match wins)
RULES: list[tuple[str, list[str]]] = [
    ("FY", ["first year", "first-year", "1st year", "1st-year", "spring week", "insight", "early careers", "discover"]),
    ("VS", ["vac scheme", "vacation scheme", "summer scheme", "winter scheme"]),
    ("TC", ["training contract", "trainee solicitor"]),
    ("OPEN", ["open day", "workshop"]),
    ("SCHOLAR", ["scholarship"]),
]


def classify_title(title, rules=RULES):
    """Return (label, matched_keyword). Label is 'UNKNOWN' if no rule matches."""
    t = (title or "").lower()
    for label, keywords in rules:
        for k in keywords:
            if k in t:
                return label, k
    return "UNKNOWN", None


def main():
    df = pd.read_csv("legalcheek_deadlines.csv")

    # programme type, programme type reason
    out = df["title"].fillna("").apply(classify_title)
    df["programme_type"] = out.apply(lambda x: x[0])

    # print classified rows
    for title, label in zip(df["title"].fillna(""), df["programme_type"]):
        print(label, title)

    # print summary
    print("\n*** Summary ***\n")
    print(df["programme_type"].value_counts(dropna=False))

    # save as csv
    # df.to_csv("legalcheek_deadlines_classified.csv", index=False)


if __name__ == "__main__":
    main()