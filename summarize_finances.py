import pandas as pd
import sys

# use global variable for coin convention
CURRENCY = '$'

def summarize_finances(csv_file: str, date: str) -> pd.DataFrame:

    try:
        # Read the CSV file into a data frame
        df = pd.read_csv(csv_file, usecols=["date", "description", "category", "amount"])

        # Convert the date column to a datetime format
        df['date']      = pd.to_datetime(df['date'])

        # Extract year and month in format "%Y-%m"
        df = df[df['date'].dt.strftime('%Y-%m') == date]

        # Return the filtered DataFrame
        return df
    except pd.errors.EmptyDataError:
        print(f"Error: {csv_file} is empty")
    except FileNotFoundError:
        print(f"Error: {csv_file} not found")
    except ValueError:
        print(f"Error: {csv_file} is not in the correct format")



def total_summary(df: pd.DataFrame, currency: str) -> None:

    # calculate total income
    total_income     = df[df['amount'] > 0]['amount'].sum()

    # calculate total expenses
    total_expenses     = abs(df[df['amount'] < 0]['amount'].sum())

    month_year = df['date'].min().strftime('%B %Y')

    print("\n" + "Summary for {}".format(month_year))
    print(f"{ '-' * 30 }")
    print(f"Total income: {currency:>5}{total_income:.2f}")
    print(f"Total expenses: {currency:>3}{total_expenses:.2f}")


# print the summation of each category, by amount with their categories
def expenses_by_category(df: pd.DataFrame) -> dict:

    categorized_list = []

    category_sums = df[df['amount'] < 0].groupby('category')['amount'].sum()

    # convert the Series to a dictionary
    category_dict = category_sums.to_dict()

    # format the dictionary so that the amounts are positive and have two decimal places
    category_dict = {k: round(abs(v), 2) for k, v in category_dict.items()}

    # print the expenses by category to the console
    print("\nExpenses by Category")
    print(f"{ '-' * 30 }")
    for category, amount in category_dict.items():
        print(f"{category:<23}${amount:.2f}")

    return category_dict




def top_five_expenses(top_expenses: dict, currency: str) -> None:

    top_five_exp = 5
    # sort the list in descending order with length of 5

    sorted_dict = sorted(top_expenses.items(), key=lambda x: x[1], reverse=True)
    # sorted_dict = dict(sorted(top_expenses.items(), key=lambda x: x[1], reverse=True))
    sorted_dict = sorted_dict[:top_five_exp]

    print("\n" + "Top 5 expenses: ")
    print(f"{ '-' * 30 }")
    for i, (category, amount) in enumerate(sorted_dict, 1):
        print(f"{i}. {category:<20}${amount:.2f}")




if __name__ == "__main__":
    # open the file and call the function from here

    if not len(sys.argv) > 2:
        print("Please add a CSV file in order to run this program.")
        sys.exit()
    else:
        filename            = sys.argv[1]
        desired_month       = sys.argv[2]

        df              = summarize_finances(filename, desired_month)
        total_sum_list  = total_summary(df, CURRENCY)

        list_category_df = expenses_by_category(df)
        top_five_expenses(list_category_df, CURRENCY)


'''
pseudo code

TODO: create a container with the files to be executed

'''