import mysql.connector
import tkinter as tk
from tkinter import messagebox
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def connect_db():
    conn = mysql.connector.connect(
        host="127.0.0.1",
        port=3306,
        user="root", 
        passwd="", 
        database="data_tracker" 
    )
    return conn


def create_database():
    conn = mysql.connector.connect(
        host="127.0.0.1",
        port=3306,
        user="root",
        passwd=""  
    )
    cursor = conn.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS data_tracker")
    conn.close()


def create_table():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS screen_usage (
            date DATE,
            day VARCHAR(10),
            youtube FLOAT,
            instagram FLOAT,
            educational FLOAT,
            others FLOAT
        )
    ''')
    conn.commit()
    conn.close()


def load_data():
    conn = connect_db()
    query = "SELECT * FROM screen_usage"  
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df


def save_data():
    conn = connect_db()
    cursor = conn.cursor()
    for _, row in df.iterrows():
        cursor.execute(''' 
            INSERT INTO screen_usage (date, day, youtube, instagram, educational, others)  # Updated to use screen_usage
            VALUES (%s, %s, %s, %s, %s, %s)
        ''', (row['date'], row['day'], row['youtube'], row['instagram'], row['educational'], row['others']))
    conn.commit()
    conn.close()


create_database()
create_table()


try:
    df = load_data()
except:
    df = pd.DataFrame(columns=["date", "day", "youtube", "instagram", "educational", "others"])


root = tk.Tk()
root.title("Tracker Data Viewer & Graphical Representation")
root.configure(bg='#D2B48C')


def view_data():
    top = tk.Toplevel(root)
    top.title("View Data")
    top.configure(bg='#D2B48C')
    text = tk.Text(top, wrap="word", bg='#D2B48C', fg='black')
    text.pack(fill=tk.BOTH, expand=True)
    text.insert(tk.END, df.to_string(index=False))
    text.config(state=tk.DISABLED)


def add_record():
    def submit_record():
        try:
            date = date_entry.get()
            day = day_entry.get()
            youtube = float(youtube_entry.get())
            instagram = float(instagram_entry.get())
            educational = float(educational_entry.get())
            others = float(others_entry.get())

            new_data = {
                "date": date,
                "day": day,
                "youtube": youtube,
                "instagram": instagram,
                "educational": educational,
                "others": others
            }

            global df
            df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)

            
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute(''' 
                INSERT INTO screen_usage (date, day, youtube, instagram, educational, others)  # Updated to use screen_usage
                VALUES (%s, %s, %s, %s, %s, %s)
            ''', (date, day, youtube, instagram, educational, others))
            conn.commit()
            conn.close()

            messagebox.showinfo("Success", "Record added successfully!")
            add_window.destroy()
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numerical values.")

    add_window = tk.Toplevel(root)
    add_window.title("Add Record")
    add_window.configure(bg='#D2B48C')

    
    tk.Label(add_window, text="Date (YYYY-MM-DD)", bg='#D2B48C').grid(row=0, column=0)
    tk.Label(add_window, text="Day", bg='#D2B48C').grid(row=1, column=0)
    tk.Label(add_window, text="YouTube", bg='#D2B48C').grid(row=2, column=0)
    tk.Label(add_window, text="Instagram", bg='#D2B48C').grid(row=3, column=0)
    tk.Label(add_window, text="Educational", bg='#D2B48C').grid(row=4, column=0)
    tk.Label(add_window, text="Others", bg='#D2B48C').grid(row=5, column=0)

    date_entry = tk.Entry(add_window)
    day_entry = tk.Entry(add_window)
    youtube_entry = tk.Entry(add_window)
    instagram_entry = tk.Entry(add_window)
    educational_entry = tk.Entry(add_window)
    others_entry = tk.Entry(add_window)

    date_entry.grid(row=0, column=1)
    day_entry.grid(row=1, column=1)
    youtube_entry.grid(row=2, column=1)
    instagram_entry.grid(row=3, column=1)
    educational_entry.grid(row=4, column=1)
    others_entry.grid(row=5, column=1)

    submit_button = tk.Button(add_window, text="Submit", command=submit_record)
    submit_button.grid(row=6, column=0, columnspan=2)


def graphical_representation():
    def plot_graph():
        selected_graph = graph_type_var.get()
        df_sorted = df.dropna(subset=["date"]).sort_values("date")

        fig, ax = plt.subplots(figsize=(10, 6))

        if selected_graph == "Line":
            df_sorted.plot(x="date", y=["youtube", "instagram", "educational", "others"], kind="line", ax=ax)
        elif selected_graph == "Bar":
            df_sorted.plot(x="date", y=["youtube", "instagram", "educational", "others"], kind="bar", ax=ax)
        elif selected_graph == "Pie":
            aggregate_data = df_sorted[['youtube', 'instagram', 'educational', 'others']].sum()
            aggregate_data.plot(kind="pie", autopct='%1.1f%%', ax=ax)
            ax.set_ylabel('')
        else:
            messagebox.showerror("Error", "Please select a valid graph type.")
            return

        ax.set_title(f"{selected_graph} Chart")
        plt.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=graph_window)
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        canvas.draw()

    graph_window = tk.Toplevel(root)
    graph_window.title("Graphical Representation")
    graph_window.configure(bg='#D2B48C')

    tk.Label(graph_window, text="Select Graph Type:", bg='#D2B48C').pack(pady=10)
    graph_type_var = tk.StringVar(value="Line")
    graph_types = ["Line", "Bar", "Pie"]
    for graph in graph_types:
        tk.Radiobutton(graph_window, text=graph, variable=graph_type_var, value=graph, bg='#D2B48C').pack()

    plot_button = tk.Button(graph_window, text="Plot Graph", command=plot_graph)
    plot_button.pack(pady=10)


view_button = tk.Button(root, text="View Data", width=20, command=view_data, bg='#D2B48C')
view_button.pack(pady=10)

add_button = tk.Button(root, text="Add Record", width=20, command=add_record, bg='#D2B48C')
add_button.pack(pady=10)

graph_button = tk.Button(root, text="Graphical Representation", width=20, command=graphical_representation, bg='#D2B48C')
graph_button.pack(pady=10)

root.mainloop()
