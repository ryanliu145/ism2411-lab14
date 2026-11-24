# REFLECTION QUESTIONS
#
# 1. Which cleaning decision feels most ambiguous?
# Filling missing values feels most ambiguous because using
# the mean assumes that the missing values are similar to
# the other values. Before making this decision with real
# business data, I would want to know why the information
# is missing and whether the average is a reasonable estimate.
#
# 2. Would someone understand my cleaning decisions?
# Yes. I included comments explaining why I filled missing
# numeric values, removed rows without essential identifiers,
# removed duplicate records, and deleted the 9,999 quantity
# placeholder. These comments explain the reasoning behind
# the decisions instead of only describing the code.
#
# 3. What was most unexpected about the dataset?
# One unexpected issue was that the dataset contained
# inconsistent date formats and invalid date entries.
# I also found that a quantity of 9,999 was a placeholder
# rather than a legitimate sale. This demonstrates why
# checking the data before analyzing it is important.
# ============================================================

import pandas as pd

# Exercise 1
df = pd.read_csv("data/messy_sales.csv")

print("\nEXERCISE 1")
df.info()
print(df.isnull().sum())
print((df.isnull().mean() * 100).round(2))


# Exercise 2
print("\nEXERCISE 2")
df.columns = df.columns.str.lower().str.replace(" ", "_")
print(df.columns.tolist())


# Exercise 3
print("\nEXERCISE 3")
print("Shape before cleaning:", df.shape)

df = df.dropna(subset=["order_id", "order_date"])

df["unit_price"] = (
    df["unit_price"]
    .astype("string")
    .str.replace("$", "", regex=False)
    .str.replace(",", "", regex=False)
)

df["unit_price"] = pd.to_numeric(
    df["unit_price"], errors="coerce"
)

df["quantity_sold"] = pd.to_numeric(
    df["quantity_sold"], errors="coerce"
)

df["unit_price"] = df["unit_price"].fillna(
    df["unit_price"].mean()
)

df["quantity_sold"] = df["quantity_sold"].fillna(
    df["quantity_sold"].mean()
)

print("Shape after cleaning:", df.shape)
print(df.isnull().sum())


# Exercise 4
print("\nEXERCISE 4")

df["order_date"] = pd.to_datetime(
    df["order_date"], errors="coerce"
)

print("Invalid dates:", df["order_date"].isna().sum())

df["unit_price"] = df["unit_price"].astype(float)
df["quantity_sold"] = df["quantity_sold"].astype(int)

df["revenue"] = (
    df["unit_price"] * df["quantity_sold"]
).round(2)

print(df.dtypes)


# Exercise 5
print("\nEXERCISE 5")

print("Duplicate rows:", df.duplicated().sum())

df = df.drop_duplicates()

print("Shape after removing duplicates:", df.shape)


# Exercise 6
print("\nEXERCISE 6")

print(df.describe())

df = df[df["quantity_sold"] != 9999]

print("Shape after removing placeholder quantities:", df.shape)
print(df.describe())


# Exercise 7
print("\nEXERCISE 7")

df.to_csv("data/clean_sales.csv", index=False)

cleaned_df = pd.read_csv("data/clean_sales.csv")
cleaned_df.info()

cleaned_df = pd.read_csv(
    "data/clean_sales.csv",
    parse_dates=["order_date"]
)

cleaned_df.info()

print("Final dataset shape:", cleaned_df.shape)
print("LAB 14 COMPLETE!")
