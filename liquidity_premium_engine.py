# assignment script to analyze liquidity premiums on yield curves
# Splits credit risk from liquidity costs 

import numpy as np
import pandas as pd

def process_liquidity_data():
    # step 1: load up the detailed market data sheet
    file_name = 'market_yield_curves.csv'
    try:
        raw_data = pd.read_csv(file_name)
    except:
        print("Fatal error: csv tracking file is completely missing")
        return

    print("--- Starting Multi-Step Liquidity Premium Processing Engine ---")
    print(f"Successfully loaded {len(raw_data)} rows of market data points.\n")

    # step 2: isolate values and calculate the total spread
    # the total spread is just funding cost minus the risk-free government rate
    raw_data['Total_Spread_Pct'] = raw_data['Wholesale_Funding_Cost_Pct'] - raw_data['Government_Yield_Pct']
    
    # step 3: break down the liquidity premium component
    # proxy estimation: using transaction volumes to scale the liquidity drag
    # less volume in a tenor means cash is harder to move, pushing premium up
    base_credit_risk_proxy = 0.0020 # assume a constant 20 basis points for base credit risk
    
    liquidity_premiums = []
    for idx, row in raw_data.iterrows():
        vol = row['Transaction_Volume_Millions']
        total_spread = row['Total_Spread_Pct']
        
        # basic volume scaling factor to calculate liquidity friction
        if vol > 500:
            volume_friction = 0.0005 # high volume = low liquidity cost
        elif vol > 300:
            volume_friction = 0.0015 # medium volume
        else:
            volume_friction = 0.0030 # low volume = high liquidity lockup cost
            
        # calculated premium cannot exceed the actual total spread
        estimated_premium = min(total_spread, base_credit_risk_proxy + volume_friction)
        liquidity_premiums.append(estimated_premium)
        
    raw_data['Estimated_Liquidity_Premium'] = liquidity_premiums

    # step 4: calculate average curve metrics grouped by tenor months
    # this provides a clean snapshot of the term structure of liquidity
    summary_matrix = raw_data.groupby('Tenor_Months').agg({
        'Government_Yield_Pct': 'mean',
        'Wholesale_Funding_Cost_Pct': 'mean',
        'Total_Spread_Pct': 'mean',
        'Estimated_Liquidity_Premium': 'mean'
    }).reset_index()

    # step 5: report results to screen in a clean structural layout
    print("---------------------------------------------------------------------")
    print("               ESTIMATED LIQUIDITY TERM STRUCTURE REPORT             ")
    print("---------------------------------------------------------------------")
    print("Tenor(Mo) | Gov Yield | Funding Cost | Total Spread | Liquidity Prem")
    print("---------------------------------------------------------------------")
    
    for idx, row in summary_matrix.iterrows():
        tenor = int(row['Tenor_Months'])
        gov = row['Government_Yield_Pct'] * 100
        fund = row['Wholesale_Funding_Cost_Pct'] * 100
        spread = row['Total_Spread_Pct'] * 100
        prem = row['Estimated_Liquidity_Premium'] * 100
        
        print(f" {tenor:7d}M |  {gov:7.3f}% |   {fund:8.3f}% |   {spread:8.3f}% |    {prem:7.3f}%")
        
    print("---------------------------------------------------------------------")
    
    # step 6: calculate net portfolio impact logic
    # checking if long-term lockups are getting too expensive to fund safely
    long_term_premium = summary_matrix.loc[summary_matrix['Tenor_Months'] == 12, 'Estimated_Liquidity_Premium'].values[0]
    
    if long_term_premium > 0.0040:
        print("Analysis Alert: 12-Month liquidity premium exceeds 40bps threshold.")
        print("Action Required: Adjust internal transfer pricing to penalize long lockups.")
    else:
        print("Analysis Status: Term structure curve parameters remain stable.")
    print("=====================================================================\n")

if __name__ == "__main__":
    process_liquidity_data()
