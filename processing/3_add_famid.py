import os
import pandas as pd
from pathlib import Path

EXTRACT_NUM = 7

if __name__ == "__main__":
    input_dir = Path("data/ipums_csv")
    # Create output directory if it doesn't exist
    output_dir = Path("data/processed")
    os.makedirs(output_dir, exist_ok=True)

    df = pd.read_csv(input_dir / f"cps_0000{EXTRACT_NUM}.csv")
    print(f"Dataframe shape: {df.shape}")
    # print(df.head(5))

    # IPUMS_FAMID = CPSID + FAMUNIT
    df["IPUMS_FAMID"] = df.apply(lambda row: str(int(row["CPSID"])) + str(int(row["FAMUNIT"])), axis=1)
    df["IPUMS_FAMID"] = df["IPUMS_FAMID"].astype("int64")

    # CENSUS_FAMID = CPSID + FAMID
    df["CENSUS_FAMID"] = df.apply(lambda row: str(int(row["CPSID"])) + str(int(row["FAMID"])), axis=1)
    df["CENSUS_FAMID"] = df["CENSUS_FAMID"].astype("int64")

    # save w the new columns
    df.to_csv(output_dir / f"cps_0000{EXTRACT_NUM}_famid.csv", index=False)

