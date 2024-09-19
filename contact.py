from datetime import datetime

class Contact:
    def __init__(self, first_name, last_name, phone_number, email=None, address=None):
        """
        Creat a Contact object with first name, last name, phone number, and email and address(optional).
        The creation and update timestamps are set to the current time.
        
        """
        self.first_name = first_name  
        self.last_name = last_name  
        self.phone_number = phone_number  
        self.email = email  
        self.address = address  
        self.created_at = datetime.now()  
        self.updated_at = datetime.now()  

    def update_contact(self, first_name=None, last_name=None, phone_number=None, email=None, address=None):
        """
        The updated_at timestamp is set to the current time whenever any field is updated.
        
        """
        if first_name:  # If a new first name is provided, update it
            self.first_name = first_name
        if last_name:  # If a new last name is provided, update it
            self.last_name = last_name
        if phone_number:  # If a new phone number is provided, update it
            self.phone_number = phone_number
        if email:  # If a new email address is provided, update it
            self.email = email
        if address:  # If a new physical address is provided, update it
            self.address = address
        self.updated_at = datetime.now()  # Update the last updated timestamp

    def __str__(self):
        """
        Return a string representation of the contact, displaying the contact's name, phone number, 
        email, and address. If email or address is not provided, show 'N/A'.
        
        :return: A formatted string representing the contact's details.
        """
        return f"{self.first_name} {self.last_name}: {self.phone_number} | Email: {self.email or 'N/A'} | Address: {self.address or 'N/A'}"
