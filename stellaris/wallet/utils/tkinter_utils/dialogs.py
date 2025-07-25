import tkinter as tk
from tkinter import ttk
import ttkbootstrap as tb
from .custom_dialog import CustomDialog
from PIL import ImageTk, Image
import _tkinter

class Dialogs:

    def __init__(self, root):
        self.root = root
        self.dialog_functions = DialogFunctions(self.root, self)


    def messagebox(self, title, msg, is_callback=False):
        result, _, _ = CustomDialog(parent=self.root, title=title, 
                                    prompt=[
                                    {'type': 'label', 
                                     "config":"text='{}', wraplength=500, justify='left'".format(msg), 
                                     "grid_config":"column=0"},
                                    
                                    {'type': 'button', 
                                     "config":"text='Okay'", 
                                     "command":"command_str=self.submit_entry", 
                                     "grid_config":"row=2, column=0, sticky='we', padx=(0, 5), pady=(10, 0)"}
                                     ], true_on_submit=True).result
        
        if is_callback:
                self.root.stored_data.ask_bool_result = result[0]
                self.root.wallet_thread_manager.dialog_event.set()
        else:
            return result[0]


    def address_info(self, event=None, entry_data=None, entry_type=None,  is_callback=False):
        
        if not entry_data:
            widget = event.widget if event else self.root.current_event.widget
            if isinstance(widget, ttk.Treeview):
                # Treeview copy functionality
                row_id = widget.identify_row(self.root.current_event.y)
                col_id = int(widget.identify_column(self.root.current_event.x).replace('#', '')) - 1
                if len(row_id) > 0:            
                    item = widget.item(row_id)
                    address = item['values'][col_id]
                    entry_data, entry_type = self.root.wallet_operations.get_entry_data(address)        
        
        entry_type = "Generated Address" if entry_type == 'entries' else "Imported Address"
      
        if entry_data:
            CustomDialog(parent=self.root, 
                         title="Address Info", 
                         prompt=
                            [
                                {"type":"label", "config":"text='Address Info', font='Helvetica 16 bold'", 
                                 "grid_config":"column=0, columnspan=2"},
                                
                                {"type":"frame", 
                                 "widget_name":"frame_1", 
                                 "grid_config":"column=0, sticky='w'"},
                                 
                                {"type":"label", 
                                 "config":"text='ID:', font='Helvetica 12 bold'",
                                 "parent":"frame_1",
                                 "pack_config":"side='left'"},
                                    
                                {"type":"entry", 
                                 "config":"style='addressInfo.TEntry', state='readonly', font='Helvetica 12 bold'",
                                 "parent":"frame_1",
                                 "insert":"string='{}'".format(entry_data['id']),
                                 "style_map_config":"style='addressInfo.TEntry', lightcolor='[(\"focus\", \"white\")]'",
                                 "variables": {"expand_entry_width": True},
                                 "pack_config":"side='left'"},
                                
                                {"type":"frame", 
                                 "widget_name":"frame_2", 
                                 "grid_config":"column=0, sticky='w'"},
                                 
                                {"type":"label", 
                                 "config":"text='Type:', font='Helvetica 12 bold'",
                                 "parent":"frame_2",
                                 "pack_config":"side='left'"},
                                    
                                {"type":"entry", 
                                 "config":"style='addressInfo.TEntry', state='readonly', font='Helvetica 12 bold'",
                                 "parent":"frame_2",
                                 "insert":"string='{}'".format(entry_type),
                                 "variables": {"expand_entry_width": True},
                                 "pack_config":"side='left'"},

                                {"type":"separator", 
                                 "config":"orient='horizontal'", 
                                 "grid_config":"column=0, columnspan=2, sticky='we', pady=(0, 5)"},
                                 
                                {"type":"frame", 
                                 "widget_name":"frame_3", 
                                 "grid_config":"column=0, sticky='w'"},
                                 
                                {"type":"label", 
                                 "config":"text='Address:', font='Helvetica 12 bold'",
                                 "parent":"frame_3",
                                 "pack_config":"side='left'"},
                                    
                                {"type":"entry", 
                                 "config":"style='addressInfo.TEntry', state='readonly', font='Helvetica 12 bold'",
                                 "parent":"frame_3",
                                 "insert":"string='{}'".format(entry_data['address']),
                                 "variables": {"expand_entry_width": True},
                                 "pack_config":"side='left'"},

                                {"type":"frame", 
                                 "widget_name":"frame_4", 
                                 "grid_config":"column=0, sticky='w'"},
                                 
                                {"type":"label", 
                                 "config":"text='Public Key:', font='Helvetica 12 bold'",
                                 "parent":"frame_4",
                                 "pack_config":"side='left'"},
                                    
                                {"type":"entry", 
                                 "config":"style='addressInfo.TEntry', state='readonly', font='Helvetica 12 bold'",
                                 "parent":"frame_4",
                                 "insert":"string='{}'".format(entry_data['public_key']),
                                 "variables": {"expand_entry_width": True},
                                 "pack_config":"side='left'"},

                                {"type":"frame", 
                                 "widget_name":"frame_5", 
                                 "grid_config":"column=0, sticky='w'"},
                                 
                                {"type":"label", 
                                 "config":"text='Private Key:', font='Helvetica 12 bold'",
                                 "parent":"frame_5",
                                 "pack_config":"side='left'"},

                                {"type":"entry",
                                 "widget_name":"private_key",
                                 "config":"style='addressInfo.TEntry', state='readonly', font='Helvetica 12 bold'", 
                                 "parent":"frame_5",
                                 "insert":"string='{}'".format(f"{entry_data['private_key']}"),
                                 "variables": {"expand_entry_width": True},
                                 "pack_config":"side='left'"},
                                
                                {"type":"frame", 
                                 "widget_name":"frame_6", 
                                 "grid_config":"row=6, column=1, sticky='w'"},
                                 
                                {"type":"button",
                                 "widget_name":"private_key_toggle",
                                 "class":"KeyToggle",
                                 "style_config":"style='toggle1.TButton', background='white', borderwidth=0, highlightthickness=0, padx=0, pady=0",
                                 "style_map_config":"style='toggle1.TButton', background=[(\"active\",\"white\")], foreground=[(\"disabled\",\"gray\")]",
                                 "config":"style='toggle1.TButton', padding=0",                                  
                                 "command": "command_str='set_key_visibility', args='(self.widget_references[\"private_key_toggle\"], self.widget_references[\"private_key\"],)', execute_on_load=True, first=True",
                                 "binds":[{"bind_config":"event='<Button-1>', callback_str='toggle_key_visibility', args='(self.widget_references[\"private_key_toggle\"], self.widget_references[\"private_key\"],)'"}],
                                 "parent":"frame_6",
                                 "pack_config":"side='left', padx=(5, 0), pady=(0, 5)"},

                                {"type":"frame", 
                                 "widget_name":"frame_7", 
                                 "grid_config":"column=0, sticky='w'",
                                 "hidden":False if "mnemonic" in entry_data else True},
                                 
                                {"type":"label", 
                                 "config":"text='Mnemonic:', font='Helvetica 12 bold'",
                                 "parent":"frame_7",
                                 "pack_config":"side='left'"},

                                {"type":"entry",
                                 "widget_name":"mnemonic",
                                 "config":"style='addressInfo.TEntry', state='readonly', font='Helvetica 12 bold'", 
                                 "parent":"frame_7",
                                 "insert":"string='{}'".format(f"{entry_data['mnemonic']}" if "mnemonic" in entry_data else ""),
                                 "variables": {"expand_entry_width": True},
                                 "pack_config":"side='left'"},
                                
                                {"type":"frame", 
                                 "widget_name":"frame_8", 
                                 "grid_config":"row=8, column=1, sticky='w'",
                                 "hidden":False if "mnemonic" in entry_data else True},
                                 
                                {"type":"button",
                                 "widget_name":"mnemonic_toggle",
                                 "class":"KeyToggle",
                                 "style_config":"style='toggle1.TButton', background='white', borderwidth=0, highlightthickness=0, padx=0, pady=0",
                                 "style_map_config":"style='toggle1.TButton', background=[(\"active\",\"white\")], foreground=[(\"disabled\",\"gray\")]",
                                 "config":"style='toggle1.TButton', padding=0",                                  
                                 "command": "command_str='set_key_visibility', args='(self.widget_references[\"mnemonic_toggle\"], self.widget_references[\"mnemonic\"],)', execute_on_load=True, first=True",
                                 "binds":[{"bind_config":"event='<Button-1>', callback_str='toggle_key_visibility', args='(self.widget_references[\"mnemonic_toggle\"], self.widget_references[\"mnemonic\"],)'"}],
                                 "parent":"frame_8",
                                 "pack_config":"side='left', padx=(5, 0), pady=(0, 5)"},
                                    
                                {"type":"button", 
                                 "config":"text='Close'",
                                 "command":"command_str=self.cancel",
                                 "grid_config":"column=0, columnspan=2, sticky='ew'"}
                            ], true_on_submit=False, callbacks={"set_key_visibility":self.dialog_functions.set_key_visibility, "toggle_key_visibility":self.dialog_functions.toggle_key_visibility},
                            classes={"KeyToggle":KeyToggle}).result
        if is_callback:
            self.root.wallet_thread_manager.dialog_event.set()


    def create_wallet_dialog(self):

        if self.root.stored_data.operation_mode != 'send':
            self.root.gui_utils.close_wallet()
        else:
            self.messagebox("Error", "Can not create a new wallet while a transaction is taking place.")
            return
        
        result, checkbox_values, _ = CustomDialog(parent=self.root, 
                            title="Create Wallet", 
                            prompt=
                            [     
                                {"type":"label", "config":"text='Create Wallet', font='Helvetica 14 bold'", 
                                 "grid_config":"column=0"},

                                {'type': 'separator', 
                                 "config":"orient='horizontal'", 
                                 "grid_config":"column=0, columnspan=2, sticky='we'"},
                                 
                                {"type":"label", 
                                 "config":"text='Wallet Name: ', font='Helvetica 10 bold'",
                                 "grid_config":"column=0, sticky='w', pady=(20, 0)"},
                                    
                                {"type":"entry", 
                                 "config":"state='normal'",
                                 #"variables":[{"set_var":"name='disable_context_menu_items', value=True"}],
                                 "grid_config":"column=0, sticky='we', padx=(25, 0), pady=(5, 0)"},

                                {"type":"label", 
                                 "config":"text='Wallet Options:', font='Helvetica 10 bold'", 
                                 "grid_config":"column=0, sticky='w', pady=(20, 0)"},

                                {"type":"checkbox", 
                                 "widget_name":"deterministic_checkbox", 
                                 "config":"text='Deterministic Address Generation'",
                                 "grid_config":"column=0, sticky='w', padx=(25, 0), pady=(5, 0)"},                                 

                                 {"type":"checkbox", 
                                 "widget_name":"2fa_checkbox", 
                                 "config":"text='Two-Factor Authentication', state='disabled'",
                                 "grid_config":"row=7, column=0, sticky='w', padx=(25, 0), pady=(10, 0)"},

                                {"type":"checkbox", 
                                 "widget_name":"encrypt_checkbox", 
                                 "config":"text='Encryption'",
                                 "command": "command_str='enable_2fa_checkbox', args='(self.widget_references[\"encrypt_checkbox\"], self.widget_references[\"2fa_checkbox\"],)', execute_on_load=False",
                                 "grid_config":"row=6, column=0, sticky='w', padx=(25, 0), pady=(10, 0)"},        

                                {"type":"frame", 
                                 "widget_name":"frame_1", 
                                 "grid_config":"column=0, sticky='we', pady=(20, 0)"},                              

                                {'type': 'button', 
                                 "config":"text='Cancel', width=20", 
                                 "command":"command_str=self.cancel", 
                                 "parent":"frame_1",
                                 "pack_config":"side='left', expand=True, fill=x, padx=(0, 5)"},

                                {'type': 'button', 
                                 "config":"text='Continue', width=20", 
                                 "command":"command_str=self.submit_entry", 
                                 "parent":"frame_1",
                                 "pack_config":"side='right', expand=True, fill=x, padx=(5, 0)"},

                            ], callbacks={"enable_2fa_checkbox":self.dialog_functions.enable_2fa_checkbox}).result
        
        filename = result[0]

        if filename == '':
            self.messagebox('Error', 'No wallet name provided.')
            self.create_wallet_dialog()
            return
            
        if filename is None:
            return
        
        password = None

        
        if checkbox_values[2]:

            password = self.password_dialog_with_confirmation(title='Create Wallet', msg=f'Please choose a password.\nThis will be used for wallet encryption and decryption.', is_callback=False)

            if not password:
                return

            enable_2fa_value = checkbox_values[1]

        if checkbox_values[2] is False:
            enable_2fa_value = False
        
        self.root.wallet_thread_manager.start_thread("create_wallet", self.root.wallet_operations.create_wallet, args=(result[0], password, checkbox_values[0], checkbox_values[2], enable_2fa_value), )
    
    def password_dialog(self, title, msg, show, is_callback):
        # This is called by the main thread to  show the dialog
        result, _, _ = CustomDialog(parent=self.root, title=title, 
                                        prompt=[
                                                {'type': 'label', 
                                                 "config":"text={}".format(msg), 
                                                 "grid_config":"column=0, columnspan=2"},


                                                {"type":"frame", 
                                                 "widget_name":"frame_1", 
                                                 "grid_config":"column=0, columnspan=2, sticky='nswe', pady=(10, 0)"}, 
                                                 
                                                {"type":"entry", 
                                                 "widget_name":"password_entry", 
                                                 "config":"font='Helvetica 12 bold', show='*'", 
                                                 "parent":"frame_1", 
                                                 "pack_config":"side='left', expand=True, fill='x'"}, 

                                                {"type":"button", 
                                                 "widget_name":"password_entry_toggle", 
                                                 "class":"KeyToggle", 
                                                 "style_config":"style='toggle1.TButton', background='white', borderwidth=0, highlightthickness=0, padx=0, pady=0", 
                                                 "style_map_config":"style='toggle1.TButton', background=[(\"active\",\"white\")], foreground=[(\"disabled\",\"gray\")]", 
                                                 "config":"style='toggle1.TButton', padding=0", 
                                                 "command": "command_str='set_entry_visibility', args='(self.widget_references[\"password_entry_toggle\"], self.widget_references[\"password_entry\"],)', execute_on_load=True, first=True", 
                                                 "binds":[{"bind_config":"event='<Button-1>', callback_str='toggle_entry_visibility', args='(self.widget_references[\"password_entry_toggle\"], self.widget_references[\"password_entry\"],)'"}], 
                                                 "parent":"frame_1", 
                                                 "pack_config":"side='left', padx=(5, 0), pady=(0, 5)"}, 

                                                #{'type': 'entry', 
                                                # "config":"{}".format(f"show={show}" if show else ''), 
                                                # "binds":[{"bind_config":"event='<Return>',  callback_str='lambda e:self.submit_entry'"}],
                                                # "grid_config":"column=0, columnspan=2, sticky='we', pady=(10, 0)"},

                                                {'type': 'button', 
                                                 "config":"text='Submit'", 
                                                 "command":"command_str=self.submit_entry", 
                                                 "grid_config":"row=2, column=0, sticky='ew', padx=(0, 5), pady=(10, 0)"},

                                                {'type': 'button', 
                                                 "config":"text='Cancel'", 
                                                 "command":"command_str=self.cancel", 
                                                 "grid_config":"row=2, column=1, sticky='ew', padx=(5, 0), pady=(10, 0)"}
                                                                                              ], callbacks={"set_entry_visibility":self.dialog_functions.set_entry_visibility, "toggle_entry_visibility":self.dialog_functions.toggle_entry_visibility}, classes={"KeyToggle":KeyToggle}).result
        
        if is_callback:
                self.root.stored_data.ask_string_result = result[0]
                self.root.wallet_thread_manager.dialog_event.set()
        else:
            return result[0]
        

    def password_dialog_with_confirmation(self, title=None, msg=None, is_callback=False):
        while True:
            result, _, _ = CustomDialog(parent=self.root, title=title, 
                        prompt=[
                                {"type":"label", 
                                "config":"text={}".format(msg), 
                                "grid_config":"column=0, sticky='w', pady=(20, 0)"}, 

                                {"type":"label", 
                                "config":"text='Enter Password:', font='Helvetica 10 bold'", 
                                "grid_config":"column=0, sticky='w', pady=(20, 0)"}, 
                                
                                {"type":"frame", 
                                 "widget_name":"frame_1", 
                                 "grid_config":"column=0, columnspan=2, sticky='nswe', pady=(0, 0)"}, 
                                                 
                                {"type":"entry", 
                                 "widget_name":"password_1_entry", 
                                 "config":"font='Helvetica 12 bold', show='*'", 
                                 "binds":[{"bind_config":"event='<Tab>', callback_str='focus_next_widget'"}, {"bind_config":"event='<space>', callback_str='focus_next_widget'"}], 
                                 "parent":"frame_1", 
                                 "pack_config":"side='left', expand=True, fill='x'"}, 

                                {"type":"button", 
                                 "widget_name":"password_1_entry_toggle", 
                                 "class":"KeyToggle", 
                                 "style_config":"style='toggle1.TButton', background='white', borderwidth=0, highlightthickness=0, padx=0, pady=0", 
                                 "style_map_config":"style='toggle1.TButton', background=[(\"active\",\"white\")], foreground=[(\"disabled\",\"gray\")]", 
                                 "config":"style='toggle1.TButton', padding=0", 
                                 "command": "command_str='set_entry_visibility', args='(self.widget_references[\"password_1_entry_toggle\"], self.widget_references[\"password_1_entry\"],)', execute_on_load=True, first=True", 
                                 "binds":[{"bind_config":"event='<Button-1>', callback_str='toggle_entry_visibility', args='(self.widget_references[\"password_1_entry_toggle\"], self.widget_references[\"password_1_entry\"],)'"}], 
                                 "parent":"frame_1", 
                                 "pack_config":"side='left', padx=(5, 0), pady=(0, 5)"}, 
                                
                                {"type":"label", 
                                "config":"text='Confirm Password:', font='Helvetica 10 bold'", 
                                "grid_config":"column=0, sticky='w', pady=(20, 0)"},
                                
                                {"type":"frame", 
                                 "widget_name":"frame_2", 
                                 "grid_config":"column=0, columnspan=2, sticky='nswe', pady=(0, 0)"}, 
                                                 
                                {"type":"entry", 
                                 "widget_name":"password_2_entry", 
                                 "config":"font='Helvetica 12 bold', show='*'", 
                                 "binds":[{"bind_config":"event='<Tab>', callback_str='focus_next_widget'"}, {"bind_config":"event='<space>', callback_str='focus_next_widget'"}], 
                                 "parent":"frame_2", 
                                 "pack_config":"side='left', expand=True, fill='x'"}, 

                                {"type":"button", 
                                 "widget_name":"password_2_entry_toggle", 
                                 "class":"KeyToggle", 
                                 "style_config":"style='toggle1.TButton', background='white', borderwidth=0, highlightthickness=0, padx=0, pady=0", 
                                 "style_map_config":"style='toggle1.TButton', background=[(\"active\",\"white\")], foreground=[(\"disabled\",\"gray\")]", 
                                 "config":"style='toggle1.TButton', padding=0", 
                                 "command": "command_str='set_entry_visibility', args='(self.widget_references[\"password_2_entry_toggle\"], self.widget_references[\"password_2_entry\"],)', execute_on_load=True, first=True", 
                                 "binds":[{"bind_config":"event='<Button-1>', callback_str='toggle_entry_visibility', args='(self.widget_references[\"password_2_entry_toggle\"], self.widget_references[\"password_2_entry\"],)'"}], 
                                 "parent":"frame_2", 
                                 "pack_config":"side='left', padx=(5, 0), pady=(0, 5)"},
    
                                {"type":"frame", 
                                 "widget_name":"frame_3", 
                                 "grid_config":"column=0, sticky='we', pady=(20, 0)"},                              
    
                                {'type': 'button', 
                                 "config":"text='Submit', width=20", 
                                 "command":"command_str=self.submit_entry", 
                                 "parent":"frame_3",
                                 "pack_config":"side='left', expand=True, fill=x, padx=(0, 5)"},
    
                                {'type': 'button', 
                                 "config":"text='Cancel', width=20", 
                                 "command":"command_str=self.cancel", 
                                 "parent":"frame_3",
                                 "pack_config":"side='right', expand=True, fill=x, padx=(5, 0)"},                                  
                                ], callbacks={"focus_next_widget":self.dialog_functions.focus_next_widget, "set_entry_visibility":self.dialog_functions.set_entry_visibility, "toggle_entry_visibility":self.dialog_functions.toggle_entry_visibility}, classes={"KeyToggle":KeyToggle}).result
            
            if result[0] is None:
                password = None
                break
                
            if result[0] == '':
                self.messagebox('Error', 'No password provided.')
                continue
    
            if result[1] != result[0] or result[1] is None:
                self.messagebox('Error', 'Passwords do not match.')
                continue
            password = result[0]
            break
        if is_callback:
            self.root.stored_data.ask_string_result = password
            self.root.wallet_thread_manager.dialog_event.set()
        else:
            return password


    def confirmation_prompt(self, title, msg=None, msg_2=None, is_callback=False):
        result, _, _ = CustomDialog(parent=self.root, title=title, 
                                    prompt=[
                                            {"type": "label", 
                                             "config":"text={}".format(msg), 
                                             "grid_config":"column=0"},
                                            
                                            {"type":"frame", 
                                             "widget_name":"frame_1", 
                                             "grid_config":"column=0",
                                             "hidden":False if msg_2 else True},
                                            
                                            {"type":"entry",
                                             "config":"style='addressInfo.TEntry', state='readonly', font='Helvetica 10 bold', justify='center'", 
                                             "style_map_config":"style='addressInfo.TEntry', lightcolor='[(\"focus\", \"white\")]'",
                                             "insert":"string='{}'".format(msg_2),
                                             "variables": {"expand_entry_width": True},
                                             "parent":"frame_1",
                                             "pack_config":"side='left', padx=(5, 5)"},
                                            
                                            {"type":"frame", 
                                             "widget_name":"frame_2", 
                                             "grid_config":"column=0, sticky='we'"},                                            
                                            
                                            {"type": "button", 
                                             "config":"text='Yes'", 
                                             "parent":"frame_2",
                                             "command":"command_str=self.submit_entry", 
                                             "pack_config":"side='left', fill='x', expand=True, padx=(5, 0), pady=(0, 5)"},                                            
                                            
                                            {"type": "button", 
                                             "config":"text='No'",
                                             "parent":"frame_2",
                                             "command":"command_str=self.cancel", 
                                             "pack_config":"side='left', fill='x', expand=True, padx=(5, 0), pady=(0, 5)"}
                                            ], true_on_submit=True).result
        
        if is_callback:
                self.root.stored_data.ask_bool_result = result[0]
                self.root.wallet_thread_manager.dialog_event.set()
        else:
            return result[0]


    def ask_string(self, title, msg, show, is_callback):
        # This is called by the main thread to  show the dialog
        result, _, _ = CustomDialog(parent=self.root, title=title, 
                                        prompt=[
                                                {'type': 'label', 
                                                 "config":"text={}".format(msg), 
                                                 "grid_config":"column=0, columnspan=2"},

                                                {'type': 'entry', 
                                                 "config":"{}".format(f"show={show}" if show else ''), 
                                                 "binds":[{"bind_config":"event='<Return>',  callback_str='lambda e:self.submit_entry'"}],
                                                 "grid_config":"column=0, columnspan=2, sticky='we', pady=(10, 0)"},

                                                {'type': 'button', 
                                                 "config":"text='Submit'", 
                                                 "command":"command_str=self.submit_entry", 
                                                 "grid_config":"row=2, column=0, sticky='ew', padx=(0, 5), pady=(10, 0)"},

                                                {'type': 'button', 
                                                 "config":"text='Cancel'", 
                                                 "command":"command_str=self.cancel", 
                                                 "grid_config":"row=2, column=1, sticky='ew', padx=(5, 0), pady=(10, 0)"}
                                               ]).result
        
        if is_callback:
                self.root.stored_data.ask_string_result = result[0]
                self.root.wallet_thread_manager.dialog_event.set()
        else:
            return result[0]


    def tx_confirmation_dialog(self, sender=None, receiver=None, amount=None, is_callback=False):
        result, disable_dialog, _ = CustomDialog(parent=self.root, 
                                        title="Confirm Transaction", 
                                        prompt=[
                                                {'type': 'label', 
                                                 "config":"text='Are you sure you want to execute this transaction?', font='Helvetica 12 bold'", 
                                                 "grid_config":"column=0, columnspan=2"},
                                                
                                                {'type': 'label', 
                                                 "config": "text='From: {}\n\nTo: {}'".format(sender, receiver), 
                                                 "grid_config":"column=0, columnspan=2, sticky='w', pady=(10, 0)"},

                                                {'type': 'separator', 
                                                 "config":"orient='horizontal'", 
                                                 "grid_config":"column=0, columnspan=2, sticky='we', pady=(10, 0)"},

                                                {'type': 'label', 
                                                 "config":"text='Amount: {} DNR', font='Helvetica 12 bold'".format(amount), 
                                                 "grid_config":"column=0, columnspan=2, sticky='w', pady=(5, 0)"},

                                                {'type': 'checkbox', 
                                                 "config":"text='Do not show this dialog box for future transactions (This session only)'", 
                                                 "grid_config":"column=0, columnspan=2, sticky='w', pady=(10, 0)"},

                                                {'type': 'button', 
                                                 "config":"text='Yes'", 
                                                 "command":"command_str=self.submit_entry", 
                                                 "grid_config":"row=6, column=0, sticky='ew', padx=(0, 5), pady=(10, 0)"},

                                                {'type': 'button', "config":"text='No'", 
                                                 "command":"command_str=self.cancel", 
                                                 "grid_config":"row=6, column=1, sticky='ew', padx=(5, 0), pady=(10, 0)"}                                                
                                               ], true_on_submit=True).result
        
        if is_callback:
                self.root.stored_data.disable_tx_confirmation_dialog = disable_dialog[0]
                self.root.stored_data.ask_string_result = result[0]
                self.root.wallet_thread_manager.dialog_event.set()
        else:
            return result[0], disable_dialog[0]
        

    def input_listener_dialog(self, is_callback=False):
        result, _, _ = CustomDialog(parent=self.root, title='Wallet Annihilation', 
                                    prompt=[
                                            {"type": "label",
                                             "widget_name":"label_1",
                                             "config":"", 
                                             "command": "command_str='input_listener_callback', args='(self.widget_references[\"label_1\"],self.master,)', execute_on_load=True",
                                             "binds":[{"bind_config":"event='<Unmap>', callback_str='self.cancel'"}],
                                             "grid_config":"column=0, columnspan=2"},
                                            
                                            {"type": "label", 
                                             "widget_name":"label_2",
                                             "binds": [{"bind_config":"event='<Unmap>', callback_str='self.submit_entry'"}],
                                             "grid_config":"row=0, column=0, columnspan=2"},

                                            {"type":"self.master",
                                             "binds":[{"bind_config":"event='<KeyRelease>', callback_str='input_listener_submit', args='(self.widget_references[\"label_2\"],)'"}]},
                                           ], true_on_submit=True, callbacks={"input_listener_callback":self.dialog_functions.input_listener_callback, "input_listener_submit":self.dialog_functions.input_listener_submit}).result
        
        self.root.stored_data.input_listener_submit = False
        self.root.stored_data.input_listener_time_remaining = None

        if is_callback:
            self.root.stored_data.ask_bool_result = result[0]
            self.root.wallet_thread_manager.dialog_event.set()
        else:
            return result[0]


    def backup_mnemonic_dialog(self, mnemonic=None, is_callback=False):
        word_list = mnemonic.split()
        while True:
            result, _, _ = CustomDialog(parent=self.root, title='Recovery Phrase Backup', 
                                        prompt=[
                                                
                                                #{"type":"frame", 
                                                # "widget_name":"frame_1", 
                                                # "grid_config":"column=0, sticky='we', pady=(10, 0)"}, 
                                                 
                                                {"type": "label",
                                                 #"parent":"frame_1",
                                                 "config":"text='The words below is the recovery phrase of the wallet.', justify='left'",
                                                 #"pack_config":"anchor='w'"},
                                                 "grid_config":"column=0"},
                                                
                                                {"type": "label",
                                                 #"parent":"frame_1",
                                                 "config":"text='They enable you to access your Denaro and restore your wallet.', justify='left'",
                                                 #"pack_config":"anchor='w'"},
                                                 "grid_config":"column=0"},
                                                
                                                {"type": "label",
                                                 #"parent":"frame_1",
                                                 "config":"text='Please write them down in the order shown.', justify='left'",
                                                 #"pack_config":"anchor='w'"},
                                                 "grid_config":"column=0"},
                                                
                                                {"type": "separator",
                                                 "config":"orient='horizontal'",
                                                 "grid_config":"column=0, sticky='we', pady=(5, 5)"},

                                                {"type":"frame", 
                                                 "widget_name":"frame_2", 
                                                 "grid_config":"column=0, pady=(10, 0)"}, 

                                                {"type":"label", 
                                                 "config":"text='1: ', font='Helvetica 12 bold'", 
                                                 "parent":"frame_2", 
                                                 "pack_config":"side='left'"}, 
                                                 
                                                {"type":"entry", 
                                                 "config":"style='addressInfo.TEntry', state='readonly', font='Helvetica 12 bold'", 
                                                 "style_map_config":"style='addressInfo.TEntry', lightcolor='[(\"focus\", \"white\")]'", 
                                                 "parent":"frame_2", 
                                                 "insert":"string='{}'".format(word_list[0]), 
                                                 #"variables": {"disable_context_menu_items": True},
                                                 "pack_config":"side='left'"}, 

                                                {"type":"label", 
                                                 "config":"text='2: ', font='Helvetica 12 bold'", 
                                                 "parent":"frame_2", 
                                                 "pack_config":"side='left'"}, 
                                                 
                                                {"type":"entry", 
                                                 "config":"style='addressInfo.TEntry', state='readonly', font='Helvetica 12 bold'", 
                                                 "parent":"frame_2", 
                                                 "insert":"string='{}'".format(word_list[1]), 
                                                 #"variables": {"disable_context_menu_items": True},
                                                 "pack_config":"side='left'"}, 

                                                {"type":"frame", 
                                                 "widget_name":"frame_3", 
                                                 "grid_config":"column=0, pady=(10, 0)"}, 

                                                {"type":"label", 
                                                 "config":"text='3: ', font='Helvetica 12 bold'", 
                                                 "parent":"frame_3", 
                                                 "pack_config":"side='left'"}, 

                                                {"type":"entry", 
                                                 "config":"style='addressInfo.TEntry', state='readonly', font='Helvetica 12 bold'", 
                                                 "parent":"frame_3", 
                                                 "insert":"string='{}'".format(word_list[2]), 
                                                 #"variables": {"disable_context_menu_items": True},
                                                 "pack_config":"side='left'"}, 
                                                 
                                                {"type":"label", 
                                                 "config":"text='4: ', font='Helvetica 12 bold'", 
                                                 "parent":"frame_3", 
                                                 "pack_config":"side='left'"}, 

                                                {"type":"entry", 
                                                 "config":"style='addressInfo.TEntry', state='readonly', font='Helvetica 12 bold'", 
                                                 "parent":"frame_3", 
                                                 "insert":"string='{}'".format(word_list[3]), 
                                                 #"variables": {"disable_context_menu_items": True},
                                                 "pack_config":"side='left'"}, 

                                                {"type":"frame", 
                                                 "widget_name":"frame_4", 
                                                 "grid_config":"column=0, pady=(10, 0)"}, 

                                                {"type":"label", 
                                                 "config":"text='5: ', font='Helvetica 12 bold'", 
                                                 "parent":"frame_4", 
                                                 "pack_config":"side='left'"}, 

                                                {"type":"entry", 
                                                 "config":"style='addressInfo.TEntry', state='readonly', font='Helvetica 12 bold'", 
                                                 "parent":"frame_4", 
                                                 "insert":"string='{}'".format(word_list[4]), 
                                                 #"variables": {"disable_context_menu_items": True},
                                                 "pack_config":"side='left'"}, 

                                                {"type":"label", 
                                                 "config":"text='6: ', font='Helvetica 12 bold'", 
                                                 "parent":"frame_4", 
                                                 "pack_config":"side='left'"}, 

                                                {"type":"entry", 
                                                 "config":"style='addressInfo.TEntry', state='readonly', font='Helvetica 12 bold'", 
                                                 "parent":"frame_4", 
                                                 "insert":"string='{}'".format(word_list[5]), 
                                                 #"variables": {"disable_context_menu_items": True},
                                                 "pack_config":"side='left'"}, 

                                                {"type":"frame", 
                                                 "widget_name":"frame_5", 
                                                 "grid_config":"column=0, pady=(10, 0)"}, 

                                                {"type":"label", 
                                                 "config":"text='7: ', font='Helvetica 12 bold'", 
                                                 "parent":"frame_5", 
                                                 "pack_config":"side='left'"}, 

                                                {"type":"entry", 
                                                 "config":"style='addressInfo.TEntry', state='readonly', font='Helvetica 12 bold'", 
                                                 "parent":"frame_5", 
                                                 "insert":"string='{}'".format(word_list[6]), 
                                                 #"variables": {"disable_context_menu_items": True},
                                                 "pack_config":"side='left'"}, 

                                                {"type":"label", 
                                                 "config":"text='8: ', font='Helvetica 12 bold'", 
                                                 "parent":"frame_5", 
                                                 "pack_config":"side='left'"}, 

                                                {"type":"entry", 
                                                 "config":"style='addressInfo.TEntry', state='readonly', font='Helvetica 12 bold'", 
                                                 "parent":"frame_5", 
                                                 "insert":"string='{}'".format(word_list[7]), 
                                                 #"variables": {"disable_context_menu_items": True},
                                                 "pack_config":"side='left'"}, 

                                                {"type":"frame", 
                                                 "widget_name":"frame_6", 
                                                 "grid_config":"column=0, pady=(10, 0)"}, 

                                                {"type":"label", 
                                                 "config":"text='9: ', font='Helvetica 12 bold'", 
                                                 "parent":"frame_6", 
                                                 "pack_config":"side='left'"}, 

                                                {"type":"entry", 
                                                 "config":"style='addressInfo.TEntry', state='readonly', font='Helvetica 12 bold'", 
                                                 "parent":"frame_6", 
                                                 "insert":"string='{}'".format(word_list[8]), 
                                                 #"variables": {"disable_context_menu_items": True},
                                                 "pack_config":"side='left'"}, 

                                                {"type":"label", 
                                                 "config":"text='10:', font='Helvetica 11 bold'", 
                                                 "parent":"frame_6", 
                                                 "pack_config":"side='left'"}, 

                                                {"type":"entry", 
                                                 "config":"style='addressInfo.TEntry', state='readonly', font='Helvetica 12 bold'", 
                                                 "parent":"frame_6", 
                                                 "insert":"string='{}'".format(word_list[9]), 
                                                 #"variables": {"disable_context_menu_items": True},
                                                 "pack_config":"side='left'"}, 

                                                {"type":"frame", 
                                                 "widget_name":"frame_7", 
                                                 "grid_config":"column=0, pady=(10, 0)"}, 

                                                {"type":"label", 
                                                 "config":"text='11:', font='Helvetica 11 bold'", 
                                                 "parent":"frame_7", 
                                                 "pack_config":"side='left'"}, 

                                                {"type":"entry", 
                                                 "config":"style='addressInfo.TEntry', state='readonly', font='Helvetica 12 bold'", 
                                                 "parent":"frame_7", 
                                                 "insert":"string='{}'".format(word_list[10]), 
                                                 #"variables": {"disable_context_menu_items": True},
                                                 "pack_config":"side='left'"}, 

                                                {"type":"label", 
                                                 "config":"text='12:', font='Helvetica 11 bold'", 
                                                 "parent":"frame_7", 
                                                 "pack_config":"side='left'"}, 

                                                {"type":"entry", 
                                                 "config":"style='addressInfo.TEntry', state='readonly', font='Helvetica 12 bold'", 
                                                 "parent":"frame_7", 
                                                 "insert":"string='{}'".format(word_list[11]), 
                                                 #"variables": {"disable_context_menu_items": True},
                                                 "pack_config":"side='left'"},
                                                
                                                {"type": "separator",
                                                 "config":"orient='horizontal'",
                                                 "grid_config":"column=0, sticky='we', pady=(15, 0)"},
                                                
                                                {"type":"frame", 
                                                 "widget_name":"frame_8", 
                                                 "grid_config":"column=0, sticky='w', pady=(10, 0)"}, 
                                                
                                                {"type":"label", 
                                                 "config":"text='', font='Helvetica 11 bold'",
                                                 "widget_name":"copied_mnemonic_label",  
                                                 "parent":"frame_8", 
                                                 "pack_config":"side='right', padx=(10, 0)"}, 

                                                {"type": "button", 
                                                 "config":"text='Copy to clipboard'", 
                                                 "parent":"frame_8", 
                                                 "binds":[{"bind_config":"event='<Button-1>', callback_str='copy_mnemonic_to_clipboard', args='(\"{}\", self.widget_references[\"copied_mnemonic_label\"],)'".format(mnemonic)}], 
                                                 "pack_config":"side='left'"},
                                                
                                                {"type":"frame", 
                                                 "widget_name":"frame_9", 
                                                 "grid_config":"column=0, sticky='we', pady=(10, 0)"},

                                                 {"type": "button", 
                                                 "config":"text='Cancel'", 
                                                 "parent":"frame_9", 
                                                 "command":"command_str=self.cancel", 
                                                 "pack_config":"side='left', padx=(0, 5), fill='x', expand=True"},

                                                {"type": "button", 
                                                 "config":"text='Next'", 
                                                 "parent":"frame_9", 
                                                 "command":"command_str=self.submit_entry", 
                                                 "pack_config":"side='left', padx=(5, 0), fill='x', expand=True"},
                                               ], true_on_submit=True, callbacks={"copy_mnemonic_to_clipboard": self.dialog_functions.copy_mnemonic_to_clipboard}).result
            if result[0] is None:
                if is_callback:
                    self.root.stored_data.ask_bool_result = False
                    self.root.wallet_thread_manager.dialog_event.set()
                    break
                else:
                    return False

            if self.confirm_mnemonic_dialog(mnemonic=word_list):
                if is_callback:
                    self.root.stored_data.ask_bool_result = True
                    self.root.wallet_thread_manager.dialog_event.set()
                    break
                else:
                    return True
            else:
                if self.root.stored_data.confirm_mnemonic_back_button_press:
                    self.root.stored_data.confirm_mnemonic_back_button_press = False
                    continue
                
                if is_callback:
                    self.root.stored_data.ask_bool_result = False
                    self.root.wallet_thread_manager.dialog_event.set()
                    break
                else:
                    return False


    def confirm_mnemonic_dialog(self, mnemonic=None, is_callback=False ):
        while True:
            #word_list = mnemonic.split()
            result, _, _ = CustomDialog(parent=self.root, title='Recovery Phrase Backup', 
                                        prompt=[
                                                {"type": "label", 
                                                 "config":"text='Please confirm your recovery phrase.'", 
                                                 "grid_config":"column=0"}, 

                                                {"type": "separator", 
                                                 "config":"orient='horizontal'", 
                                                 "grid_config":"column=0, sticky='we', pady=(5, 5)"}, 

                                                {"type":"frame", 
                                                 "widget_name":"frame_2", 
                                                 "grid_config":"column=0, sticky='we', pady=(10, 0)"}, 

                                                {"type":"label", 
                                                 "config":"text='1: ', font='Helvetica 12 bold'", 
                                                 "parent":"frame_2", 
                                                 "pack_config":"side='left'"}, 
                                                 
                                                {"type":"entry", 
                                                 "widget_name":"word_1", 
                                                 "config":"font='Helvetica 12 bold', show='*'", 
                                                 "binds":[{"bind_config":"event='<Tab>', callback_str='focus_next_widget'"}, {"bind_config":"event='<space>', callback_str='focus_next_widget'"}], 
                                                 "parent":"frame_2", 
                                                 "pack_config":"side='left'"}, 

                                                {"type":"button", 
                                                 "widget_name":"word_1_toggle", 
                                                 "class":"KeyToggle", 
                                                 "style_config":"style='toggle1.TButton', background='white', borderwidth=0, highlightthickness=0, padx=0, pady=0", 
                                                 "style_map_config":"style='toggle1.TButton', background=[(\"active\",\"white\")], foreground=[(\"disabled\",\"gray\")]", 
                                                 "config":"style='toggle1.TButton', padding=0", 
                                                 "command": "command_str='set_entry_visibility', args='(self.widget_references[\"word_1_toggle\"], self.widget_references[\"word_1\"],)', execute_on_load=True, first=True", 
                                                 "binds":[{"bind_config":"event='<Button-1>', callback_str='toggle_entry_visibility', args='(self.widget_references[\"word_1_toggle\"], self.widget_references[\"word_1\"],)'"}], 
                                                 "parent":"frame_2", 
                                                 "pack_config":"side='left', padx=(5, 0), pady=(0, 5)"}, 

                                                {"type":"label", 
                                                 "config":"text='2: ', font='Helvetica 12 bold'", 
                                                 "parent":"frame_2", 
                                                 "pack_config":"side='left', padx=(50, 0)"}, 
                                                 
                                                {"type":"entry", 
                                                 "widget_name":"word_2", 
                                                 "config":"font='Helvetica 12 bold', show='*'", 
                                                 "binds":[{"bind_config":"event='<Tab>', callback_str='focus_next_widget'"}, {"bind_config":"event='<space>', callback_str='focus_next_widget'"}], 
                                                 "parent":"frame_2", 
                                                 "pack_config":"side='left'"}, 

                                                {"type":"button", 
                                                 "widget_name":"word_2_toggle", 
                                                 "class":"KeyToggle", 
                                                 "style_config":"style='toggle1.TButton', background='white', borderwidth=0, highlightthickness=0, padx=0, pady=0", 
                                                 "style_map_config":"style='toggle1.TButton', background=[(\"active\",\"white\")], foreground=[(\"disabled\",\"gray\")]", 
                                                 "config":"style='toggle1.TButton', padding=0", 
                                                 "command": "command_str='set_entry_visibility', args='(self.widget_references[\"word_2_toggle\"], self.widget_references[\"word_2\"],)', execute_on_load=True, first=True", 
                                                 "binds":[{"bind_config":"event='<Button-1>', callback_str='toggle_entry_visibility', args='(self.widget_references[\"word_2_toggle\"], self.widget_references[\"word_2\"],)'"}], 
                                                 "parent":"frame_2", 
                                                 "pack_config":"side='left', padx=(5, 0), pady=(0, 5)"}, 

                                                {"type":"frame", 
                                                 "widget_name":"frame_3", 
                                                 "grid_config":"column=0, sticky='we', pady=(10, 0)"}, 

                                                {"type":"label", 
                                                 "config":"text='3: ', font='Helvetica 12 bold'", 
                                                 "parent":"frame_3", 
                                                 "pack_config":"side='left'"}, 

                                                {"type":"entry", 
                                                 "widget_name":"word_3", 
                                                 "config":"font='Helvetica 12 bold', show='*'", 
                                                 "binds":[{"bind_config":"event='<Tab>', callback_str='focus_next_widget'"}, {"bind_config":"event='<space>', callback_str='focus_next_widget'"}], 
                                                 "parent":"frame_3", 
                                                 "pack_config":"side='left'"}, 

                                                {"type":"button", 
                                                 "widget_name":"word_3_toggle", 
                                                 "class":"KeyToggle", 
                                                 "style_config":"style='toggle1.TButton', background='white', borderwidth=0, highlightthickness=0, padx=0, pady=0", 
                                                 "style_map_config":"style='toggle1.TButton', background=[(\"active\",\"white\")], foreground=[(\"disabled\",\"gray\")]", 
                                                 "config":"style='toggle1.TButton', padding=0", 
                                                 "command": "command_str='set_entry_visibility', args='(self.widget_references[\"word_3_toggle\"], self.widget_references[\"word_3\"],)', execute_on_load=True, first=True", 
                                                 "binds":[{"bind_config":"event='<Button-1>', callback_str='toggle_entry_visibility', args='(self.widget_references[\"word_3_toggle\"], self.widget_references[\"word_3\"],)'"}], 
                                                 "parent":"frame_3", 
                                                 "pack_config":"side='left', padx=(5, 0), pady=(0, 5)"}, 

                                                {"type":"label", 
                                                 "config":"text='4: ', font='Helvetica 12 bold'", 
                                                 "parent":"frame_3", 
                                                 "pack_config":"side='left', padx=(50, 0)"}, 

                                                {"type":"entry", 
                                                 "widget_name":"word_4", 
                                                 "config":"font='Helvetica 12 bold', show='*'", 
                                                 "binds":[{"bind_config":"event='<Tab>', callback_str='focus_next_widget'"}, {"bind_config":"event='<space>', callback_str='focus_next_widget'"}], 
                                                 "parent":"frame_3", 
                                                 "pack_config":"side='left'"}, 

                                                {"type":"button", 
                                                 "widget_name":"word_4_toggle", 
                                                 "class":"KeyToggle", 
                                                 "style_config":"style='toggle1.TButton', background='white', borderwidth=0, highlightthickness=0, padx=0, pady=0", 
                                                 "style_map_config":"style='toggle1.TButton', background=[(\"active\",\"white\")], foreground=[(\"disabled\",\"gray\")]", 
                                                 "config":"style='toggle1.TButton', padding=0", 
                                                 "command": "command_str='set_entry_visibility', args='(self.widget_references[\"word_4_toggle\"], self.widget_references[\"word_4\"],)', execute_on_load=True, first=True", 
                                                 "binds":[{"bind_config":"event='<Button-1>', callback_str='toggle_entry_visibility', args='(self.widget_references[\"word_4_toggle\"], self.widget_references[\"word_4\"],)'"}], 
                                                 "parent":"frame_3", 
                                                 "pack_config":"side='left', padx=(5, 0), pady=(0, 5)"}, 

                                                {"type":"frame", 
                                                 "widget_name":"frame_4", 
                                                 "grid_config":"column=0, sticky='we', pady=(10, 0)"}, 

                                                {"type":"label", 
                                                 "config":"text='5: ', font='Helvetica 12 bold'", 
                                                 "parent":"frame_4", 
                                                 "pack_config":"side='left'"}, 

                                                {"type":"entry", 
                                                 "widget_name":"word_5", 
                                                 "config":"font='Helvetica 12 bold', show='*'", 
                                                 "binds":[{"bind_config":"event='<Tab>', callback_str='focus_next_widget'"}, {"bind_config":"event='<space>', callback_str='focus_next_widget'"}], 
                                                 "parent":"frame_4", 
                                                 "pack_config":"side='left'"}, 

                                                {"type":"button", 
                                                 "widget_name":"word_5_toggle", 
                                                 "class":"KeyToggle", 
                                                 "style_config":"style='toggle1.TButton', background='white', borderwidth=0, highlightthickness=0, padx=0, pady=0", 
                                                 "style_map_config":"style='toggle1.TButton', background=[(\"active\",\"white\")], foreground=[(\"disabled\",\"gray\")]", 
                                                 "config":"style='toggle1.TButton', padding=0", 
                                                 "command": "command_str='set_entry_visibility', args='(self.widget_references[\"word_5_toggle\"], self.widget_references[\"word_5\"],)', execute_on_load=True, first=True", 
                                                 "binds":[{"bind_config":"event='<Button-1>', callback_str='toggle_entry_visibility', args='(self.widget_references[\"word_5_toggle\"], self.widget_references[\"word_5\"],)'"}], 
                                                 "parent":"frame_4", 
                                                 "pack_config":"side='left', padx=(5, 0), pady=(0, 5)"}, 

                                                {"type":"label", 
                                                 "config":"text='6: ', font='Helvetica 12 bold'", 
                                                 "parent":"frame_4", 
                                                 "pack_config":"side='left', padx=(50, 0)"}, 

                                                {"type":"entry", 
                                                 "widget_name":"word_6", 
                                                 "config":"font='Helvetica 12 bold', show='*'", 
                                                 "binds":[{"bind_config":"event='<Tab>', callback_str='focus_next_widget'"}, {"bind_config":"event='<space>', callback_str='focus_next_widget'"}], 
                                                 "parent":"frame_4", 
                                                 "pack_config":"side='left'"}, 

                                                {"type":"button", 
                                                 "widget_name":"word_6_toggle", 
                                                 "class":"KeyToggle", 
                                                 "style_config":"style='toggle1.TButton', background='white', borderwidth=0, highlightthickness=0, padx=0, pady=0", 
                                                 "style_map_config":"style='toggle1.TButton', background=[(\"active\",\"white\")], foreground=[(\"disabled\",\"gray\")]", 
                                                 "config":"style='toggle1.TButton', padding=0", 
                                                 "command": "command_str='set_entry_visibility', args='(self.widget_references[\"word_6_toggle\"], self.widget_references[\"word_6\"],)', execute_on_load=True, first=True", 
                                                 "binds":[{"bind_config":"event='<Button-1>', callback_str='toggle_entry_visibility', args='(self.widget_references[\"word_6_toggle\"], self.widget_references[\"word_6\"],)'"}], 
                                                 "parent":"frame_4", 
                                                 "pack_config":"side='left', padx=(5, 0), pady=(0, 5)"}, 

                                                {"type":"frame", 
                                                 "widget_name":"frame_5", 
                                                 "grid_config":"column=0, sticky='we', pady=(10, 0)"}, 

                                                {"type":"label", 
                                                 "config":"text='7: ', font='Helvetica 12 bold'", 
                                                 "parent":"frame_5", 
                                                 "pack_config":"side='left'"}, 

                                                {"type":"entry", 
                                                 "widget_name":"word_7", 
                                                 "config":"font='Helvetica 12 bold', show='*'", 
                                                 "binds":[{"bind_config":"event='<Tab>', callback_str='focus_next_widget'"}, {"bind_config":"event='<space>', callback_str='focus_next_widget'"}], 
                                                 "parent":"frame_5", 
                                                 "pack_config":"side='left'"}, 

                                                {"type":"button", 
                                                 "widget_name":"word_7_toggle", 
                                                 "class":"KeyToggle", 
                                                 "style_config":"style='toggle1.TButton', background='white', borderwidth=0, highlightthickness=0, padx=0, pady=0", 
                                                 "style_map_config":"style='toggle1.TButton', background=[(\"active\",\"white\")], foreground=[(\"disabled\",\"gray\")]", 
                                                 "config":"style='toggle1.TButton', padding=0", 
                                                 "command": "command_str='set_entry_visibility', args='(self.widget_references[\"word_7_toggle\"], self.widget_references[\"word_7\"],)', execute_on_load=True, first=True", 
                                                 "binds":[{"bind_config":"event='<Button-1>', callback_str='toggle_entry_visibility', args='(self.widget_references[\"word_7_toggle\"], self.widget_references[\"word_7\"],)'"}], 
                                                 "parent":"frame_5", 
                                                 "pack_config":"side='left', padx=(5, 0), pady=(0, 5)"}, 

                                                {"type":"label", 
                                                 "config":"text='8: ', font='Helvetica 12 bold'", 
                                                 "parent":"frame_5", 
                                                 "pack_config":"side='left', padx=(50, 0)"}, 

                                                {"type":"entry", 
                                                 "widget_name":"word_8", 
                                                 "config":"font='Helvetica 12 bold', show='*'", 
                                                 "binds":[{"bind_config":"event='<Tab>', callback_str='focus_next_widget'"}, {"bind_config":"event='<space>', callback_str='focus_next_widget'"}], 
                                                 "parent":"frame_5", 
                                                 "pack_config":"side='left'"}, 

                                                {"type":"button", 
                                                 "widget_name":"word_8_toggle", 
                                                 "class":"KeyToggle", 
                                                 "style_config":"style='toggle1.TButton', background='white', borderwidth=0, highlightthickness=0, padx=0, pady=0", 
                                                 "style_map_config":"style='toggle1.TButton', background=[(\"active\",\"white\")], foreground=[(\"disabled\",\"gray\")]", 
                                                 "config":"style='toggle1.TButton', padding=0", 
                                                 "command": "command_str='set_entry_visibility', args='(self.widget_references[\"word_8_toggle\"], self.widget_references[\"word_8\"],)', execute_on_load=True, first=True", 
                                                 "binds":[{"bind_config":"event='<Button-1>', callback_str='toggle_entry_visibility', args='(self.widget_references[\"word_8_toggle\"], self.widget_references[\"word_8\"],)'"}], 
                                                 "parent":"frame_5", 
                                                 "pack_config":"side='left', padx=(5, 0), pady=(0, 5)"}, 

                                                {"type":"frame", 
                                                 "widget_name":"frame_6", 
                                                 "grid_config":"column=0, sticky='we', pady=(10, 0)"}, 

                                                {"type":"label", 
                                                 "config":"text='9: ', font='Helvetica 12 bold'", 
                                                 "parent":"frame_6", 
                                                 "pack_config":"side='left'"}, 

                                                {"type":"entry", 
                                                 "widget_name":"word_9", 
                                                 "config":"font='Helvetica 12 bold', show='*'", 
                                                 "binds":[{"bind_config":"event='<Tab>', callback_str='focus_next_widget'"}, {"bind_config":"event='<space>', callback_str='focus_next_widget'"}], 
                                                 "parent":"frame_6", 
                                                 "pack_config":"side='left'"}, 
                                                 
                                                {"type":"button", 
                                                 "widget_name":"word_9_toggle", 
                                                 "class":"KeyToggle", 
                                                 "style_config":"style='toggle1.TButton', background='white', borderwidth=0, highlightthickness=0, padx=0, pady=0", 
                                                 "style_map_config":"style='toggle1.TButton', background=[(\"active\",\"white\")], foreground=[(\"disabled\",\"gray\")]", 
                                                 "config":"style='toggle1.TButton', padding=0", 
                                                 "command": "command_str='set_entry_visibility', args='(self.widget_references[\"word_9_toggle\"], self.widget_references[\"word_9\"],)', execute_on_load=True, first=True", 
                                                 "binds":[{"bind_config":"event='<Button-1>', callback_str='toggle_entry_visibility', args='(self.widget_references[\"word_9_toggle\"], self.widget_references[\"word_9\"],)'"}], 
                                                 "parent":"frame_6", 
                                                 "pack_config":"side='left', padx=(5, 0), pady=(0, 5)"}, 

                                                {"type":"label", 
                                                 "config":"text='10:', font='Helvetica 11 bold'", 
                                                 "parent":"frame_6", 
                                                 "pack_config":"side='left', padx=(50, 0)"}, 

                                                {"type":"entry", 
                                                 "widget_name":"word_10", 
                                                 "config":"font='Helvetica 12 bold', show='*'", 
                                                 "binds":[{"bind_config":"event='<Tab>', callback_str='focus_next_widget'"}, {"bind_config":"event='<space>', callback_str='focus_next_widget'"}], 
                                                 "parent":"frame_6", 
                                                 "pack_config":"side='left'"}, 

                                                {"type":"button", 
                                                 "widget_name":"word_10_toggle", 
                                                 "class":"KeyToggle", 
                                                 "style_config":"style='toggle1.TButton', background='white', borderwidth=0, highlightthickness=0, padx=0, pady=0", 
                                                 "style_map_config":"style='toggle1.TButton', background=[(\"active\",\"white\")], foreground=[(\"disabled\",\"gray\")]", 
                                                 "config":"style='toggle1.TButton', padding=0", 
                                                 "command": "command_str='set_entry_visibility', args='(self.widget_references[\"word_10_toggle\"], self.widget_references[\"word_10\"],)', execute_on_load=True, first=True", 
                                                 "binds":[{"bind_config":"event='<Button-1>', callback_str='toggle_entry_visibility', args='(self.widget_references[\"word_10_toggle\"], self.widget_references[\"word_10\"],)'"}], 
                                                 "parent":"frame_6", 
                                                 "pack_config":"side='left', padx=(5, 0), pady=(0, 5)"}, 

                                                {"type":"frame", 
                                                 "widget_name":"frame_7", 
                                                 "grid_config":"column=0, sticky='we', pady=(10, 0)"}, 

                                                {"type":"label", 
                                                 "config":"text='11:', font='Helvetica 11 bold'", 
                                                 "parent":"frame_7", 
                                                 "pack_config":"side='left'"}, 

                                                {"type":"entry", 
                                                 "widget_name":"word_11", 
                                                 "config":"font='Helvetica 12 bold', show='*'", 
                                                 "binds":[{"bind_config":"event='<Tab>', callback_str='focus_next_widget'"}, {"bind_config":"event='<space>', callback_str='focus_next_widget'"}], 
                                                 "parent":"frame_7", 
                                                 "pack_config":"side='left'"}, 

                                                {"type":"button", 
                                                 "widget_name":"word_11_toggle", 
                                                 "class":"KeyToggle", 
                                                 "style_config":"style='toggle1.TButton', background='white', borderwidth=0, highlightthickness=0, padx=0, pady=0", 
                                                 "style_map_config":"style='toggle1.TButton', background=[(\"active\",\"white\")], foreground=[(\"disabled\",\"gray\")]", 
                                                 "config":"style='toggle1.TButton', padding=0", 
                                                 "command": "command_str='set_entry_visibility', args='(self.widget_references[\"word_11_toggle\"], self.widget_references[\"word_11\"],)', execute_on_load=True, first=True", 
                                                 "binds":[{"bind_config":"event='<Button-1>', callback_str='toggle_entry_visibility', args='(self.widget_references[\"word_11_toggle\"], self.widget_references[\"word_11\"],)'"}], 
                                                 "parent":"frame_7", 
                                                 "pack_config":"side='left', padx=(5, 0), pady=(0, 5)"}, 

                                                {"type":"label", 
                                                 "config":"text='12:', font='Helvetica 11 bold'", 
                                                 "parent":"frame_7", 
                                                 "pack_config":"side='left', padx=(50, 0)"}, 

                                                {"type":"entry", 
                                                 "widget_name":"word_12", 
                                                 "config":"font='Helvetica 12 bold', show='*'", 
                                                 "binds":[{"bind_config":"event='<Tab>', callback_str='focus_next_widget'"}, {"bind_config":"event='<space>', callback_str='focus_next_widget'"}], 
                                                 "parent":"frame_7", 
                                                 "pack_config":"side='left'"}, 

                                                {"type":"button", 
                                                 "widget_name":"word_12_toggle", 
                                                 "class":"KeyToggle", 
                                                 "style_config":"style='toggle1.TButton', background='white', borderwidth=0, highlightthickness=0, padx=0, pady=0", 
                                                 "style_map_config":"style='toggle1.TButton', background=[(\"active\",\"white\")], foreground=[(\"disabled\",\"gray\")]", 
                                                 "config":"style='toggle1.TButton', padding=0", 
                                                 "command": "command_str='set_entry_visibility', args='(self.widget_references[\"word_12_toggle\"], self.widget_references[\"word_12\"],)', execute_on_load=True, first=True", 
                                                 "binds":[{"bind_config":"event='<Button-1>', callback_str='toggle_entry_visibility', args='(self.widget_references[\"word_12_toggle\"], self.widget_references[\"word_12\"],)'"}], 
                                                 "parent":"frame_7", 
                                                 "pack_config":"side='left', padx=(5, 0), pady=(0, 5)"},
                                                
                                                {"type": "separator",
                                                 "config":"orient='horizontal'",
                                                 "grid_config":"column=0, sticky='we', pady=(15, 0)"},
                                                 
                                                {"type":"frame", 
                                                 "widget_name":"frame_8", 
                                                 "grid_config":"column=0, sticky='we', pady=(10, 0)"}, 

                                                {"type": "button", 
                                                 "config":"text='Back'", 
                                                 "parent":"frame_8", 
                                                 "command":"command_str=self.submit_entry", 
                                                 "binds":[{"bind_config":"event='<Button-1>', callback_str='confirm_mnemonic_back_button_press'"}], 
                                                 "pack_config":"side='left', padx=(5, 5), pady=(0, 5), expand=True, fill='x'"}, 

                                                {"type": "button", 
                                                 "config":"text='Finish'", 
                                                 "parent":"frame_8", 
                                                 "command":"command_str=self.submit_entry", 
                                                 "pack_config":"side='left', padx=(5, 5), pady=(0, 5), expand=True, fill='x'"}, 
                                               ], callbacks={"focus_next_widget":self.dialog_functions.focus_next_widget, "set_entry_visibility":self.dialog_functions.set_entry_visibility, "toggle_entry_visibility":self.dialog_functions.toggle_entry_visibility, "confirm_mnemonic_back_button_press": self.dialog_functions.confirm_mnemonic_back_button_press}, classes={"KeyToggle":KeyToggle}).result
            if result[0] is None:
                return False                
            else:
                if self.root.stored_data.confirm_mnemonic_back_button_press:
                    return False
                if mnemonic != list(result):
                    self.messagebox(title="Error", msg="Recovery phrase is not correct.")
                    continue
                else:
                    return True
    
    def about_wallet_dialog(self):

        result, _, _ = CustomDialog(parent=self.root, title="About", 
                                    prompt=[

                                    {"type":"frame", 
                                     "widget_name":"frame_1", 
                                     "grid_config":"row=0, column=0, sticky='w', padx=(0, 10)"},
                                    
                                    {"type":"label", 
                                      "widget_name":"label_1",
                                      "config":"",
                                      "parent":"frame_1",
                                      "command": "command_str='set_label_image', args='(self.widget_references[\"label_1\"],\"./denaro/gui_assets/denaro_logo.png\",120,120,)', execute_on_load=True",
                                      "pack_config":"side='left'"},
                                    
                                    {"type":"frame", 
                                     "widget_name":"frame_2", 
                                     "grid_config":"row=0, column=1, sticky='w', padx=(0, 10)"},

                                    {'type': 'label', 
                                     "widget_name":"label_2",
                                     "parent":"frame_2",
                                     "config":"text='{}', anchor='w', justify='left'".format(f'\n{self.root.wallet_client_version}'), 
                                     "grid_config":"row=0, column=1, sticky='w'"},
                                    
                                    {"type":"frame", 
                                     "widget_name":"frame_3",
                                     "parent":"frame_2", 
                                     "class":"HyperlinkLabel",
                                     "class_config":"text=\"Copyright © 2023-2025 The-Sycorax (https://github.com/The-Sycorax)\", link_text=\"\", url=\"https://github.com/The-Sycorax\"",
                                     "grid_config":"row=1, column=1, sticky='w'"},

                                    {"type":"frame", 
                                     "widget_name":"frame_4",
                                     "parent":"frame_2", 
                                     "class":"HyperlinkLabel",
                                     "class_config":"text=\"\nThe source code for this wallet client is available at: https://github.com/The-Sycorax/DenaroWalletClient-GUI\", link_text=\"\", url=\"https://github.com/The-Sycorax/DenaroWalletClient-GUI\"",
                                     "grid_config":"row=2, column=1, sticky='w'"},

                                    {"type":"frame", 
                                     "widget_name":"frame_4",
                                     "parent":"frame_2", 
                                     "class":"HyperlinkLabel",
                                     "class_config":"text=\"The source code for the Denaro cryptocurrency is available at: https://github.com/denaro-coin/denaro\", link_text=\"\", url=\"https://github.com/denaro-coin/denaro\"",
                                     "grid_config":"row=3, column=1, sticky='w'"},

                                    {'type': 'label', 
                                     "parent":"frame_2",
                                     "config":"text='{}', justify='left'".format('\nThis is experimental software.'), 
                                     "grid_config":"row=4, column=1, sticky='w'"},

                                    {"type":"frame", 
                                     "widget_name":"frame_5",
                                     "parent":"frame_2", 
                                     "class":"HyperlinkLabel",
                                     "class_config":"text=\"Distributed under the MIT software license, see the accompanying LICENSE file or https://opensource.org/licenses/MIT\", link_text=\"\", url=\"https://opensource.org/licenses/MIT\"",
                                     "grid_config":"row=5, column=1, sticky='w'"},

                                    {'type': 'button', 
                                     "config":"text='Close'", 
                                     "command":"command_str=self.submit_entry", 
                                     "grid_config":"row=6, column=1, sticky='e', padx=(0, 10), pady=(75, 10)"}
                                     ], true_on_submit=True, callbacks={"set_label_image":self.dialog_functions.set_label_image, "set_hyperlink":self.dialog_functions.set_hyperlink}, classes={"HyperlinkLabel":HyperlinkLabel}).result
        
    def tfa_qr_code_dialog(self):
        pass
                
