'''
General methods for retrieving IPUMS data. note the ipumspy website says you have to cite them
at some point? https://ipumspy.readthedocs.io/en/latest/
'''
import os
from dotenv import load_dotenv
from pathlib import Path
from ipumspy import IpumsApiClient, MicrodataExtract


if __name__ == "__main__":
    load_dotenv()
    IPUMS_API_KEY = os.getenv("IPUMS_API_KEY")

    # load all the variables we want from variables_clean.txt
    with open("variables_clean.txt", "r") as f:
        variables_of_interest = [line.strip() for line in f.readlines()]

    print(f"Variables of interest: {variables_of_interest}")
    
    # connect to ipums api
    headers = {
        "Authorization": IPUMS_API_KEY
    }
    ipums = IpumsApiClient(IPUMS_API_KEY)
    
    # Create an extract request
    extract = MicrodataExtract(
        collection="cps",
        description="Sample CPS extract",
        samples=[f"cps20{year:02d}_03s" for year in [23, 20, 18, 17, 16, 14, 12, 10, 8, 6, 4, 2, 0]],  # ASEC samples
        variables=variables_of_interest,
    )

    ipums.submit_extract(extract)
    print(f"Extract submitted with id {extract.extract_id}")
    #> Extract submitted with id 1

    # Wait for the extract to finish
    ipums.wait_for_extract(extract)

    print(f"Extract {extract.extract_id} is ready for download")
    # Download the extract
    DOWNLOAD_DIR = Path("data/ipums_direct")
    ipums.download_extract(extract, download_dir=DOWNLOAD_DIR)
    print(f"Extract {extract.extract_id} downloaded to {DOWNLOAD_DIR}")


