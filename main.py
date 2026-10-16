import customtkinter as ctk

# APP SETTINGS
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")
app = ctk.CTk()
app.title("Python Study Tracker")
app.geometry("1100x800")
app.minsize(950, 700)

#DATA
topics = [
    "Variables",
    "Data Types",
    "Strings",
    "Lists",
    "Tuples",
    "Sets",
    "Dictionaries",
    "If Statements",
    "Loops",
    "Functions",
    "Modules",
    "File Handling",
    "Exception Handling",
    "Object-Oriented Programming",
]

# Number of solved exercises for every topic
topic_exercises = {
    topic: 0 for topic in topics
}

# Completed topics
studied_topics = set()

# Tasks
tasks = []


#COLORS / STYLES
BG_COLOR = "#0B0F14"
CARD_COLOR = "#121820"
CARD_HOVER = "#18212B"

TEXT_PRIMARY = "#F5F7FA"
TEXT_SECONDARY = "#8B98A7"

ACCENT = "#4F8CFF"
ACCENT_HOVER = "#6A9DFF"

GREEN = "#35D07F"
PURPLE = "#9B7BFF"
ORANGE = "#FFB454"
RED = "#FF5C6C"


#HELPER FUNCTIONS
def get_exercise_count():
    """Return total solved exercises."""
    return sum(topic_exercises.values())


def get_project_count():
    """Return number of completed projects."""
    return sum(
        1 for task in tasks
        if task["type"] == "Project" and task["done"]
    )

def get_completed_exercise_tasks():
    """Return completed exercise tasks."""
    return sum(
        1 for task in tasks
        if task["type"] == "Exercise" and task["done"]
    )

def update_dashboard():
    """Update all dashboard statistics."""

    # Exercises
    exercise_count = get_exercise_count()
    exercise_card_value.configure(
        text=str(exercise_count)
    )

    # Projects
    project_count = get_project_count()
    project_card_value.configure(
        text=str(project_count)
    )

    # Topics
    studied_count = len(studied_topics)
    topic_card_value.configure(
        text=f"{studied_count}/{len(topics)}"
    )

    # Progress
    percentage = studied_count / len(topics)

    progress_card_value.configure(
        text=f"{percentage * 100:.0f}%"
    )

    progress_bar.set(percentage)

    progress_percent.configure(
        text=f"{percentage * 100:.0f}%"
    )

    progress_text.configure(
        text=f"{studied_count} of {len(topics)} topics completed"
    )

#TOPIC FUNCTIONS
def update_topic_exercise_label(choice=None):
    """Update exercise counter when topic changes."""

    topic = topic_menu.get()

    count = topic_exercises.get(topic, 0)

    topic_exercise_label.configure(
        text=f"{count} exercises solved for this topic"
    )

    exercise_spinbox.delete(0, "end")
    exercise_spinbox.insert(0, str(count))

def update_exercise_count():
    """Save spinbox value for selected topic."""
    topic = topic_menu.get()
    try:
        count = int(exercise_spinbox.get())
        if count < 0:
            count = 0
    except ValueError:
        count = 0
    topic_exercises[topic] = count
    topic_exercise_label.configure(
        text=f"{count} exercises solved for this topic"
    )
    update_dashboard()

def mark_as_studied():
    """Mark selected topic as studied."""
    topic = topic_menu.get()
    studied_topics.add(topic)
    studied_label.configure(
        text=f"✓ {topic} marked as completed",
        text_color=GREEN
    )
    update_dashboard()


#TASK FUNCTIONS
def add_task():
    """Add a new exercise/project."""
    task_name = task_entry.get().strip()
    task_type = task_type_menu.get()
    if not task_name:
        return
    task = {
        "name": task_name,
        "type": task_type,
        "done": False
    }
    tasks.append(task)
    task_entry.delete(0, "end")
    show_tasks()
    update_dashboard()

def complete_task(task):
    """Toggle task completion."""
    task["done"] = not task["done"]
    show_tasks()
    update_dashboard()

def delete_task(task):
    """Delete a task."""
    if task in tasks:
        tasks.remove(task)
    show_tasks()
    update_dashboard()