class DialogFunctions:
    def __init__(self, root, parent):
        self.root = root
        self.parent = parent
   
 
    # address_info functions
    def set_key_visibility(self, widget=None, entry=None, first=False):
        #self.print_variable_values(entry)
        
        if first:
            #widget.setvar(name='visibility_on', value='True')
            #self.toggle_key_visibility(widget, entry)
            entry.pack_forget()

        visibility_on = widget.visibility_on
        if visibility_on:
             visibility_img = Image.open("./denaro/gui_assets/visibility_on.png")
             visibility_img = visibility_img.resize((32, 32), Image.LANCZOS)
             visibility_img = ImageTk.PhotoImage(visibility_img)
             widget.config(image=visibility_img)
             widget.visibility_img = visibility_img
             
        else:
            visibility_img = Image.open("./denaro/gui_assets/visibility_off.png")
            visibility_img = visibility_img.resize((32, 32), Image.LANCZOS)
            visibility_img = ImageTk.PhotoImage(visibility_img)
            widget.config(image=visibility_img)
            widget.visibility_img = visibility_img
 
    
    def toggle_key_visibility(self, widget=None, entry=None, state=None):
        visibility_on = widget.visibility_on

        if visibility_on:
            widget.visibility_on = False
            self.set_key_visibility(widget, entry)
            entry.pack_forget()
        else:
            widget.visibility_on = True
            self.set_key_visibility(widget, entry)
            entry.pack(side='left')


    def set_entry_visibility(self, widget=None, entry=None, first=False):
        #self.print_variable_values(entry)
        
        if first:
            #widget.setvar(name='visibility_on', value='True')
            #self.toggle_key_visibility(widget, entry)
            entry.config(show='*')

        visibility_on = widget.visibility_on
        if visibility_on:
             visibility_img = Image.open("./denaro/gui_assets/visibility_on.png")
             visibility_img = visibility_img.resize((24, 24), Image.LANCZOS)
             visibility_img = ImageTk.PhotoImage(visibility_img)
             widget.config(image=visibility_img)
             widget.visibility_img = visibility_img
             
        else:
            visibility_img = Image.open("./denaro/gui_assets/visibility_off.png")
            visibility_img = visibility_img.resize((24, 24), Image.LANCZOS)
            visibility_img = ImageTk.PhotoImage(visibility_img)
            widget.config(image=visibility_img)
            widget.visibility_img = visibility_img
 
    
    def toggle_entry_visibility(self, widget=None, entry=None, state=None):
        visibility_on = widget.visibility_on

        if visibility_on:
            widget.visibility_on = False
            self.set_entry_visibility(widget, entry)
            entry.config(show='*')
        else:
            widget.visibility_on = True
            self.set_entry_visibility(widget, entry)
            entry.config(show='')
      

    def enable_2fa_checkbox(self, encryption_checkbox=None, _2fa_checkbox=None, state=None):
        # Get the state of the encryption checkbox
        encryption_state = encryption_checkbox.instate(['selected'])    
        # If encryption_checkbox is selected, enable _2fa_checkbox
        if encryption_state:
            _2fa_checkbox.state(['!disabled'])
        else:
            # If encryption_checkbox is not selected, disable and deselect _2fa_checkbox
            _2fa_checkbox.state(['disabled'])
            _2fa_checkbox.state(['!selected'])


    #input_listener_dialog functions 
    def input_listener_callback(self, label=None, master=None, state=None):
        master.focus_set()
        self.root.wallet_thread_manager.start_thread("input_listener_timer", self.input_listener_timer, args=(label,),)
        
    
    def input_listener_timer(self, stop_signal=None, label=None):
        while True:            
            #if self.root.stored_data.input_listener_submit:
            #    return
            if not self.root.stored_data.input_listener_submit or not (stop_signal and stop_signal.is_set()):
                if self.root.stored_data.input_listener_time_remaining == 0:
                    msg = f"Existing wallet data will be erased in {self.root.stored_data.input_listener_time_remaining} seconds.\nPress any key to cancel operation..."
                    try:
                        label.config(text=msg)
                        label.grid_remove() 
                    except tk.TclError:
                        pass
                    return       
                
                msg = f"Existing wallet data will be erased in {self.root.stored_data.input_listener_time_remaining} seconds.\nPress any key to cancel operation..."
                try:
                    label.config(text=msg)
                except tk.TclError:
                        pass
            else:
                return

            
    def input_listener_submit(self, label=None, state=None):
        self.root.stored_data.input_listener_submit = True
        if 'input_listener_timer' in self.root.event_handler.thread_event:
            self.root.wallet_thread_manager.stop_thread("input_listener_timer")
        label.grid_remove()
    
    
    def confirm_mnemonic_back_button_press(self, state=None):
        self.root.stored_data.confirm_mnemonic_back_button_press = True

    #DEBUG FUNCTIONS
    def get_config(self, widget):
        options = {}
        for i in widget.keys():
            value = widget.cget(i)
            options[i] = value.string if type(value) is _tkinter.Tcl_Obj else value
        return options, widget.winfo_parent()
    
    #def print_variable_values(self, widget):
    #        # Retrieve all variable names associated with the widget
    #    variable_names = widget.tk.splitlist(widget.tk.call('info', 'vars'))
    #    
    #    # Print the values of these variables
    #    for var_name in variable_names:
    #        try:
    #            # Check if the variable is not an array
    #            value = widget.getvar(var_name)
    #            print(f"Variable '{var_name}' has value: {value}")
    #        except tk.TclError as e:
    #            pass  
    
    def focus_next_widget(self, event, state=None):
        # Find the next widget in the focus order
        next_widget = event.widget.tk_focusNext()
        # Loop to skip over non-entry widgets (like buttons)
        while next_widget and isinstance(next_widget, tb.Button):
            next_widget = next_widget.tk_focusNext()
        # If a valid next widget is found, focus it
        if next_widget:
            next_widget.focus()
        return "break"
    
    def copy_mnemonic_to_clipboard(self, mnemonic=None, label=None, event=None, state=None):
        self.root.clipboard_clear()
        self.root.clipboard_append(mnemonic)
        label.config(text='Copied', foreground='#008000')

        if 'fade_copied_mnemonic_label' in self.root.event_handler.thread_event:
            self.root.wallet_thread_manager.stop_thread('fade_copied_mnemonic_label')

        #if 'fade_copied_mnemonic_label' in self.root.event_handler.thread_event and 'copied_mnemonic_label' in self.root.gui_utils.fade_text_widgets:
        #        self.root.gui_utils.fade_text_widgets['copied_mnemonic_label']['step'] = 1
        #        return
        #else:
        self.root.wallet_thread_manager.start_thread("fade_copied_mnemonic_label", self.root.gui_utils.fade_text, args=(label, 'copied_mnemonic_label', 1.25),)
    
    def set_label_image(self, label=None, image_path=None, width=None, height=None, state=None):
        image = Image.open(image_path)
        image = image.resize((width, height), Image.LANCZOS)
        image = ImageTk.PhotoImage(image)
        label.config(image=image)
        label.image = image
    
    def set_hyperlink(self, label=None, hyperlink_url=None, state=None):
        hyperlink_tag = f"hyperlink-{hyperlink_url}"
        start = self.root.send_page.tx_log.search(hyperlink_url, "1.0", tk.END)
      
        end = f"{start}+{len(hyperlink_url)}c"
      
        label.tag_add(hyperlink_tag, start, end)
        label.tag_config(hyperlink_tag, foreground="blue", underline=True)
        label.tag_bind(hyperlink_tag, "<Enter>", self.root.gui_utils.on_link_enter)
        label.tag_bind(hyperlink_tag, "<Leave>", self.root.gui_utils.on_link_leave)
        label.tag_bind(hyperlink_tag, "<Button-1>", lambda e, url=hyperlink_url: self.root.gui_utils.open_link(url))

