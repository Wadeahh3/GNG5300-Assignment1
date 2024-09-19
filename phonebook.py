import csv
import os
import logging
import re
from datetime import datetime
from contact import Contact

# Set up logging configuration
logging.basicConfig(
    filename='phonebook.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class PhoneBook:
    def __init__(self):
        """
        Initialize the PhoneBook class with an empty list of contacts and set the filename for saving/loading contacts.
        """
        self.contacts = []  # List to store Contact objects
        self.filename = os.path.join(os.path.dirname(__file__), 'contacts.csv')  # Set the CSV file path

    def validate_phone_number(self, phone_number):
        """
        Validate the phone number to ensure it follows the format (###) ###-####
        :param phone_number: Phone number string
        :return: True if valid, False otherwise
        """
        pattern = r"\(\d{3}\) \d{3}-\d{4}"  # Regular expression for phone number format
        return re.fullmatch(pattern, phone_number) is not None

    def add_contact(self, contact):
        """
        Add a contact to the phonebook after validating the phone number.
        Automatically sort the contacts after adding a new one.
        :param contact: Contact object to be added
        """
        if not self.validate_phone_number(contact.phone_number):  # Validate phone number format
            print("Invalid phone number format. Please use (###) ###-####.")
            return  # If invalid, stop the function
        self.contacts.append(contact)  # Add contact to the list
        logging.info(f"Added contact: {contact.first_name} {contact.last_name}, Phone: {contact.phone_number}")
        
        # Automatically sort contacts by last name after adding
        self.sort_contacts(key="last_name")

    def sort_contacts(self, key="first_name"):
        """
        Sort contacts either by first name or last name.
        :param key: Sorting criterion (default is "first_name")
        """
        if key == "first_name":
            self.contacts = sorted(self.contacts, key=lambda contact: contact.first_name.lower())
        elif key == "last_name":
            self.contacts = sorted(self.contacts, key=lambda contact: contact.last_name.lower())
        logging.info(f"Contacts automatically sorted by {key}.")

    def remove_contact_by_name(self, first_name, last_name):
        """
        Remove a contact from the phonebook by matching first and last name.
        """
        original_count = len(self.contacts)  # Keep track of original contact count
        first_name, last_name = first_name.strip(), last_name.strip()  # Clean up input
        # Remove contacts that match the given first and last name
        self.contacts = [contact for contact in self.contacts if contact.first_name.strip().lower() != first_name.lower() or contact.last_name.strip().lower() != last_name.lower()]
        if len(self.contacts) < original_count:  # If a contact was removed
            logging.info(f"Removed contact: {first_name} {last_name}")
            print(f"Contact {first_name} {last_name} deleted successfully.")
        else:  # If no contact was removed
            logging.warning(f"Contact {first_name} {last_name} not found.")

    def batch_delete(self, csv_file):
        """
        Batch delete contacts by reading a CSV file that contains a list of first and last names.
        csv_file: Path to the CSV file for batch deletion
        """
        try:
            not_found_contacts = []  # List to track contacts that were not found
            with open(csv_file, newline='', encoding='utf-8') as file:
                reader = csv.reader(file)
                next(reader)  # Skip the header row (e.g., first_name, last_name, etc.)
                
                for row in reader:
                    if len(row) >= 2:
                        first_name, last_name = row[0].strip(), row[1].strip()  # Get first and last name from CSV
                        original_count = len(self.contacts)
                        self.remove_contact_by_name(first_name, last_name)  # Try to remove the contact
                        if len(self.contacts) == original_count:
                            not_found_contacts.append(f"{first_name} {last_name}")  # If not found, add to not_found list
                logging.info(f"Batch delete completed from {csv_file}")

            if not_found_contacts:  # If some contacts were not found
                print(f"The following contacts were not found and could not be deleted: {', '.join(not_found_contacts)}")
            else:  # All contacts deleted successfully
                print(f"Batch delete from {csv_file} completed successfully.")

        except FileNotFoundError:
            logging.error(f"File {csv_file} not found.")  # Log error if file not found
            print(f"File {csv_file} not found.")

    def batch_import(self, csv_file):
        """
        Batch import contacts from a CSV file and validate phone numbers.
        csv_file: Path to the CSV file for importing contacts
        """
        try:
            invalid_contacts = []  # List to record contacts with invalid phone numbers
            with open(csv_file, newline='', encoding='utf-8') as file:
                reader = csv.reader(file)
                for row in reader:
                    if len(row) >= 3:  # Ensure there are enough columns for first name, last name, and phone number
                        first_name, last_name, phone_number = row[0], row[1], row[2]
                        email = row[3] if len(row) > 3 else None
                        address = row[4] if len(row) > 4 else None
                        contact = Contact(first_name, last_name, phone_number, email, address)
                        if not self.validate_phone_number(phone_number):  # Validate phone number format
                            invalid_contacts.append(f"{first_name} {last_name}: {phone_number}")
                            continue  # Skip invalid contacts
                        self.add_contact(contact)  # Add valid contact
            if invalid_contacts:  # If some contacts had invalid phone numbers
                print(f"❌ The following contacts have invalid phone numbers and were not imported:")
                for contact in invalid_contacts:
                    print(contact)
            else:  # All contacts imported successfully
                print(f"✅ Batch import from {csv_file} completed successfully.")
            logging.info(f"Batch import from {csv_file} completed with {len(invalid_contacts)} invalid contacts.")
        except FileNotFoundError:
            logging.error(f"File {csv_file} not found.")
            print(f"❌ File {csv_file} not found.")

    def search_contact(self, query):
        """
        Search for contacts by first name, last name, or phone number.
        """
        query = query.strip().lower()  # Clean up and normalize search query
        result = [
            contact for contact in self.contacts
            if query in contact.first_name.lower() or
               query in contact.last_name.lower() or
               query in contact.phone_number
        ]
        logging.info(f"Searched for: {query}, Found: {len(result)} contact(s)")
        return result  # Return the list of matched contacts

    def filter_by_date(self, start_date, end_date):
        """
        Filter contacts by the date they were added to the phonebook.
        :return: List of contacts added within the specified date range
        """
        try:
            # Convert input strings to date objects
            start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
            end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
            result = []
            for contact in self.contacts:
                contact_created_at = contact.created_at.date()  # Get only the date part of created_at
                if start_date <= contact_created_at <= end_date:  # Check if within date range
                    result.append(contact)
            if result:  # If there are results
                print(f"📅 Found {len(result)} contact(s) in the given date range:")
                for contact in result:
                    print(contact)
            else:
                print(f"❌ No contacts found between {start_date} and {end_date}")
            logging.info(f"Filtered contacts from {start_date} to {end_date}, Found: {len(result)} contact(s)")
            return result
        except ValueError:  # If the date format is invalid
            print("❌ Invalid date format. Please enter dates in YYYY-MM-DD format.")
            return []

    def update_contact_by_name(self, first_name, last_name, new_contact_info):
        """
        Update contact information based on first and last name.

        """
        # Find the matching contact
        for contact in self.contacts:
            if contact.first_name.lower() == first_name.lower() and contact.last_name.lower() == last_name.lower():
                # Perform the update only if contact is found
                contact.update_contact(**new_contact_info)
                logging.info(f"Updated contact: {contact.first_name} {contact.last_name}")
                print(f"Contact {first_name} {last_name} updated successfully.")
                return
        
        # If no contact is found, print a message and stop further execution
        logging.warning(f"Tried to update contact but no contact found with name: {first_name} {last_name}")
        print(f"No contact found with the name {first_name} {last_name}.")



    def display_contacts(self):
        """
        Display all contacts in the phonebook.
        """
        if not self.contacts:  # If no contacts exist
            print("No contacts found.")
        for contact in self.contacts:  # Loop through and display all contacts
            print(contact)

    def save_to_file(self):
        """
        Save all contacts to the CSV file.
        """
        with open(self.filename, 'w', newline='') as file:  # Open CSV file for writing
            writer = csv.writer(file)
            for contact in self.contacts:  # Write each contact's details as a new row
                writer.writerow([contact.first_name, contact.last_name, contact.phone_number, contact.email, contact.address])
        logging.info("Contacts saved to file.")  # Log that contacts were saved

    def load_from_file(self):
        """
        Load contacts from the CSV file into the phonebook.
        """
        try:
            with open(self.filename, 'r') as file:  # Open CSV file for reading
                reader = csv.reader(file)
                for row in reader:
                    if len(row) >= 3:  # Ensure row has at least first name, last name, and phone number
                        contact = Contact(row[0], row[1], row[2], email=row[3] if len(row) > 3 else None, address=row[4] if len(row) > 4 else None)
                        self.add_contact(contact)  # Add contact to phonebook
            logging.info("Contacts loaded from file.")  # Log that contacts were loaded
        except FileNotFoundError:  # If the CSV file is not found
            logging.warning(f"No contacts found in {self.filename}. Starting with an empty phone book.")
            print(f"No contacts found in {self.filename}. Starting with an empty phone book.")  # Print message to user