def show_tasks():
    """Refresh task list."""
    for widget in task_list_frame.winfo_children():
        widget.destroy()
    if not tasks:
        empty_label = ctk.CTkLabel(
            task_list_frame,
            text="No exercises or projects yet.",
            text_color=TEXT_SECONDARY,
            font=ctk.CTkFont(size=13)
        )
        empty_label.pack(
            pady=30
        )
        return
    
    for task in tasks:

        task_card = ctk.CTkFrame(
            task_list_frame,
            fg_color=CARD_COLOR,
            corner_radius=12
        )
        task_card.pack(
            fill="x",
            padx=5,
            pady=5
        )
        # -------------------------
        # Task checkbox

        checkbox = ctk.CTkCheckBox(
            task_card,
            text="",
            width=25,
            command=lambda item=task: complete_task(item)
        )

        checkbox.pack(
            side="left",
            padx=(12, 5),
            pady=12
        )

        if task["done"]:
            checkbox.select()

        # -------------------------
        # Task information

        info_frame = ctk.CTkFrame(
            task_card,
            fg_color="transparent"
        )

        info_frame.pack(
            side="left",
            fill="x",
            expand=True,
            pady=8
        )

        task_name_label = ctk.CTkLabel(
            info_frame,
            text=task["name"],
            anchor="w",
            font=ctk.CTkFont(
                size=14,
                weight="bold"
            ),
            text_color=(
                TEXT_SECONDARY
                if task["done"]
                else TEXT_PRIMARY
            )
        )

        task_name_label.pack(
            anchor="w"
        )

        type_color = (
            GREEN
            if task["type"] == "Exercise"
            else PURPLE
        )

        type_label = ctk.CTkLabel(
            info_frame,
            text=task["type"],
            text_color=type_color,
            font=ctk.CTkFont(size=11)
        )

        type_label.pack(
            anchor="w",
            pady=(2, 0)
        )

        # -------------------------
        # Delete button

        delete_button = ctk.CTkButton(
            task_card,
            text="×",
            width=35,
            height=32,
            fg_color="transparent",
            hover_color="#252D37",
            text_color=RED,
            font=ctk.CTkFont(
                size=20,
                weight="bold"
            ),
            command=lambda item=task: delete_task(item)
        )

        delete_button.pack(
            side="right",
            padx=10
        )


#MAIN LAYOUT
app.configure(
    fg_color=BG_COLOR
)


# HEADER
header = ctk.CTkFrame(
    app,
    fg_color="transparent"
)

header.pack(
    fill="x",
    padx=35,
    pady=(28, 10)
)

title = ctk.CTkLabel(
    header,
    text="🐍 Python Study Tracker",
    font=ctk.CTkFont(
        size=30,
        weight="bold"
    ),
    text_color=TEXT_PRIMARY
)

title.pack(
    anchor="w"
)

subtitle = ctk.CTkLabel(
    header,
    text="Track your learning, exercises and projects.",
    font=ctk.CTkFont(size=14),
    text_color=TEXT_SECONDARY
)

subtitle.pack(
    anchor="w",
    pady=(5, 0)
)

# STATISTICS CARDS
stats_frame = ctk.CTkFrame(
    app,
    fg_color="transparent"
)

stats_frame.pack(
    fill="x",
    padx=35,
    pady=15
)

stats_frame.grid_columnconfigure(
    (0, 1, 2, 3),
    weight=1
)

def create_stat_card(
    parent,
    column,
    title,
    value,
    icon,
    color
):
    card = ctk.CTkFrame(
        parent,
        fg_color=CARD_COLOR,
        corner_radius=16,
        height=120
    )

    card.grid(
        row=0,
        column=column,
        sticky="nsew",
        padx=6
    )

    card.grid_propagate(False)

    icon_label = ctk.CTkLabel(
        card,
        text=icon,
        font=ctk.CTkFont(size=24)
    )

    icon_label.pack(
        anchor="w",
        padx=16,
        pady=(14, 0)
    )

    value_label = ctk.CTkLabel(
        card,
        text=value,
        font=ctk.CTkFont(
            size=25,
            weight="bold"
        ),
        text_color=color
    )

    value_label.pack(
        anchor="w",
        padx=16,
        pady=(2, 0)
    )

    title_label = ctk.CTkLabel(
        card,
        text=title,
        font=ctk.CTkFont(size=12),
        text_color=TEXT_SECONDARY
    )

    title_label.pack(
        anchor="w",
        padx=16
    )

    return value_label