class KeyToggle:
    def __init__(self, base_class, master=None, **kwargs):
        # Dynamically create a new class that inherits from both KeyToggle and the base_class
        self.__class__ = type(self.__class__.__name__, (self.__class__, base_class), {})
        base_class.__init__(self, master, **kwargs)  # Initialization of the base class
        self.visibility_on = False

import tkinter as tk

class HyperlinkLabel:
    """
    A class that creates a label-like widget with a portion of the text behaving as a hyperlink.
    Uses grid without extra spacing to keep the text segments tightly together.
    """
    def __init__(self, base_class, master=None, class_config=None, **kwargs):
        """
        :param base_class: The base Tk widget class to inherit from (e.g., tk.Label).
        :param master: The parent widget.
        :param class_config: Dictionary containing at least:
            'url':        The URL to open when the hyperlink is clicked
            'text':       The full text to display
            'link_text':  The portion of 'text' that should be clickable
        :param kwargs: Additional parameters to pass to the base class initializer.
        """
        # Dynamically create a new class that inherits from this and the base_class
        self.__class__ = type(self.__class__.__name__, (self.__class__, base_class), {})
        base_class.__init__(self, master, **kwargs)
        self.root = self.winfo_toplevel().master


        # Retrieve parameters
        self.url = class_config.get('url')
        self.text = class_config.get('text', "")
        self.link_text = class_config.get('link_text', "")

        # If link_text is empty, fall back to the URL as link_text
        if not self.link_text:
            self.link_text = self.url

        # Split the full text into before_link and after_link segments
        if self.link_text in self.text:
            before_link, after_link = self.text.split(self.link_text, 1)
        else:
            before_link, after_link = self.text, ""

        # Label for the text before the hyperlink
        if before_link:
            before_label = tb.Label(self, text=before_link, border=0, borderwidth=0)
            # Grid with no padding
            before_label.grid(row=0, column=0, sticky="w", padx=(2,0), pady=0)
        
        if '\n' in before_link:
            self.link_text = f'\n{self.link_text}'
        # Label for the hyperlink portion
        self.link_label = tb.Label(self, text=self.link_text, foreground="blue", cursor="hand2", underline=False, border=0, borderwidth=0)
        self.link_label.grid(row=0, column=1, sticky="w", padx=0, pady=0)

        # Bind hover and click events
        self.link_label.bind("<Enter>", self.on_enter)
        self.link_label.bind("<Leave>", self.on_leave)
        self.link_label.bind("<Button-1>", lambda e, url=self.url: self.root.gui_utils.open_link(url, show_link=True))

        # Label for the text after the hyperlink
        if after_link:
            after_label = tb.Label(self, text=after_link, border=0, borderwidth=0)
            after_label.grid(row=0, column=2, sticky="w", padx=0, pady=0)

        self.grid_columnconfigure(0, pad=0)
        self.grid_columnconfigure(1, pad=0)
        self.grid_columnconfigure(2, pad=0)

    def on_enter(self, event):
        """
        Change the hyperlink color and cursor on hover.
        """
        event.widget.config(foreground="red", cursor="hand2")

    def on_leave(self, event):
        """
        Revert the hyperlink color and cursor when the mouse leaves.
        """
        event.widget.config(foreground="blue", cursor="arrow")

   