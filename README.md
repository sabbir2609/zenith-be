# ZenithReserve - Hotel Management System

ZenithReserve is a robust Hotel Management System developed using Django Rest Framework. It provides a comprehensive solution for managing hotel properties, reservations, billing, and more.

## Features

- **User Authentication and Authorization:**
  - User registration and login with role-based access control.
  - Single sign-on integration with Google.

- **Dashboard:**
  - Overview of key metrics, including occupancy, revenue, and check-ins/check-outs.
  - Quick access to important functionalities.

- **Property Management:**
  - Add, edit, and remove hotel properties.
  - Manage room inventory, types, and rates.

- **Reservation Management:**
  - Search for availability based on dates, room type, etc.
  - Create, modify, and cancel reservations.

- **Check-In and Check-Out:**
  - Efficient check-in and check-out processes.
  - Room assignment based on availability and guest preferences.

- **Billing and Invoicing:**
  - Generate invoices for room charges, services, and amenities.
  - Support for multiple payment methods (credit card, cash, etc.).

- **Online Booking Engine:**
  - User-friendly interface for guests to make online reservations.
  - Real-time availability updates with payment gateway integration.

- **Channel Management:**
  - Integration with third-party booking platforms (e.g., Booking.com, Expedia).
  - Synchronize availability and rates across channels.

- **Housekeeping Management:**
  - Track room cleaning status and assign cleaning tasks to staff.

- **Inventory and Supplies Management:**
  - Track and manage hotel supplies with alerts for low inventory levels.

- **Reporting and Analytics:**
  - Generate reports on occupancy rates, revenue, and more.
  - Visualize data for insights and decision-making.

- **Subscription Management:**
  - Admin panel to manage subscription plans with billing and renewal automation.

- **Multi-language and Multi-currency Support:**
  - Provide a seamless experience for users across different languages and currencies.


## Getting Started

To get started with the project, follow these steps:

1. **Clone the repository**

   Use the following command to clone the repository:

   ```bash
   git clone https://github.com/sabbir2609/zenith-fe.git
   ```

2. **Navigate into the project directory**

   Use the following command to navigate into the project directory:

   ```bash
   cd zenith-fe
   ```

3. **Create a virtual environment**

   Use the following command to create a virtual environment:

   ```bash
   python3 -m venv venv
   ```

4. **Activate the virtual environment**

   On Windows, use the following command to activate the virtual environment:

   ```bash
   .\venv\Scripts\activate
   ```

   On Unix or MacOS, use the following command to activate the virtual environment:

   ```bash
   source venv/bin/activate
   ```

5. **Install the required dependencies**

   Use the following command to install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

6. **Apply the migrations**

   Use the following command to apply the migrations:

   ```bash
   python manage.py migrate
   ```

7. **Run the server**

   Use the following command to run the server:

   ```bash
   python manage.py runserver
   ```

Now, you should be able to access the application at `http://localhost:8000/`.


## Technology Stack

![Python](https://img.shields.io/badge/-Python-333333?style=flat&logo=python)
![Django](https://img.shields.io/badge/-Django-333333?style=flat&logo=django)
![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-333333?style=flat&logo=postgresql)
![Docker](https://img.shields.io/badge/-Docker-333333?style=flat&logo=docker)
![GitHub](https://img.shields.io/badge/-GitHub-333333?style=flat&logo=github)
![Redis](https://img.shields.io/badge/-Redis-333333?style=flat&logo=redis)
![MQTT](https://img.shields.io/badge/-MQTT-333333?style=flat&logo=mqtt)
![Django Rest Framework](https://img.shields.io/badge/-Django%20Rest%20Framework-333333?style=flat)
![Celery](https://img.shields.io/badge/-Celery-333333?style=flat&logo=celery)



## Resources

For more information, see the [Instruction Manual](resource/Instruction.md).

## License

This project is licensed under the terms of the [MIT License](LICENSE).
