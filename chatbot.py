import tkinter as tk
from tkinter import ttk
import pandas as pd
from decimal import Decimal

# Load the data from the provided CSV file
data_file = "C:/Users/thoma/Downloads/goflow2_sample_output.csv"  # Ensure this is the correct path to your CSV
data = pd.read_csv(data_file)

# Caterpillar color theme
CAT_YELLOW = "#FFCC00"
CAT_BLACK = "#1C1C1C"
CAT_GRAY = "#A9A9A9"


def create_main_window():
    """Sets up and runs the main application window with Caterpillar Inc. color theme."""
    root = tk.Tk()
    root.title("Network Stats Chatbot - Caterpillar Inc.")
    root.geometry("400x400")
    root.configure(bg=CAT_BLACK)

    # Apply custom style
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("TLabel", background=CAT_BLACK, foreground=CAT_YELLOW)
    style.configure("TCombobox", background=CAT_GRAY, foreground=CAT_BLACK)
    style.configure("TButton", background=CAT_YELLOW, foreground=CAT_BLACK)

    # Chat history display
    chat_history = tk.Text(root, wrap="word", state=tk.DISABLED, width=50, height=15, bg=CAT_BLACK, fg=CAT_YELLOW)
    chat_history.pack(pady=10)

    # Dropdown menu for preset questions
    question_var = tk.StringVar(value="Select an option")
    questions_layer_1 = [
        "Select an option",
        "Utilization percentage",
        "Top Volume (Bytes)",
        "Top Flows today"
    ]
    question_menu = ttk.Combobox(root, textvariable=question_var, values=questions_layer_1, state="readonly",
                                 style="TCombobox")
    question_menu.pack(pady=10)

    # Button to get response
    response_button = ttk.Button(root, text="Get Info", style="TButton",
                                 command=lambda: handle_user_input(question_var, chat_history, root))
    response_button.pack(pady=10)

    root.mainloop()


def handle_user_input(question_var, chat_history, root):
    """Processes the selected question and opens a new window with information as needed."""
    user_input = question_var.get()
    if user_input == "Select an option":
        response = "Please select a valid option."
        display_response(user_input, response, chat_history)
    elif user_input == "Utilization percentage":
        open_utilization_threshold_window(root)
    elif user_input == "Top Volume (Bytes)":
        open_top_volume_input_window(root)
    elif user_input == "Top Flows today":
        open_top_flows_input_window(root)


def display_response(user_input, response, chat_history):
    """Displays the user input and chatbot response in the chat history."""
    chat_history.config(state=tk.NORMAL)
    chat_history.insert(tk.END, f"You: {user_input}\nBot: {response}\n\n")
    chat_history.config(state=tk.DISABLED)
    chat_history.see(tk.END)


def open_utilization_threshold_window(root):
    """Opens a new window for entering a utilization threshold."""
    new_window = tk.Toplevel(root)
    new_window.geometry("400x400")
    new_window.title("Utilization Threshold")
    new_window.configure(bg=CAT_BLACK)

    label = tk.Label(new_window, text="Enter a utilization percentage threshold:", bg=CAT_BLACK, fg=CAT_YELLOW,
                     wraplength=350)
    label.pack(pady=10)

    threshold_entry = tk.Entry(new_window, bg=CAT_GRAY, fg=CAT_BLACK)
    threshold_entry.pack(pady=10)

    submit_button = ttk.Button(new_window, text="Submit", style="TButton",
                               command=lambda: display_utilization_over_threshold(new_window, threshold_entry))
    submit_button.pack(pady=10)


def display_utilization_over_threshold(window, threshold_entry):
    """Displays networks over the entered utilization threshold from the CSV data."""
    threshold = float(threshold_entry.get())
    window.destroy()

    result_window = tk.Toplevel()
    result_window.geometry("400x400")
    result_window.title("Networks Over Utilization Threshold")
    result_window.configure(bg=CAT_BLACK)
    data['time_elapsed'] = 0
    for index, row in data.iterrows():
        data.loc[index, 'time_elapsed'] = float(data.iloc[index]['time_flow_end_ns']) - float(data.iloc[index]['time_flow_start_ns'] )
    data['bps'] = (data['bytes'] * 8) / (data['time_elapsed'] / 10 ** 9)
    data['util_perc'] = data['bps'] / 10**9 * 100
    new_data = data.groupby('src_addr', as_index=False)['util_perc'].sum()
    print(new_data)
    filtered_data = new_data[new_data['util_perc'] > threshold]
   # print(float(1729276399355000000) - float(1729276231969000000))
    label = tk.Label(result_window, text=f"Networks with utilization over {threshold} %:", bg=CAT_BLACK,
                     fg=CAT_YELLOW, wraplength=350)
    label.pack(pady=10)

    for index, row in filtered_data.iterrows():
        network_label = tk.Label(result_window, text=f"Src Addr: {row['src_addr']} - util percentage: {row['util_perc']}",
                                 bg=CAT_BLACK, fg=CAT_YELLOW)
        network_label.pack()

    close_button = ttk.Button(result_window, text="Close", style="TButton", command=result_window.destroy)
    close_button.pack(pady=10)


