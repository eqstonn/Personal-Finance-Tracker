"""
Simple script to delete expenses from the database.
Usage: python delete_expense.py <expense_id>
Or run without arguments to see all expenses and choose one to delete.
"""
import sqlite3
import sys
import os

# Path to your database
db_path = os.path.join(os.path.dirname(__file__), 'instance', 'expenses.db')

def list_expenses():
    """List all expenses"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT id, description, amount, category, date FROM expense ORDER BY date DESC")
    expenses = cursor.fetchall()
    conn.close()
    
    if not expenses:
        print("No expenses found.")
        return
    
    print("\nCurrent Expenses:")
    print("-" * 80)
    print(f"{'ID':<5} {'Description':<20} {'Amount':<10} {'Category':<15} {'Date':<12}")
    print("-" * 80)
    for exp in expenses:
        print(f"{exp[0]:<5} {exp[1]:<20} ${exp[2]:<9.2f} {exp[3]:<15} {exp[4]}")
    print("-" * 80)
    return expenses

def delete_expense(expense_id):
    """Delete an expense by ID"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # First check if it exists
    cursor.execute("SELECT id, description, amount FROM expense WHERE id = ?", (expense_id,))
    expense = cursor.fetchone()
    
    if not expense:
        print(f"Expense with ID {expense_id} not found.")
        conn.close()
        return False
    
    print(f"\nAbout to delete: ID {expense[0]} - {expense[1]} - ${expense[2]}")
    confirm = input("Are you sure? (yes/no): ").strip().lower()
    
    if confirm == 'yes':
        cursor.execute("DELETE FROM expense WHERE id = ?", (expense_id,))
        conn.commit()
        conn.close()
        print(f"Expense ID {expense_id} deleted successfully!")
        return True
    else:
        print("Deletion cancelled.")
        conn.close()
        return False

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Delete specific expense ID
        try:
            expense_id = int(sys.argv[1])
            delete_expense(expense_id)
        except ValueError:
            print("Error: Expense ID must be a number.")
    else:
        # Interactive mode - show all expenses and let user choose
        expenses = list_expenses()
        if expenses:
            try:
                expense_id = int(input("\nEnter the ID of the expense to delete (or 0 to cancel): "))
                if expense_id > 0:
                    delete_expense(expense_id)
                else:
                    print("Cancelled.")
            except ValueError:
                print("Error: Please enter a valid number.")
            except KeyboardInterrupt:
                print("\nCancelled.")
