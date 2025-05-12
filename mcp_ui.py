import dearpygui.dearpygui as dpg

def load_repo_callback():
    repo_url = dpg.get_value("repo_input")
    if not repo_url.strip():
        dpg.set_value("repo_status", "❌ Please enter a valid GitHub URL.")
        return

    dpg.set_value("repo_status", f"✅ Loaded: {repo_url}")
    dpg.hide_item("repo_input")
    dpg.hide_item("load_repo_btn")
    dpg.show_item("repo_tree")
    dpg.show_item("code_label")
    dpg.show_item("code_viewer")

def send_message_callback():
    user_message = dpg.get_value("chat_input")
    dpg.add_text(f"You: {user_message}", parent="chat_window")
    response_mode = dpg.get_value("response_mode")

    if response_mode == "Verbose":
        llm_response = "Verbose response from the LLM explaining all the details in depth..."
    else:
        llm_response = "Condensed summary from the LLM."

    dpg.add_text(f"LLM: {llm_response}", parent="chat_window")

def file_clicked(sender, app_data, user_data):
    filename = user_data
    code = f"# Content of {filename}\n\ndef hello():\n    return 'Hello, world!'"
    dpg.set_value("code_viewer", code)

dpg.create_context()

with dpg.window(label="Repo Surfer 1.0", tag="main_window"):
    with dpg.menu_bar():
        with dpg.menu(label="Settings"):
            dpg.add_combo(["Condensed", "Verbose"], default_value="Condensed", tag="response_mode", label="Response Detail Level")

    with dpg.group(horizontal=True):
        # Left Panel (Resizable)
        with dpg.child_window(border=True, autosize_y=True, autosize_x=False, tag="left_panel", width=600):
            dpg.add_text("🔗 Enter GitHub Repository URL")
            dpg.add_input_text(tag="repo_input", hint="https://github.com/user/repo")
            dpg.add_button(label="Load Repository", tag="load_repo_btn", callback=load_repo_callback)
            dpg.add_text("", tag="repo_status")

            with dpg.tree_node(label="Repository Files", tag="repo_tree", default_open=True, show=False):
                with dpg.tree_node(label="src", default_open=True):
                    dpg.add_button(label="main.py", callback=file_clicked, user_data="main.py")
                    dpg.add_button(label="utils.py", callback=file_clicked, user_data="utils.py")
                with dpg.tree_node(label="tests", default_open=False):
                    dpg.add_button(label="test_main.py", callback=file_clicked, user_data="test_main.py")

            dpg.add_spacer(height=10)
            dpg.add_text("📄 Code Viewer", tag="code_label", show=False)
            dpg.add_input_text(tag="code_viewer", multiline=True, readonly=True, width=-1, height=300, show=False)

        # Right Panel (Resizable)
        with dpg.child_window(border=True, autosize_y=True, autosize_x=False, tag="right_panel"):
            dpg.add_text("💬 Ask Questions About the Code")
            with dpg.child_window(height=600, tag="chat_window", autosize_x=True):
                dpg.add_text("LLM: Hello! Ask me anything about the code.")
            dpg.add_input_text(tag="chat_input", hint="Type your question here...", on_enter=True, callback=send_message_callback)
            dpg.add_button(label="Send", callback=send_message_callback)

# Set full screen and run
dpg.create_viewport(title='MCP UI with Resizable Panels', width=1400, height=900)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("main_window", True)
dpg.start_dearpygui()
dpg.destroy_context()