def open_top_volume_input_window(root):
    """Opens a new window for entering the number of top volumes to display."""
    new_window = tk.Toplevel(root)
    new_window.geometry("400x400")
    new_window.title("Top Volume (Bytes)")
    new_window.configure(bg=CAT_BLACK)

    label = tk.Label(new_window, text="Enter the number of top volumes to display:", bg=CAT_BLACK, fg=CAT_YELLOW,
                     wraplength=350)
    label.pack(pady=10)

    volume_entry = tk.Entry(new_window, bg=CAT_GRAY, fg=CAT_BLACK)
    volume_entry.pack(pady=10)

    submit_button = ttk.Button(new_window, text="Submit", style="TButton",
                               command=lambda: display_top_volume(new_window, volume_entry))
    submit_button.pack(pady=10)


def display_top_volume(window, volume_entry):
    """Displays the top N volumes based on user input from the CSV data."""
    top_n = int(volume_entry.get())
    window.destroy()

    result_window = tk.Toplevel()
    result_window.geometry("400x400")
    result_window.title("Top Volume Networks")
    result_window.configure(bg=CAT_BLACK)

    total_bytes = data.groupby('src_addr', as_index = False)['bytes'].sum()
    top_volumes = total_bytes.nlargest(top_n, 'bytes')[['src_addr', 'bytes']]
    print(top_volumes)
    label = tk.Label(result_window, text=f"Top {top_n} networks by volume (Bytes):", bg=CAT_BLACK, fg=CAT_YELLOW,
                     wraplength=350)
    label.pack(pady=10)

    for index, row in top_volumes.iterrows():
        volume_label = tk.Label(result_window, text=f"Src Addr: {row['src_addr']} - Bytes: {row['bytes']}",
                                bg=CAT_BLACK, fg=CAT_YELLOW)
        volume_label.pack()

    close_button = ttk.Button(result_window, text="Close", style="TButton", command=result_window.destroy)
    close_button.pack(pady=10)


def open_top_flows_input_window(root):
    """Opens a new window for entering the number of top flows to display."""
    new_window = tk.Toplevel(root)
    new_window.geometry("400x400")
    new_window.title("Top Flows Today")
    new_window.configure(bg=CAT_BLACK)

    label = tk.Label(new_window, text="Enter the number of top flows to display:", bg=CAT_BLACK, fg=CAT_YELLOW,
                     wraplength=350)
    label.pack(pady=10)

    flows_entry = tk.Entry(new_window, bg=CAT_GRAY, fg=CAT_BLACK)
    flows_entry.pack(pady=10)

    submit_button = ttk.Button(new_window, text="Submit", style="TButton",
                               command=lambda: display_top_flows(new_window, flows_entry))
    submit_button.pack(pady=10)


def display_top_flows(window, flows_entry):
    """Displays the top N flows based on user input from the CSV data."""
    top_n = int(flows_entry.get())
    window.destroy()

    result_window = tk.Toplevel()
    result_window.geometry("400x400")
    result_window.title("Top Flows Networks")
    result_window.configure(bg=CAT_BLACK)

    top_flows = data.nlargest(top_n, 'packets')[['src_addr', 'packets']]

    label = tk.Label(result_window, text=f"Top {top_n} networks by flows (Packets):", bg=CAT_BLACK, fg=CAT_YELLOW,
                     wraplength=350)
    label.pack(pady=10)

    for index, row in top_flows.iterrows():
        flows_label = tk.Label(result_window, text=f"Src Addr: {row['src_addr']} - Packets: {row['packets']}",
                               bg=CAT_BLACK, fg=CAT_YELLOW)
        flows_label.pack()

    close_button = ttk.Button(result_window, text="Close", style="TButton", command=result_window.destroy)
    close_button.pack(pady=10)


# Run the application
create_main_window()
