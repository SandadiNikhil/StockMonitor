def analyze_sp500_output(input_file="sp500_output.txt"):
    """
    Analyzes the sp500_output.txt file, extracts Total Fundamental Scores,
    sorts companies by score, and prints the top and bottom 10.
    """
    company_scores = []

    try:
        with open(input_file, "r") as infile:
            current_company_output = ""
            current_symbol = None
            reading_company_block = False

            for line in infile:
                line = line.strip()
                if line.startswith("---------- START OF OUTPUT FOR"):
                    reading_company_block = True
                    current_symbol = line.split("FOR")[-1].strip().strip('- ') # Extract symbol from start line
                    current_company_output = "" # Reset output for new company
                    continue # Skip to next line after start marker

                if line.startswith("---------- END OF OUTPUT FOR"):
                    reading_company_block = False
                    if current_symbol and current_company_output:
                        score = extract_total_fundamental_score(current_company_output)
                        if score is not None:
                            company_scores.append({'symbol': current_symbol, 'score': score})
                    current_symbol = None # Reset symbol
                    continue # Skip to next line after end marker

                if reading_company_block:
                    current_company_output += line + "\n" # Accumulate output lines for current company

    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found. Make sure you ran run_sp500.py first.")
        return

    if not company_scores:
        print("No Total Fundamental Scores found in the output file. Check the output file format.")
        return

    # Sort companies by score in descending order
    company_scores.sort(key=lambda item: item['score'], reverse=True)

    print("----- Top 10 Companies by Total Fundamental Score -----")
    for i in range(min(10, len(company_scores))):
        company = company_scores[i]
        print(f"{i+1}. {company['symbol']}: Score = {company['score']:.2f}")

    print("\n----- Bottom 10 Companies by Total Fundamental Score -----")
    for i in range(max(0, len(company_scores) - 10), len(company_scores)): # Start index to get last 10
        company = company_scores[i]
        print(f"{i+1}. {company['symbol']}: Score = {company['score']:.2f}")


def extract_total_fundamental_score(company_output):
    """
    Extracts the Total Fundamental Score from a company's output text block.
    Returns the score as a float, or None if not found.
    """
    for line in company_output.splitlines():
        if "Total Fundamental Score" in line and "out of 100" in line:
            try:
                score_str = line.split(":")[-1].strip() # Get part after colon, remove whitespace
                return float(score_str) # Convert to float
            except ValueError:
                print(f"Warning: Could not parse score value from line: '{line}'")
                return None # Parsing error
    return None # Score not found in output


if __name__ == "__main__":
    analyze_sp500_output()