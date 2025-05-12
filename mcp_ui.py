import dearpygui.dearpygui as dpg

def send_message_callback():
    user_message = dpg.get_value("chat_input")
    dpg.add_text(f"You: {user_message}", parent="chat_window")
    response_mode = dpg.get_value("response_mode")
    
    # Placeholder LLM response
    if response_mode == "Verbose":
        llm_response = "This is a **verbose** response from the LLM explaining all the relevant details in depth..."
    else:
        llm_response = "This is a **condensed** summary."
    
    dpg.add_text(f"LLM: {llm_response}", parent="chat_window")

def file_clicked(sender, app_data, user_data):
    filename = user_data
    # Simulated file content
    code = f"# Simulated content of {filename}\n\ndef hello():\n    return 'Hello, world!'"
    dpg.set_value("code_viewer", code)

dpg.create_context()

with dpg.window(label="MCP GitHub Code Explorer", width=1200, height=800):
    with dpg.menu_bar():
        with dpg.menu(label="Settings"):
            dpg.add_combo(["Condensed", "Verbose"], default_value="Condensed", tag="response_mode", label="Response Detail Level")

    with dpg.group(horizontal=True):
        # Left Panel: Git Repo and Code Viewer
        with dpg.child_window(width=600, border=True):
            dpg.add_text("📁 GitHub Repository")
            with dpg.tree_node(label="src", default_open=True):
                dpg.add_button(label="main.py", callback=file_clicked, user_data="main.py")
                dpg.add_button(label="utils.py", callback=file_clicked, user_data="utils.py")
            with dpg.tree_node(label="tests", default_open=False):
                dpg.add_button(label="test_main.py", callback=file_clicked, user_data="test_main.py")
            dpg.add_spacer(height=10)
            dpg.add_text("📄 Code Viewer")
            dpg.add_input_text(tag="code_viewer", multiline=True, readonly=True, width=580, height=300)

        # Right Panel: Chat Interface
        with dpg.child_window(width=600, border=True):
            dpg.add_text("💬 Ask Questions About the Code")
            with dpg.child_window(height=600, tag="chat_window", autosize_x=True):
                dpg.add_text("LLM: Hello! Ask me anything about the code.")
            dpg.add_input_text(tag="chat_input", hint="Type your question here...", on_enter=True, callback=send_message_callback)
            dpg.add_button(label="Send", callback=send_message_callback)

dpg.create_viewport(title='MCP UI Mockup', width=1220, height=820)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
