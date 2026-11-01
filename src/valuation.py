import re
import json
import pandas as pd
import streamlit as st
from pathlib import Path

SITE_DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "sites.json"

def parse_pasted_sigs(pasted_sigs, site_data_path=SITE_DATA_PATH):
    # Takes a string of tab delineated lines containing
    # Signature Code: ABC-123
    # Site Type: Combat, Gas, Ore
    # Site Name
    # Location: JSIG and Class Designation
    # 
    # Parses the input string and returns
    # a pandas dataframe containing the
    # viable sites from the input paste
    rows = []
    for line in pasted_sigs.splitlines():
        # Split the string by tabs
        fields = line.split("\t")
        # Remove leading whitespace tab if present
        if fields[0] == "":
            fields = fields[1:]
        # Pull the values into variables for each thing
        signature_code, site_type, location, site_name = fields[:4]
        match = re.search(
            r"C[1-9][A-Za-z]?$",
            location, 
            re.IGNORECASE
        )
        if match:
            rows.append({
                "Signature Code": signature_code,
                "Site Type": site_type,
                "Site Name": site_name,
                "Location": match.group()
        })
    df = pd.DataFrame(rows)
    if not Path(site_data_path).exists():
        raise FileNotFoundError(
            f"Looking for site data at: {Path(site_data_path).resolve()}"
        )
    with open(site_data_path, "r", encoding="utf-8") as file:
        sites = json.load(file)

    value_by_name = {
        site["Site Name"].strip().casefold(): site["Value"]
        for site in sites
    }

    df["Value"] = df["Site Name"].str.casefold().map(value_by_name)
    df = df.dropna(subset=["Value"]).reset_index(drop=True)
    return df

def tally_site_values(site_list):
    # Adds the values of all sites on site list
    # Takes a list of sites returns an integer
    return site_list["Value"].sum()