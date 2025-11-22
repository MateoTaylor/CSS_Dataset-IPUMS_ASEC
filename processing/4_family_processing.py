import os
import pandas as pd
from pathlib import Path

EXTRACT_NUM = 7

class Family:
    def __init__(self, cpsid, famunit, famid):
        self.cpsid = cpsid
        self.famunit = famunit
        self.famid = famid
        self.children = []
        self.adults = []
        self.armed_forces = []
        self.has_cpselig_adult = False
        self.total_fam_income = 0

    def add_person(self, person):
        if person["INCTOT"] != 999999999 and person["INCTOT"] != 999999998:
            self.total_fam_income += person["INCTOT"]
        if person["POPSTAT"] == 1:  # Adult
            self.adults.append(person)
            if person["CSELIG"] == 1:
                self.has_cpselig_adult = True
        elif person["POPSTAT"] == 2:  # Armed Forces
            self.armed_forces.append(person)
        elif person["POPSTAT"] == 3:  # Child
            self.children.append(person)
        else:
            raise ValueError(f"Unknown POPSTAT value: {person['POPSTAT']}")
        
    
def construct_families(df, fam_type):
    #fam_type: 'IPUMS_FAMID' or 'CENSUS_FAMID' for which famid 
    # family table

    # loop through each row and create Family objects
    families = {}
    for index, person in df.iterrows():
        # if the person's family is not in the families dict, create a new Family object
        if families.get(person[fam_type]) is None:
            families[person[fam_type]] = Family(person["CPSID"], person["FAMUNIT"], person[fam_type])
        # add the person to the family
        families[person[fam_type]].add_person(person)
    return families

if __name__ == "__main__":
    input_dir = Path("data/processed")
    # Create output directory if it doesn't exist
    output_dir = Path("data/processed")
    os.makedirs(output_dir, exist_ok=True)

    df = pd.read_csv(input_dir / f"cps_0000{EXTRACT_NUM}_famid.csv")

    print(f"Unique IPUMS families: {df['IPUMS_FAMID'].nunique()}")
    print(f"Unique Census families: {df['CENSUS_FAMID'].nunique()}")

    ipums_families = construct_families(df, fam_type="IPUMS_FAMID")
    census_families = construct_families(df, fam_type="CENSUS_FAMID")
    
    # add total fam income for ipums families (already exists for census families)
    # additionally, add num_children, num_adults, num_armed_forces, has_cpselig_adult for each person
    df["IPUMS_FTOTVAL"] = df["IPUMS_FAMID"].apply(lambda famid: ipums_families[famid].total_fam_income)
    df["IPUMS_NUM_CHILDREN"] = df["IPUMS_FAMID"].apply(lambda famid: len(ipums_families[famid].children))
    df["IPUMS_NUM_ADULTS"] = df["IPUMS_FAMID"].apply(lambda famid: len(ipums_families[famid].adults))
    df["IPUMS_NUM_ARMED_FORCES"] = df["IPUMS_FAMID"].apply(lambda famid: len(ipums_families[famid].armed_forces))
    df["IPUMS_HAS_CPSELIG_ADULT"] = df["IPUMS_FAMID"].apply(lambda famid: ipums_families[famid].has_cpselig_adult)

    # do the same for census families byt w/o the fam income
    df["CENSUS_NUM_CHILDREN"] = df["CENSUS_FAMID"].apply(lambda famid: len(census_families[famid].children))
    df["CENSUS_NUM_ADULTS"] = df["CENSUS_FAMID"].apply(lambda famid: len(census_families[famid].adults))
    df["CENSUS_NUM_ARMED_FORCES"] = df["CENSUS_FAMID"].apply(lambda famid: len(census_families[famid].armed_forces))
    df["CENSUS_HAS_CPSELIG_ADULT"] = df["CENSUS_FAMID"].apply(lambda famid: census_families[famid].has_cpselig_adult)

    # save w the new columns
    df.to_csv(output_dir / f"cps_0000{EXTRACT_NUM}_family_info.csv", index=False)

"""
    # now we test to see what vars are consistent across families
    num_cselig = 0
    num_inconsistent_cselig = 0
    for family in families.values():
        # asset that CSELIG is consistent across family members
        cselig_adults = 0
        cselig_children = 0
        for member in family.adults:
            cselig_adults += member["CSELIG"]
        for member in family.armed_forces:
            cselig_children += member["CSELIG"]
        if cselig_children > 0:
            num_inconsistent_cselig += 1
            print(f"Family {family.famid} has {cselig_children} armed_forces CSELIG values.")
            
    print(f"Total families: {len(families)}")
    print(f"Number of families with multiple CSELIG values: {num_inconsistent_cselig}")
    print(f"Number of families eligible for child support (CSELIG=1): {num_cselig}")

    # notes:
    # the only families that exist w/ all members having CSELIG=1 have length 1
    # families can have multiple members with CSELIG = 1
    

"""