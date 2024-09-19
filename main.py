import re
from phonebook import PhoneBook  # Importing the PhoneBook class to manage contacts and operations
from contact import Contact      # Importing Contact class to create contact instances

def validate_phone_number(phone_number):
    """
    make sure the phone number format match (###) ###-####
    :return: True if the phone number matches the format, False otherwise
    """
    pattern = r"\(\d{3}\) \d{3}-\d{4}"
    return re.fullmatch(pattern, phone_number) is not None

def validate_email(email):
    """
    make sure  the email that user input inculde contains "@" and "."
    :return: True if the email contains "@" and ".", False otherwise
    """
    return "@" in email and "." in email

def print_menu():
    """
    Prints the main menu for the phone book manager
    """
    print("\n" + "="*40)
    print("📒  Phone Book Manager 📒".center(40))  
    print("="*40)
    print("1. ➕ Add Contact")  
    print("2. 📄 Batch Import Contacts from CSV")  
    print("3. 📋 View Contacts")  
    print("4. 🔍 Search Contact")  
    print("5. 📅 Filter Contacts by Date")  
    print("6. ✏️  Update Contact")  
    print("7. 🗑️  Delete Contact by Name")  
    print("8. 🗑️  Batch Delete Contacts from CSV")  
    print("9. 💾 Save and Exit")  
    print("="*40)

def main():
    phonebook = PhoneBook()  
    
    # Load existing contacts when the program starts
    phonebook.load_from_file()

    while True:
        print_menu()  # Display the main menu
        choice = input("Enter your choice: ")  

        if choice == '1':  
            print("\n➕ Adding a new contact...")
            first_name = input("First Name: ")  
            last_name = input("Last Name: ")  
            phone_number = input("Phone Number (format: (###) ###-####): ")  
            if not validate_phone_number(phone_number):  
                print("❌ Invalid phone number format. Please use (###) ###-####.")
                continue  
            email = input("Email (Optional): ")  
            if email and not validate_email(email):  
                print("❌ Invalid email format.")
                continue  # If invalid, prompt user to try again
            address = input("Address (Optional): ")  # Prompt for address
            contact = Contact(first_name, last_name, phone_number, email, address)  # Create a Contact object
            phonebook.add_contact(contact)  # Add the contact to the phonebook
            print(f"✅ Contact {first_name} {last_name} added successfully!")  
        
        elif choice == '2':  
            csv_file = input("\n📄 Enter the path to the CSV file for importing contacts: ")  # Get CSV file path
            phonebook.batch_import(csv_file)  # Import contacts from CSV file
        
        elif choice == '3':  
            print("\n📋 Current contacts in phonebook:")
            phonebook.display_contacts() 
        
        elif choice == '4':  
            query = input("\n🔍 Enter name or phone number (or part of it) to search: ")  # Get search query
            results = phonebook.search_contact(query)  # Search the phonebook
            if results:
                print(f"\n🔍 Found {len(results)} contact(s):")
                for result in results:
                    print(result)  # Display search results
            else:
                print("❌ No contact found.")  # If no contact found, display message
        
        elif choice == '5':  # Option 5: Filter contacts by date
            start_date = input("Enter start date (YYYY-MM-DD): ")  
            end_date = input("Enter end date (YYYY-MM-DD): ")  
            results = phonebook.filter_by_date(start_date, end_date)  # Filter contacts by date
            if results:
                print(f"\n📅 Found {len(results)} contact(s) in the given date range:")
                for result in results:
                    print(result)  # Display filtered results
            else:
                print("❌ No contact found in the given date range.")  # If no contact found, display message
        
        elif choice == '6':  # Option 6: Update a contact
            first_name = input("Enter the first name of the contact to update: ")  # Get contact's first name
            last_name = input("Enter the last name of the contact to update: ")  # Get contact's last name
            
            # First check if the contact exists using precise first and last name matching
            contact_found = False
            for contact in phonebook.contacts:  # Loop through contacts to find a match
                if contact.first_name.lower() == first_name.lower() and contact.last_name.lower() == last_name.lower():
                    contact_found = True
                    break  # Stop searching once we find the contact

            if not contact_found:  # If no contact is found, print message and stop execution
                print(f"No contact found with the name {first_name} {last_name}.")
                continue  # Return to the menu
            
            # If contact exists, proceed with asking for new information
            new_first_name = input("New First Name (leave blank to skip): ")
            new_last_name = input("New Last Name (leave blank to skip): ")
            new_phone_number = input("New Phone Number (leave blank to skip): ")
            if new_phone_number and not validate_phone_number(new_phone_number):  # Validate new phone number
                print("❌ Invalid phone number format.")
                continue
            new_email = input("New Email (Optional, leave blank to skip): ")  # Get new email
            if new_email and not validate_email(new_email):  # Validate new email format
                print("❌ Invalid email format.")
                continue
            new_address = input("New Address (Optional, leave blank to skip): ")  # Get new address

            # Update the contact information
            phonebook.update_contact_by_name(first_name, last_name, {
                "first_name": new_first_name or None,
                "last_name": new_last_name or None,
                "phone_number": new_phone_number or None,
                "email": new_email or None,
                "address": new_address or None
            })

        
        elif choice == '7':  # Option 7: Delete a contact by name
            first_name = input("Enter the first name of the contact to delete: ")  # Get contact's first name
            last_name = input("Enter the last name of the contact to delete: ")  # Get contact's last name
            
            # First check if the contact exists before asking for confirmation
            contact_found = False
            for contact in phonebook.contacts:  # Loop through contacts to find a match
                if contact.first_name.lower() == first_name.lower() and contact.last_name.lower() == last_name.lower():
                    contact_found = True
                    break  # Stop searching once we find the contact

            if not contact_found:  # If no contact is found, print message and stop execution
                print(f"No contact found with the name {first_name} {last_name}.")
                continue  # Return to the menu
            
            # If contact exists, proceed with asking for confirmation to delete
            confirmation = input(f"Are you sure you want to delete {first_name} {last_name}? (yes/no): ").lower()
            if confirmation == 'yes':  # Confirm deletion
                phonebook.remove_contact_by_name(first_name, last_name)  # Remove contact from phonebook
            else:
                print("❌ Delete operation cancelled.")  # If user cancels deletion

        
        elif choice == '8':  # Option 8: Batch delete contacts from CSV
            csv_file = input("Enter the path to the CSV file for deleting contacts: ")  # Get CSV file path
            confirmation = input("Are you sure you want to delete contacts from the CSV file? (yes/no): ").lower()
            if confirmation == 'yes':  # Confirm batch deletion
                phonebook.batch_delete(csv_file)  # Delete contacts from the CSV file
            else:
                print("❌ Batch delete operation cancelled.")  # Cancel batch delete operation
        
        elif choice == '9':  # Option 9: Save and exit the program
            phonebook.save_to_file()  # Save contacts before exiting
            print("✅ Contacts saved. Exiting the program.")
            break  # Exit the loop and end the program
        
        else:
            print("❌ Invalid choice. Please try again.")  

if __name__ == "__main__":
    main()  
