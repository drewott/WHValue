import re
import json
import pandas as pd
import streamlit as st
from pathlib import Path

SITE_DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "sites.json"

def parse_pasted_sigs(pasted_sigs, site_data_path=SITE_DATA_PATH):
    rows = []
    for line in pasted_sigs.splitlines():
        fields = line.split("\t")
        if len(fields) < 5:
            continue

        signature_code, site_type, jsig = fields[:3]

    match = re.match(
        r"^\s*(\S+)\s+Cosmic\s+Anomaly\s+(Ore|Wormhole|Combat|Data|Relic|Gas)\s+Site\s+(.+?)(?=\s+\d+(?:\.\d+)?%)",
        line, 
        re.IGNORECASE
    )
        location = match.group(3)
        if not match or site_type == "—":
            continue
        # Split the location into two sig code and the class designation
        

        # Combine the site names
        site_name = " ".join(fields[3:-2])
        if site_name == "—":
            continue

        # Fill the rows list
        rows.append({
            "Signature Code": signature_code,
            "Site Type": site_type,
            "Site Name": site_name,
            "Location": location,
        })

    df = pd.DataFrame(
        rows,
        columns=["Signature Code", "Site Type", "Site Name", "Location"],
    )

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
    return site_list["Value"].sum()