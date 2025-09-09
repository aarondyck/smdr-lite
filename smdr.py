import socket
import csv
import sys
import os
import argparse
import datetime
import msvcrt
import time
import io

def print_status(port, filename, record_count, last_received_time):
    """
    Prints the current status of the server to the console.
    """
    os.system('cls')  # Clear the console screen
    print("Bovaird SMDR Collector Lite")
    print("Press 'Q' to quit")
    print("-" * 30)
    print(f"Records Received: {record_count}")
    print(f"Listening Port: {port}")
    print(f"Output File: {filename}")
    print(f"Last Record Received: {last_received_time}")
    print("-" * 30)
    print("Waiting for data...")

def run_server(port, filename):
    """
    Sets up a TCP server to listen for incoming data and writes it to a CSV file.
    
    Args:
        port (int): The port number to listen on.
        filename (str): The name of the CSV file to write to.
    """
    
    # Create a TCP/IP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # The empty string means the server will listen on all available
    # network interfaces.
    server_address = ('', port)
    
    # Initialize record counter and last received time
    record_count = 0
    last_received_time = "N/A"
    
    try:
        # Bind the socket to the port
        server_socket.bind(server_address)
        
        # Listen for incoming connections (up to 1)
        server_socket.listen(1)
        
        # Set a timeout so we can periodically check for user input
        server_socket.settimeout(0.5)
        
        # Open the CSV file in append mode.
        with open(filename, 'a', newline='') as csvfile:
            data_writer = csv.writer(csvfile)
            
            # Check if the file exists and has a header
            file_exists = os.path.exists(filename) and os.path.getsize(filename) > 0

            # Write a header row if the file is new or empty
            if not file_exists:
                header_row = [
                    "Call Start Time", "Connected Time", "Ring Time", "Caller", "Direction",
                    "Called Number", "Dialed Number", "Account Code", "Is Internal", "Call ID",
                    "Continuation", "Party1 Device", "Party1 Name", "Party2 Device", "Party2 Name",
                    "Hold Time", "Park Time", "Authorization Valid", "Authorization Code",
                    "User Charged", "Call Charge", "Currency", "Amount at Last User Change",
                    "Call Units", "Units at Last User Change", "Cost per Unit", "Mark Up",
                    "External Targeting Cause", "External Targeter ID", "Calling Party Server IP Address",
                    "Unique Call ID for the Caller Extension", "Called Party Server IP Address",
                    "Unique Call ID for the Called Extension", "SMDR Record Time", "Caller Consent Directive",
                    "Calling Number Verification"
                ]
                data_writer.writerow(header_row)

            # Initial status print
            print_status(port, filename, record_count, last_received_time)
            
            while True:
                # Check for keyboard input before waiting for a connection
                if msvcrt.kbhit():
                    key = msvcrt.getch()
                    if key in (b'q', b'Q'):
                        print("\n'q' key pressed. Shutting down...")
                        break

                # Wait for a connection
                try:
                    connection, client_address = server_socket.accept()
                    
                    try:
                        # Set a timeout on the connection itself to handle streams
                        connection.settimeout(1.0)
                        
                        buffer = b''
                        while True:
                            chunk = connection.recv(1)
                            if not chunk:
                                break  # Connection closed
                            
                            buffer += chunk
                            
                            # Check for a newline character to mark the end of a record
                            if b'\n' in buffer:
                                received_string = buffer.decode('utf-8', errors='ignore').strip()
                                
                                # Process the received string
                                if received_string:
                                    # Use StringIO to treat the string as a file and parse with csv.reader
                                    try:
                                        sio = io.StringIO(received_string)
                                        reader = csv.reader(sio)
                                        
                                        # Get the parsed row (there should be only one)
                                        parsed_row = next(reader)
                                        
                                        # Write the parsed row to the output file
                                        data_writer.writerow(parsed_row)
                                        
                                        # Update record count and last received time, and refresh display
                                        record_count += 1
                                        last_received_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                        print_status(port, filename, record_count, last_received_time)
                                    except csv.Error as e:
                                        # Handle malformed CSV data gracefully
                                        print(f"Skipping malformed CSV record: {e}")

                                buffer = b''  # Reset the buffer for the next record
                                
                    except socket.timeout:
                        # Connection timed out, but keep listening for new records.
                        pass
                        
                    finally:
                        # Clean up the connection
                        connection.close()
                
                except socket.timeout:
                    # No connection received, loop continues to check for 'q'
                    pass
                    
    except socket.error as e:
        print(f"\nSocket error: {e}")
        print("This may be due to the port already in use or lack of permissions.")
        print(f"Please check if another program is using port {port}.")
        
    except KeyboardInterrupt:
        print("\nServer shutting down.")
        
    finally:
        # Close the server socket
        server_socket.close()

def main():
    """
    Parses command-line arguments and runs the server.
    """
    parser = argparse.ArgumentParser(description='A simple TCP data collector that saves data to a CSV file.')
    parser.add_argument(
        '--port', 
        type=int, 
        default=5000, 
        help='The TCP port to listen on. (Default: 5000)'
    )
    parser.add_argument(
        '--filename',
        type=str,
        default='smdr.csv',
        help='The name of the CSV file to write to. (Default: smdr.csv)'
    )
    
    args = parser.parse_args()
    run_server(args.port, args.filename)

if __name__ == "__main__":
    main()
