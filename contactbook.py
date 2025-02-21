import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk  # Ensure you have pillow installed using 'pip install pillow'
import json

# Function to load contacts from a file
def load_contacts():
    try:
        with open("contacts.json", "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

# Function to save contacts to a file
def save_contacts():
    with open("contacts.json", "w") as file:
        json.dump(contacts, file, indent=4)

# Function to add a new contact
def add_contact():
    name = name_entry.get().strip()
    phone = phone_entry.get().strip()
    address = address_entry.get().strip()
    
    if not name or not phone or not address:
        messagebox.showwarning("Input Error", "Please fill in all fields.")
        return

    if name in contacts:
        messagebox.showerror("Duplicate Error", "Contact already exists.")
        return
    
    contacts[name] = {"phone": phone, "address": address}
    save_contacts()
    update_contact_list()
    clear_entries()
    messagebox.showinfo("Success", f"Contact {name} added.")

# Function to edit an existing contact
def edit_contact():
    selected_name = contact_listbox.get(tk.ACTIVE)
    new_name = name_entry.get().strip()
    new_phone = phone_entry.get().strip()
    new_address = address_entry.get().strip()
    
    if not new_name or not new_phone or not new_address:
        messagebox.showwarning("Input Error", "Please fill in all fields.")
        return

    if selected_name in contacts:
        del contacts[selected_name]
        contacts[new_name] = {"phone": new_phone, "address": new_address}
        save_contacts()
        update_contact_list()
        clear_entries()
        messagebox.showinfo("Success", f"Contact {selected_name} updated.")
    else:
        messagebox.showwarning("Selection Error", "Please select a contact to edit.")

# Function to delete a contact
def delete_contact():
    selected_name = contact_listbox.get(tk.ACTIVE)
    if selected_name in contacts:
        del contacts[selected_name]
        save_contacts()
        update_contact_list()
        clear_entries()
        messagebox.showinfo("Success", f"Contact {selected_name} deleted.")
    else:
        messagebox.showwarning("Selection Error", "Please select a contact to delete.")

# Function to update the contact list in the listbox
def update_contact_list(search_term=""):
    contact_listbox.delete(0, tk.END)
    for name, details in contacts.items():
        # Display only names in the listbox
        if search_term.lower() in name.lower() or search_term in details["phone"] or search_term.lower() in details["address"].lower():
            contact_listbox.insert(tk.END, name)

# Function to search contacts
def search_contacts():
    search_term = search_entry.get().strip()
    update_contact_list(search_term)
    # Automatically display the details of the first match in the search results
    if contact_listbox.size() > 0:
        contact_listbox.selection_set(0)
        show_contact_details(None)

# Function to display contact details
def show_contact_details(event):
    selected = contact_listbox.get(tk.ACTIVE)
    if selected:
        try:
            # Get the contact details using the selected name
            details = contacts[selected]
            phone = details['phone']
            address = details['address']
            name_entry.delete(0, tk.END)
            name_entry.insert(tk.END, selected)
            phone_entry.delete(0, tk.END)
            phone_entry.insert(tk.END, phone)
            address_entry.delete(0, tk.END)
            address_entry.insert(tk.END, address)
        except KeyError:
            messagebox.showwarning("Error", "Selected contact is not found.")

# Function to clear entry fields
def clear_entries():
    name_entry.delete(0, tk.END)
    phone_entry.delete(0, tk.END)
    address_entry.delete(0, tk.END)
    search_entry.delete(0, tk.END)

# Function to view all contacts in a separate window
def view_all_contacts():
    all_contacts_window = tk.Toplevel(root)
    all_contacts_window.title("All Contacts")

    # Create a frame for the table layout
    table_frame = tk.Frame(all_contacts_window)
    table_frame.pack(padx=10, pady=10)

    # Create column headers with a unique color scheme 
    headers = ["Name", "Phone", "Address"]
    for col, header in enumerate(headers):
        header_label = tk.Label(table_frame, text=header, font=("Arial", 12, "bold"), borderwidth=1, relief="solid", width=25, bg="#dcdcdc")
        header_label.grid(row=0, column=col, padx=1, pady=1)

    # Populate the table with contacts
    for row, (name, details) in enumerate(contacts.items(), start=1):
        bg_color = "#f0f0f0" if row % 2 == 0 else "#ffffff"  # Alternating row colors
        tk.Label(table_frame, text=name, borderwidth=1, relief="solid", width=20, bg=bg_color).grid(row=row, column=0, padx=1, pady=1)
        tk.Label(table_frame, text=details.get("phone", ""), borderwidth=1, relief="solid", width=30, bg=bg_color).grid(row=row, column=1, padx=1, pady=1)
        tk.Label(table_frame, text=details.get("address", ""), borderwidth=1, relief="solid", width=30, bg=bg_color).grid(row=row, column=2, padx=1, pady=1)

# Function to exit the application
def exit_application():
    root.destroy()

# Setting up the main window
root = tk.Tk()
root.title("Contact Book")
root.geometry("500x700")  # Increased height to accommodate the image
root.config(bg="#f8f8f8")  # Light grey background

# Load existing contacts
contacts = load_contacts()

# Load icons
name_icon = ImageTk.PhotoImage(Image.open("name.png").resize((20, 20), Image.LANCZOS))
phone_icon = ImageTk.PhotoImage(Image.open("phone.png").resize((20, 20), Image.LANCZOS))
address_icon = ImageTk.PhotoImage(Image.open("address.png").resize((20, 20), Image.LANCZOS))
search_icon = ImageTk.PhotoImage(Image.open("search.png").resize((20, 20), Image.LANCZOS))

# Load the contact book image
contact_book_image = Image.open("contact book image.png")  # Replace with your image file
contact_book_image = contact_book_image.resize((250, 150), Image.LANCZOS)  # Resize as needed
contact_book_photo = ImageTk.PhotoImage(contact_book_image)

# Setting up the GUI elements
frame = tk.Frame(root, bg="#f8f8f8")
frame.pack(pady=10)

# Add image label
image_label = tk.Label(frame, image=contact_book_photo, bg="#f8f8f8")
image_label.grid(row=0, column=0, columnspan=2)

# Heading
heading_label = tk.Label(frame, text="Contact Book", bg="#f8f8f8", fg="#4a4a4a", font=("Arial", 24, "bold"))
heading_label.grid(row=1, column=0, columnspan=2, pady=10)

# Reorder the input fields
name_label = tk.Label(frame, text="Name", bg="#f8f8f8", fg="#333333", font=("Arial", 12), image=name_icon, compound="left")
name_label.grid(row=2, column=0, sticky='w', padx=5)
name_entry = tk.Entry(frame, width=25, font=("Arial", 12))
name_entry.grid(row=2, column=1, pady=5)

phone_label = tk.Label(frame, text="Phone", bg="#f8f8f8", fg="#333333", font=("Arial", 12), image=phone_icon, compound="left")
phone_label.grid(row=3, column=0, sticky='w', padx=5)
phone_entry = tk.Entry(frame, width=25, font=("Arial", 12))
phone_entry.grid(row=3, column=1, pady=5)

address_label = tk.Label(frame, text="Address", bg="#f8f8f8", fg="#333333", font=("Arial", 12), image=address_icon, compound="left")
address_label.grid(row=4, column=0, sticky='w', padx=5)
address_entry = tk.Entry(frame, width=25, font=("Arial", 12))
address_entry.grid(row=4, column=1, pady=5)

search_label = tk.Label(frame, text="Search", bg="#f8f8f8", fg="#333333", font=("Arial", 12), image=search_icon, compound="left")
search_label.grid(row=5, column=0, sticky='w', padx=5)

search_entry = tk.Entry(frame, width=25, font=("Arial", 12))
search_entry.grid(row=5, column=1, pady=5)

search_button = tk.Button(frame, text="Search Contact", command=search_contacts, bg="#5bc0de", fg="#ffffff", font=("Arial", 12, "bold"))
search_button.grid(row=6, column=0, columnspan=2, pady=5, sticky='ew', padx=5)

# Place all action buttons in the same row
button_frame = tk.Frame(frame, bg="#f8f8f8")
button_frame.grid(row=7, column=0, columnspan=2, pady=10, sticky='ew')

common_button_color = "#5cb85c"  # Common button color for other buttons

add_button = tk.Button(button_frame, text="Add", command=add_contact, bg=common_button_color, fg="#ffffff", font=("Arial", 12, "bold"))
add_button.pack(side="left", fill="x", expand=True, padx=5)

edit_button = tk.Button(button_frame, text="Edit", command=edit_contact, bg=common_button_color, fg="#ffffff", font=("Arial", 12, "bold"))
edit_button.pack(side="left", fill="x", expand=True, padx=5)

delete_button = tk.Button(button_frame, text="Delete", command=delete_contact, bg=common_button_color, fg="#ffffff", font=("Arial", 12, "bold"))
delete_button.pack(side="left", fill="x", expand=True, padx=5)

view_all_button = tk.Button(button_frame, text="View All", command=view_all_contacts, bg=common_button_color, fg="#ffffff", font=("Arial", 12, "bold"))
view_all_button.pack(side="left", fill="x", expand=True, padx=5)

# Adding the contact listbox
contact_listbox = tk.Listbox(root, width=50, height=10, bg="#ffffff", selectbackground="#4a90e2", selectforeground="#ffffff", font=("Arial", 12))
contact_listbox.pack(pady=10)
contact_listbox.bind('<<ListboxSelect>>', show_contact_details)

# Adding the exit button in a smaller size
exit_button_frame = tk.Frame(root, bg="#f8f8f8")
exit_button_frame.pack(pady=10, fill='x')

exit_button = tk.Button(exit_button_frame, text="Exit", command=exit_application, bg="#d9534f", fg="#ffffff", font=("Arial", 10, "bold"), width=10)
exit_button.pack(padx=5, pady=5)

update_contact_list()

root.mainloop()
