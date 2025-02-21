#!/usr/bin/env python
import sys
import warnings
from datetime import datetime

from crew import SalesContactFinderCrew

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")


def run():
    """Run the crew."""
    print("Starting crew run...")

    inputs = {
        "target_company": "Mattress King - Nashville, TN",  # Add this for template
        "our_product": "Marketing Tool Kit",  # Add this for template
        "file_name": "Mattress_King_Prospecting_Report.md",
        "folder": "Sales Prospecting Reports",
        "slack_channel": "jandice",
    }

    print("Created inputs:", inputs)
    try:
        print("Creating crew...")
        crew = SalesContactFinderCrew()
        print("Getting crew instance...")
        crew_instance = crew.crew()
        print("Starting kickoff...")
        crew_instance.kickoff(inputs=inputs)
    except Exception as e:
        print("Error details:", str(e))
        raise Exception(f"An error occurred while running the crew: {e}")


if __name__ == "__main__":
    run()