exercise_card_value = create_stat_card(
    stats_frame,
    0,
    "Exercises Solved",
    "0",
    "🧩",
    GREEN
)

project_card_value = create_stat_card(
    stats_frame,
    1,
    "Projects Completed",
    "0",
    "🚀",
    PURPLE
)

topic_card_value = create_stat_card(
    stats_frame,
    2,
    "Topics Completed",
    "0/14",
    "📚",
    ACCENT
)

progress_card_value = create_stat_card(
    stats_frame,
    3,
    "Overall Progress",
    "0%",
    "⚡",
    ORANGE
)

#CONTENT AREA
content = ctk.CTkFrame(
    app,
    fg_color="transparent"
)

content.pack(
    fill="both",
    expand=True,
    padx=35,
    pady=10
)

content.grid_columnconfigure(
    0,
    weight=1
)

content.grid_columnconfigure(
    1,
    weight=1
)

content.grid_rowconfigure(
    0,
    weight=1
)


#LEFT PANEL
left_panel = ctk.CTkFrame(
    content,
    fg_color=CARD_COLOR,
    corner_radius=18
)

left_panel.grid(
    row=0,
    column=0,
    sticky="nsew",
    padx=(0, 8)
)

ctk.CTkLabel(
    left_panel,
    text="📚 Study Topic",
    font=ctk.CTkFont(
        size=20,
        weight="bold"
    )
).pack(
    anchor="w",
    padx=22,
    pady=(22, 5)
)

ctk.CTkLabel(
    left_panel,
    text="Select a topic and track your exercises.",
    text_color=TEXT_SECONDARY,
    font=ctk.CTkFont(size=12)
).pack(
    anchor="w",
    padx=22,
    pady=(0, 20)
)

# ---------------- Topic selection ----------------
topic_menu = ctk.CTkOptionMenu(
    left_panel,
    values=topics,
    width=300,
    height=42,
    corner_radius=10,
    fg_color="#1A222C",
    button_color=ACCENT,
    button_hover_color=ACCENT_HOVER,
    dropdown_fg_color="#161D26",
    command=update_topic_exercise_label
)

topic_menu.pack(
    padx=22,
    fill="x"
)

#EXERCISE COUNTER
ctk.CTkLabel(
    left_panel,
    text="Exercises solved",
    font=ctk.CTkFont(
        size=14,
        weight="bold"
    )
).pack(
    anchor="w",
    padx=22,
    pady=(25, 8)
)

exercise_counter_frame = ctk.CTkFrame(
    left_panel,
    fg_color="transparent"
)

exercise_counter_frame.pack(
    fill="x",
    padx=22
)

exercise_spinbox = ctk.CTkEntry(
    exercise_counter_frame,
    width=90,
    height=42,
    justify="center",
    font=ctk.CTkFont(
        size=16,
        weight="bold"
    )
)

exercise_spinbox.pack(
    side="left"
)

exercise_spinbox.insert(
    0,
    "0"
)

# Custom +/- buttons
def increase_exercises():
    try:
        value = int(exercise_spinbox.get())
    except ValueError:
        value = 0

    exercise_spinbox.delete(0, "end")
    exercise_spinbox.insert(0, str(value + 1))

    update_exercise_count()

def decrease_exercises():
    try:
        value = int(exercise_spinbox.get())
    except ValueError:
        value = 0

    value = max(0, value - 1)

    exercise_spinbox.delete(0, "end")
    exercise_spinbox.insert(0, str(value))

    update_exercise_count()

minus_button = ctk.CTkButton(
    exercise_counter_frame,
    text="−",
    width=42,
    height=42,
    fg_color="#202A35",
    hover_color="#2B3745",
    font=ctk.CTkFont(
        size=18,
        weight="bold"
    ),
    command=decrease_exercises
)

minus_button.pack(
    side="left",
    padx=(8, 4)
)

plus_button = ctk.CTkButton(
    exercise_counter_frame,
    text="+",
    width=42,
    height=42,
    fg_color=ACCENT,
    hover_color=ACCENT_HOVER,
    font=ctk.CTkFont(
        size=18,
        weight="bold"
    ),
    command=increase_exercises
)

plus_button.pack(
    side="left"
)

topic_exercise_label = ctk.CTkLabel(
    left_panel,
    text="0 exercises solved for this topic",
    text_color=TEXT_SECONDARY,
    font=ctk.CTkFont(size=12)
)

