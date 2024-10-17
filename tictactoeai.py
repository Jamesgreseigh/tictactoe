import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk  # Import PIL for image handling
import random

# Global variables
player_turn = "X"
buttons = []
game_active = True
player1_name = "Player 1"
player2_name = "Player 2"
is_playing_against_ai = False  # Variable to track if playing against AI

# Function to check if a player has won
def check_winner():
    global game_active
    for row in range(3):
        if buttons[row][0]["text"] == buttons[row][1]["text"] == buttons[row][2]["text"] != "":
            game_active = False
            return buttons[row][0]["text"]
    
    for col in range(3):
        if buttons[0][col]["text"] == buttons[1][col]["text"] == buttons[2][col]["text"] != "":
            game_active = False
            return buttons[0][col]["text"]
    
    if buttons[0][0]["text"] == buttons[1][1]["text"] == buttons[2][2]["text"] != "":
        game_active = False
        return buttons[0][0]["text"]
    
    if buttons[0][2]["text"] == buttons[1][1]["text"] == buttons[2][0]["text"] != "":
        game_active = False
        return buttons[0][2]["text"]
    
    return None

# Function to handle AI moves with a delay
def ai_move():
    global player_turn
    if player_turn == "O" and game_active:  # AI plays when it's "O"'s turn
        available_moves = [(r, c) for r in range(3) for c in range(3) if buttons[r][c]["text"] == ""]
        if available_moves:
            # Schedule the AI move after a 2-second delay
            tic_tac_toe_window.after(2000, make_ai_move)

def make_ai_move():
    global player_turn
    available_moves = [(r, c) for r in range(3) for c in range(3) if buttons[r][c]["text"] == ""]
    if available_moves:
        row, col = random.choice(available_moves)  # Choose a random available move
        button_click(row, col)  # Call button_click to make the move

# Function to handle button click
def button_click(row, col):
    global player_turn
    if buttons[row][col]["text"] == "" and game_active:
        buttons[row][col]["text"] = player_turn
        buttons[row][col].config(fg="blue" if player_turn == "X" else "red")  # Set colour based on player
        
        winner = check_winner()
        if winner:
            celebrate_winner(winner)  # Call the celebration function
            disable_buttons()
        elif all(buttons[r][c]["text"] != "" for r in range(3) for c in range(3)):
            messagebox.showinfo("Game Over", "It's a draw!")
            disable_buttons()
        else:
            player_turn = "O" if player_turn == "X" else "X"
            if player_turn == "O" and is_playing_against_ai:  # If next turn is AI's
                ai_move()  # Call AI move

# Function to celebrate the winner
def celebrate_winner(winner):
    if winner == "O":  # If AI wins
        tic_tac_toe_window.configure(bg="red")  # Change background to red
        messagebox.showinfo("Game Over", f"{player2_name} won! Better luck next time!")
    else:  # If player wins
        tic_tac_toe_window.configure(bg="yellow")  # Change background to yellow for player win
        messagebox.showinfo("Congratulations!", f"{player1_name} wins! 🎉")

# Function to disable all buttons after the game ends
def disable_buttons():
    for row in range(3):
        for col in range(3):
            buttons[row][col]["state"] = "disabled"

# Function to reset the game
def reset_game():
    global player_turn, game_active
    player_turn = "X"
    game_active = True
    for row in range(3):
        for col in range(3):
            buttons[row][col]["text"] = ""
            buttons[row][col]["state"] = "normal"
    tic_tac_toe_window.configure(bg="#7c2181")  # Reset background colour

