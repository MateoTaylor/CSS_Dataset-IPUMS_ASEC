'''
Read .dat.gz data out from /data directory and convert to csv files in /data/csv directory
'''

from pathlib import Path
from ipumspy import readers, ddi

EXTRACT_NUM = 7


if __name__ == "__main__":
    # Create output directory if it doesn't exist
    output_dir = Path("data/ipums_csv")
    download_dir = Path("data/ipums_direct")

    ddi_file = Path(f"data/ipums_direct/cps_0000{EXTRACT_NUM}.xml")
    ddi = readers.read_ipums_ddi(ddi_file)

    ipums_df = readers.read_microdata(ddi, download_dir / ddi.file_description.filename)

    print(f"Dataframe shape: {ipums_df.shape}")

    output_file = output_dir / f"cps_0000{EXTRACT_NUM}.csv"
    print(ipums_df.head())
    ipums_df.to_csv(output_file, index=False)