topic_exercise_label.pack(
    anchor="w",
    padx=22,
    pady=(8, 20)
)

# ---------------- Save counter ----------------
ctk.CTkButton(
    left_panel,
    text="↻ Update Exercise Count",
    height=40,
    corner_radius=10,
    fg_color="#202A35",
    hover_color="#2B3745",
    command=update_exercise_count
).pack(
    fill="x",
    padx=22,
    pady=5
)

# MARK AS STUDIED
ctk.CTkButton(
    left_panel,
    text="✓  Mark as Studied",
    height=44,
    corner_radius=11,
    fg_color=GREEN,
    hover_color="#2BBE6F",
    text_color="#07120C",
    font=ctk.CTkFont(
        size=14,
        weight="bold"
    ),
    command=mark_as_studied
).pack(
    fill="x",
    padx=22,
    pady=(12, 8)
)


studied_label = ctk.CTkLabel(
    left_panel,
    text="Choose a topic to get started.",
    text_color=TEXT_SECONDARY,
    font=ctk.CTkFont(size=12)
)

studied_label.pack(
    anchor="w",
    padx=22
)

#PROGRESS
progress_section = ctk.CTkFrame(
    left_panel,
    fg_color="#0F151C",
    corner_radius=14
)

progress_section.pack(
    fill="x",
    padx=22,
    pady=25
)

progress_percent = ctk.CTkLabel(
    progress_section,
    text="0%",
    font=ctk.CTkFont(
        size=25,
        weight="bold"
    ),
    text_color=ACCENT
)

progress_percent.pack(
    anchor="w",
    padx=15,
    pady=(12, 0)
)

progress_text = ctk.CTkLabel(
    progress_section,
    text="0 of 14 topics completed",
    text_color=TEXT_SECONDARY
)

progress_text.pack(
    anchor="w",
    padx=15
)

progress_bar = ctk.CTkProgressBar(
    progress_section,
    height=8,
    corner_radius=5,
    progress_color=ACCENT
)

progress_bar.pack(
    fill="x",
    padx=15,
    pady=(10, 15)
)
progress_bar.set(0)


# RIGHT PANEL
right_panel = ctk.CTkFrame(
    content,
    fg_color=CARD_COLOR,
    corner_radius=18
)

right_panel.grid(
    row=0,
    column=1,
    sticky="nsew",
    padx=(8, 0)
)

ctk.CTkLabel(
    right_panel,
    text="📝 Exercises & Projects",
    font=ctk.CTkFont(
        size=20,
        weight="bold"
    )
).pack(
    anchor="w",
    padx=22,
    pady=(22, 5)
)

ctk.CTkLabel(
    right_panel,
    text="Add what you are working on.",
    text_color=TEXT_SECONDARY,
    font=ctk.CTkFont(size=12)
).pack(
    anchor="w",
    padx=22,
    pady=(0, 18)
)

#ADD TASK
task_entry = ctk.CTkEntry(
    right_panel,
    placeholder_text="Enter an exercise or project...",
    height=42,
    corner_radius=10
)

task_entry.pack(
    fill="x",
    padx=22,
    pady=5
)

task_options = ctk.CTkFrame(
    right_panel,
    fg_color="transparent"
)

task_options.pack(
    fill="x",
    padx=22,
    pady=7
)

task_type_menu = ctk.CTkOptionMenu(
    task_options,
    values=["Exercise", "Project"],
    width=150,
    height=38,
    corner_radius=9,
    fg_color="#1A222C",
    button_color=PURPLE,
    button_hover_color="#AE95FF"
)

task_type_menu.pack(
    side="left"
)

ctk.CTkButton(
    task_options,
    text="+ Add",
    width=110,
    height=38,
    corner_radius=9,
    fg_color=ACCENT,
    hover_color=ACCENT_HOVER,
    command=add_task
).pack(
    side="right"
)

#TASK LIST
task_list_frame = ctk.CTkScrollableFrame(
    right_panel,
    fg_color="transparent",
    corner_radius=10
)

task_list_frame.pack(
    fill="both",
    expand=True,
    padx=17,
    pady=(10, 18)
)

#START
update_topic_exercise_label()
show_tasks()
update_dashboard()
app.mainloop()