# Function to create the Tic-Tac-Toe grid
def create_tic_tac_toe():
    global buttons, tic_tac_toe_window
    tic_tac_toe_window = tk.Toplevel()  # Create a new window for Tic-Tac-Toe
    tic_tac_toe_window.title("Tic-Tac-Toe")
    tic_tac_toe_window.geometry("500x500")
    tic_tac_toe_window.configure(bg="#7c2181")  # Set the background colour to purple

    # Create the Tic-Tac-Toe grid
    buttons = []  # Reset the buttons list
    for row in range(3):
        button_row = []
        for col in range(3):
            frame = tk.Frame(tic_tac_toe_window, bg="#7c2181", bd=2)  # Frame background
            frame.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")

            button = tk.Button(frame, text="", font=("Arial", 40), width=5, height=2,
                               bg="#6b196f",  # Button background colour
                               command=lambda row=row, col=col: button_click(row, col))
            button.pack(fill=tk.BOTH, expand=True)
            button_row.append(button)
        buttons.append(button_row)

    # Add a Reset button on the left
    reset_button = tk.Button(tic_tac_toe_window, text="Reset", font=("Arial", 15), command=reset_game, bg="#6b196f", fg="white")
    reset_button.grid(row=3, column=0, pady=10, sticky="w")

    # Add a Main Menu button on the right
    main_menu_button = tk.Button(tic_tac_toe_window, text="Main Menu", font=("Arial", 15), command=return_to_main_menu, bg="#6b196f", fg="white")
    main_menu_button.grid(row=3, column=2, pady=10, sticky="e")

    # Configure grid weights to ensure proper resizing
    for i in range(3):
        tic_tac_toe_window.grid_columnconfigure(i, weight=1)
        tic_tac_toe_window.grid_rowconfigure(i, weight=1)

# Function to return to the main menu
def return_to_main_menu():
    tic_tac_toe_window.destroy()  # Close the Tic-Tac-Toe window

def main_menu():
    global root, player1_entry, player2_entry
    root = tk.Tk()  # Create the main window
    root.title("Main Menu")
    root.geometry("600x450")
    root.configure(bg="#7c2181")  # Set main menu background colour to match the game

    # Load the background image (optional, comment out if you don't want it)
    # bg_image = Image.open(r"C:\Users\radie\Downloads\West-Downs-Centre-exterior-1 (1).jpg")  # Use raw string for path
    # bg_image = bg_image.resize((1920, 1080), Image.LANCZOS)  # Resize the image to fit the window
    # bg_photo = ImageTk.PhotoImage(bg_image)

    # Create a label with the background image (optional)
    # bg_label = tk.Label(root, image=bg_photo)
    # bg_label.place(relwidth=1, relheight=1)  # Make the label fill the window

    # Create a label for the main menu with a clean font
    label = tk.Label(root, text="Welcome to Tic-Tac-Toe", font=("Arial", 36, "bold"), fg="white", bg="#7c2181")  # Adjusted font
    label.pack(pady=20)

    # Create entry fields for player names with bold text
    tk.Label(root, text="Player 1 Name:", font=("Arial", 18), fg="white", bg="#7c2181").pack(pady=5)
    player1_entry = tk.Entry(root, font=("Arial", 18))
    player1_entry.pack(pady=5)

    tk.Label(root, text="Player 2 Name (or AI):", font=("Arial", 18), fg="white", bg="#7c2181").pack(pady=5)
    player2_entry = tk.Entry(root, font=("Arial", 18))
    player2_entry.pack(pady=5)

    # Create a "Play Now" button with a clean font
    play_button = tk.Button(root, text="Play Now (2 Player)", font=("Arial", 20, "bold"), command=start_game, 
                            bg="#6b196f", fg="white", relief="flat", 
                            highlightbackground="#7c2181", highlightthickness=0)  # No highlight border
    play_button.pack(pady=10)

    # Create a "Play Against AI" button with a clean font
    play_ai_button = tk.Button(root, text="Play Against AI", font=("Arial", 20, "bold"), command=start_game_ai, 
                                bg="#6b196f", fg="white", relief="flat", 
                                highlightbackground="#7c2181", highlightthickness=0)  # No highlight border
    play_ai_button.pack(pady=10)

    root.mainloop()  # Start the main event loop

# Function to start a 2-player game
def start_game():
    global player1_name, player2_name, is_playing_against_ai
    player1_name = player1_entry.get() or "Player 1"  # Default name if empty
    player2_name = player2_entry.get() or "Player 2"  # Default name if empty
    is_playing_against_ai = False  # Set to false for 2-player game
    create_tic_tac_toe()  # Create the game

# Function to start a game against AI
def start_game_ai():
    global player1_name, player2_name, is_playing_against_ai
    player1_name = player1_entry.get() or "Player 1"  # Default name if empty
    player2_name = player2_entry.get() or "Player 2"  # Default name for empty
    is_playing_against_ai = True  # Set to true for AI game
    create_tic_tac_toe()  # Create the game

# Run the main menu function to start the application
main_menu()
