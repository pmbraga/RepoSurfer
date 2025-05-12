import os
import tempfile
import git
import dearpygui.dearpygui as dpg

repo_root = None  # global to store the root of the cloned repo

def load_repo_callback():
    global repo_root

    repo_url = dpg.get_value("repo_input").strip()
    if not repo_url.startswith("https://github.com"):
        dpg.set_value("repo_status", " Please enter a valid GitHub URL.")
        return

    dpg.set_value("repo_status", "⏳ Cloning repository...")

    try:
        temp_dir = tempfile.mkdtemp()
        git.Repo.clone_from(repo_url, temp_dir)
        repo_root = temp_dir
        dpg.set_value("repo_status", f" Loaded: {repo_url}")

        dpg.hide_item("repo_input")
        dpg.hide_item("load_repo_btn")

        # Clear and rebuild the repo tree
        dpg.delete_item("repo_tree", children_only=True)
        dpg.show_item("repo_tree")
        dpg.show_item("code_label")
        dpg.show_item("code_viewer")

        build_file_tree(repo_root, parent="repo_tree")

    except Exception as e:
        dpg.set_value("repo_status", f" Failed to clone: {e}")

def build_file_tree(root_path, parent):
    for entry in sorted(os.listdir(root_path)):
        full_path = os.path.join(root_path, entry)
        rel_path = os.path.relpath(full_path, repo_root)

        if os.path.isdir(full_path):
            with dpg.tree_node(label=entry, tag=rel_path, parent=parent):
                build_file_tree(full_path, rel_path)
        else:
            dpg.add_button(label=entry, parent=parent, callback=file_clicked, user_data=full_path)

def file_clicked(sender, app_data, user_data):
    try:
        with open(user_data, 'r', encoding="utf-8") as f:
            content = f.read()
        dpg.set_value("code_viewer", content)
    except Exception as e:
        dpg.set_value("code_viewer", f"⚠️ Error reading file: {e}")

def send_message_callback():
    user_message = dpg.get_value("chat_input").strip()
    if not user_message:
        return
    dpg.add_text(f"You: {user_message}", parent="chat_window")
    response_mode = dpg.get_value("response_mode")

    # Simulated LLM response
    if response_mode == "Verbose":
        llm_response = "Verbose response from the LLM explaining details..."
    else:
        llm_response = "Condensed summary from the LLM."

    dpg.add_text(f"LLM: {llm_response}", parent="chat_window")
    dpg.set_value("chat_input", "")

# --- UI Definition ---
dpg.create_context()

with dpg.window(label="MCP GitHub Code Explorer", tag="main_window"):
    with dpg.menu_bar():
        with dpg.menu(label="Settings"):
            dpg.add_combo(["Condensed", "Verbose"], default_value="Condensed", tag="response_mode", label="Response Detail Level")

    with dpg.group(horizontal=True):
        # LEFT PANEL: Git Repo View
        with dpg.child_window(border=True, autosize_y=True, width=600):
            dpg.add_text("🔗 Enter GitHub Repository URL")
            dpg.add_input_text(tag="repo_input", hint="https://github.com/user/repo")
            dpg.add_button(label="Load Repository", tag="load_repo_btn", callback=load_repo_callback)
            dpg.add_text("", tag="repo_status")

            dpg.add_spacer(height=10)
            with dpg.tree_node(label="Repository Files", tag="repo_tree", default_open=True, show=False):
                pass

            dpg.add_spacer(height=10)
            dpg.add_text(" Code Viewer", tag="code_label", show=False)
            dpg.add_input_text(tag="code_viewer", multiline=True, readonly=True, width=-1, height=300, show=False)

        # RIGHT PANEL: Chat Interface
        with dpg.child_window(border=True, autosize_y=True):
            dpg.add_text(" Ask Questions About the Code")
            with dpg.child_window(height=600, tag="chat_window", autosize_x=True):
                dpg.add_text("LLM: Hello! Ask me anything about the code.")
            dpg.add_input_text(tag="chat_input", hint="Type your question here...", on_enter=True, callback=send_message_callback)
            dpg.add_button(label="Send", callback=send_message_callback)

# Viewport configuration
dpg.create_viewport(title='MCP UI with GitHub Integration', width=1400, height=900)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("main_window", True)
dpg.start_dearpygui()
dpg.destroy_context()