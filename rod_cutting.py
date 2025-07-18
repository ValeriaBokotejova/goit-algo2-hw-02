from typing import List, Dict, Tuple
from colorama import Fore, Style, init, Back

init(autoreset=True)


def rod_cutting_memo(length: int, prices: List[int]) -> Dict:
    """
    Compute the maximum profit for cutting a rod of given length using recursion + memoization.

    Args:
        length: total length of the rod (must be > 0)
        prices: prices[i] is the price of a rod of length (i+1)

    Returns:
        {
            "max_profit": int,         # best achievable profit
            "cuts": List[int],         # list of segment lengths that achieve it
            "number_of_cuts": int      # number of cuts made (segments-1)
        }
    """

    memo: Dict[int, Tuple[int, List[int]]] = {}

    def helper(n: int) -> Tuple[int, List[int]]:
        # Base case
        if n == 0:
            return 0, []
        if n in memo:
            return memo[n]

        max_profit = 0
        best_cuts: List[int] = []

        for i in range(1, n + 1):
            current_profit = prices[i - 1]
            remainder_profit, remainder_cuts = helper(n - i)
            total_profit = current_profit + remainder_profit

            if total_profit > max_profit:
                max_profit = total_profit
                best_cuts = [i] + remainder_cuts

        memo[n] = (max_profit, best_cuts)
        return memo[n]

    max_profit, cuts = helper(length)
    return {
        "max_profit": max_profit,
        "cuts": cuts,
        "number_of_cuts": max(0, len(cuts) - 1)
    }

def rod_cutting_table(length: int, prices: List[int]) -> Dict:
    """
    Finds the optimal rod cutting using bottom-up dynamic programming (tabulation).

    Args:
        length: The length of the rod.
        prices: List of prices where prices[i] is the price for a rod of length i+1.

    Returns:
        Dict containing:
            - max_profit: Maximum profit achievable.
            - cuts: List of segment lengths.
            - number_of_cuts: Total number of cuts made.
    """

    dp = [0] * (length + 1)
    first_cut = [0] * (length + 1)

    for j in range(1, length + 1):
        max_profit = 0
        cut_at = 0
        for i in range(1, j + 1):
            current_profit = prices[i - 1] + dp[j - i]
            if current_profit > max_profit:
                max_profit = current_profit
                cut_at = i
        dp[j] = max_profit
        first_cut[j] = cut_at

    cuts: List[int] = []
    remaining = length
    while remaining > 0:
        cut_size = first_cut[remaining]
        cuts.append(cut_size)
        remaining -= cut_size

    return {
        "max_profit": dp[length],
        "cuts": cuts,
        "number_of_cuts": max(0, len(cuts) - 1)
    }

def run_tests():
    """Run predefined test cases for both methods."""
    test_cases = [
        {"length": 5, "prices": [2, 5, 7, 8, 10], "name": "Basic Case"},
        {"length": 3, "prices": [1, 3, 8], "name": "No Cut Optimal"},
        {"length": 4, "prices": [3, 5, 6, 7], "name": "Uniform Cuts"}
    ]

    for test in test_cases:
        length = test["length"]
        prices = test["prices"]
        name = test["name"]
        print(f"\n{Back.BLUE}Test: {name}")
        print(f"Length: {length}")
        print(f"Prices: {prices}")

        memo_result = rod_cutting_memo(length, prices)
        print(f"\n{Style.BRIGHT}Memoization Result:")
        print(f"{Fore.CYAN}  Max Profit: {memo_result['max_profit']}")
        print(f"  Cuts: {memo_result['cuts']}")
        print(f"  Number of Cuts: {memo_result['number_of_cuts']}")

        table_result = rod_cutting_table(length, prices)
        print(f"\n{Style.BRIGHT}Tabulation Result:")
        print(f"{Fore.CYAN}  Max Profit: {table_result['max_profit']}")
        print(f"  Cuts: {table_result['cuts']}")
        print(f"  Number of Cuts: {table_result['number_of_cuts']}")
        print("\nTest passed successfully!")

if __name__ == "__main__":
    run_tests()
