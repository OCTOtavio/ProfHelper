import customtkinter as ctk

from tkinter import messagebox
from tkinter import simpledialog

import database
import widgets.widgets as widgets

# widgets.py

WIDGET_MAP = widgets.widget_map

# ============================================================
# CONFIGURAÇÕES GLOBAIS
# ============================================================

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


# ============================================================
# ROOT
# ============================================================

class Root(ctk.CTk):

    # ========================================================
    # INIT
    # ========================================================

    def __init__(self):
        super().__init__()

        # ====================================================
        # DATABASE
        # ====================================================

        self.Database = database.Json_Manager()

        # ====================================================
        # WINDOW
        # ====================================================

        self.title("PROF HELPER")
        self.geometry("1200x800")
        self.minsize(1000, 700)

        # ====================================================
        # STORAGE
        # ====================================================

        self.ActiveWidgets = {}

        # Widgets de cada página
        self.Pages = {}

        # Frames já construídos
        self.PageFrames = {}

        self.CurrentPage = None

        self.DataPath = "data/data.json"
        self.Data = self.Database.Load(self.DataPath) or {}
        self.ProofManager = database.Proof_Manager({
            "DataPath": self.DataPath
        })

        # ====================================================
        # GRID
        # ====================================================

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # ====================================================
        # TOPBAR
        # ====================================================

        self.TopbarWidgets = [
            {
                "Id": "Topbar",
                "Type": "Frame",
                "master": self,

                "height": 80,
                "corner_radius": 0,

                "grid": {
                    "row": 0,
                    "column": 0,
                    "sticky": "ew"
                }
            }
        ]

        self.Create_Widgets(
            self.TopbarWidgets,
            self.ActiveWidgets
        )

        self.Topbar = self.ActiveWidgets["Topbar"]

        self.Topbar.grid_columnconfigure(0, weight=1)
        self.Topbar.grid_columnconfigure(1, weight=0)

        self.TopbarContent = [
            {
                "Id": "AppTitle",
                "Type": "Label",
                "master": self.Topbar,

                "text": "PROF HELPER",
                "font": ("Arial", 30, "bold"),

                "grid": {
                    "row": 0,
                    "column": 0,
                    "padx": 20,
                    "pady": 20,
                    "sticky": "w"
                }
            }
        ]

        self.Create_Widgets(
            self.TopbarContent,
            self.ActiveWidgets
        )

        # ====================================================
        # MAIN CONTAINER
        # ====================================================

        self.MainContainerWidgets = [
            {
                "Id": "MainContainer",
                "Type": "Frame",
                "master": self,

                "fg_color": "transparent",

                "grid": {
                    "row": 1,
                    "column": 0,
                    "sticky": "nsew"
                }
            }
        ]

        self.Create_Widgets(
            self.MainContainerWidgets,
            self.ActiveWidgets
        )

        self.MainContainer = self.ActiveWidgets["MainContainer"]

        self.MainContainer.grid_columnconfigure(0, weight=1)
        self.MainContainer.grid_rowconfigure(0, weight=1)

        # ====================================================
        # START PAGE
        # ====================================================

        self.Load_Data()
        self.Create_Pages()
        self.Goto("Home")

    # ========================================================
    # LOAD DATA
    # ========================================================

    def Load_Data(self):

        self.Data = self.Database.Load(
            self.DataPath,
            default={
                "Provas": {},
                "Alunos": {}
            }
        )

    # ========================================================
    # SAVE DATA
    # ========================================================

    def Save_Data(self):

        self.Database.Save(
            self.DataPath,
            self.Data
        )

    # ========================================================
    # CREATE PAGES
    # ========================================================

    def Create_Pages(self):

        provas = self.Data.get("Provas", {})
        alunos = self.Data.get("Alunos", {})

        self.Pages = {

            # ==================================================
            # HOME
            # ==================================================

            "Home": [

                {
                    "Id": "BtnProofs",
                    "Type": "Button",

                    "text": "Abrir Provas",
                    "height": 50,

                    "command": lambda: self.Goto("Proofs"),

                    "grid": {
                        "row": 0,
                        "column": 0,
                        "pady": (80, 10)
                    }
                },

                {
                    "Id": "BtnStudents",
                    "Type": "Button",

                    "text": "Cadastrar Aluno",
                    "height": 50,

                    "command": lambda: self.Goto("Students"),

                    "grid": {
                        "row": 1,
                        "column": 0,
                        "pady": 10
                    }
                }
            ],

            # ==================================================
            # PROOFS
            # ==================================================

            "Proofs": [

                {
                    "Id": "BtnBackProofs",
                    "Type": "Button",

                    "text": "← Voltar",

                    "command": lambda: self.Goto("Home"),

                    "grid": {
                        "row": 0,
                        "column": 0,
                        "sticky": "w",
                        "padx": 20,
                        "pady": 20
                    }
                },

                {
                    "Id": "BtnCreateProof",
                    "Type": "Button",

                    "text": "Cadastrar Prova",

                    "command": self.Create_Proof,

                    "grid": {
                        "row": 1,
                        "column": 0,
                        "sticky": "w",
                        "padx": 20
                    }
                },

                {
                    "Id": "ProofsTable",
                    "Type": "Table",

                    "Sections": [
                        "Id",
                        "Prova",
                        "Disciplina",
                        "Turma",
                        "Data",
                        "Funcoes"
                    ],

                    "Rows": self.Create_Table_Rows(

                        provas,

                        {

                            "Id": lambda key, item:
                                key,

                            "Prova": lambda key, item:
                                item.get("Nome", ""),

                            "Disciplina": lambda key, item:
                                item.get("Disciplina", ""),

                            "Turma": lambda key, item:
                                item.get("Turma", ""),

                            "Data": lambda key, item:
                                item.get("Data", ""),

                            "Funcoes": lambda key, item: [

                                {
                                    "Type": ctk.CTkButton,

                                    "text": "Editar",
                                    "width": 80,

                                    "command":
                                        lambda proof_id=key:
                                        self.Edit_Proof(
                                            proof_id
                                        )
                                },

                                {
                                    "Type": ctk.CTkButton,

                                    "text": "Excluir",
                                    "width": 80,

                                    "command":
                                        lambda proof_id=key:
                                        self.Delete_Proof(
                                            proof_id
                                        )
                                },

                                {
                                    "Type": ctk.CTkButton,

                                    "text": "Corrigir",
                                    "width": 80,

                                    "command":
                                        lambda proof_id=key:
                                        self.Correct_Proof(
                                            proof_id
                                        )
                                }
                            ]
                        }
                    ),

                    "grid": {
                        "row": 2,
                        "column": 0,
                        "sticky": "nsew",
                        "padx": 20,
                        "pady": 20
                    }
                }
            ],

            # ==================================================
            # STUDENTS
            # ==================================================

            "Students": [

                {
                    "Id": "BtnBackStudents",
                    "Type": "Button",

                    "text": "← Voltar",

                    "command": lambda: self.Goto("Home"),

                    "grid": {
                        "row": 0,
                        "column": 0,
                        "sticky": "w",
                        "padx": 20,
                        "pady": 20
                    }
                },

                {
                    "Id": "BtnCreateStudent",
                    "Type": "Button",

                    "text": "Cadastrar Aluno",

                    "command": self.Create_Student,

                    "grid": {
                        "row": 1,
                        "column": 0,
                        "sticky": "w",
                        "padx": 20
                    }
                },

                {
                    "Id": "StudentsTable",
                    "Type": "Table",

                    "Sections": [
                        "Id",
                        "Nome",
                        "Turma",
                        "Funcoes"
                    ],

                    "Rows": self.Create_Table_Rows(

                        alunos,

                        {

                            "Id": lambda key, item:
                                key,

                            "Nome": lambda key, item:
                                item.get("Nome", ""),

                            "Turma": lambda key, item:
                                item.get("Turma", ""),

                            "Funcoes": lambda key, item: [

                                {
                                    "Type": ctk.CTkButton,

                                    "text": "Editar",
                                    "width": 80,

                                    "command":
                                        lambda student_id=key:
                                        self.Edit_Student(
                                            student_id
                                        )
                                },

                                {
                                    "Type": ctk.CTkButton,

                                    "text": "Excluir",
                                    "width": 80,

                                    "command":
                                        lambda student_id=key:
                                        self.Delete_Student(
                                            student_id
                                        )
                                }
                            ]
                        }
                    ),

                    "grid": {
                        "row": 2,
                        "column": 0,
                        "sticky": "nsew",
                        "padx": 20,
                        "pady": 20
                    }
                }
            ]
        }

    def Create_Proof(self):

        widgets.ProofEditor(
            master=self,
            title="Nova Prova",

            on_save=lambda data: (
                self.ProofManager.Criar_Prova(data),
                self.Reload()
            )
        )

    def Edit_Proof(
        self,
        proof_id
    ):

        prova = self.Data["Provas"].get(
            proof_id
        )

        if not prova:

            messagebox.showerror(
                "Erro",
                "Prova não encontrada."
            )

            return

        widgets.ProofEditor(

            master=self,

            title=f"Editar Prova ({proof_id})",

            data=prova,

            on_save=lambda updates:
            self._Save_Proof_Edit(
                proof_id,
                updates
            )
        )

    def _Save_Proof_Edit(
        self,
        proof_id,
        updates
    ):

        self.ProofManager.Editar_Prova(
            proof_id,
            updates
        )

        self.Reload()

    def Delete_Proof(
        self,
        proof_id
    ):

        confirm = messagebox.askyesno(
            "Excluir",
            f"Deseja excluir a prova\n\n{proof_id}?"
        )

        if not confirm:
            return

        self.ProofManager.Excluir_Prova(
            proof_id
        )

        self.Reload()

    def Correct_Proof(
        self,
        proof_id
    ):

        widgets.ProofCorrectionWindow(

            master=self,

            proof_id=proof_id,

            proof_manager=self.ProofManager,

            on_save=lambda:
                self.Reload()
        )

    def Create_Student(self):

        widgets.StudentEditor(

            master=self,

            title="Novo Aluno",

            on_save=lambda data:
            self._Create_Student_Save(
                data
            )
        )

    def _Create_Student_Save(
        self,
        data
    ):

        aluno_id = data["Id"]

        self.Data["Alunos"][aluno_id] = {

            "Nome": data["Nome"],
            "Turma": data["Turma"],

            "Historico": [],
            "PossiveisColas": []
        }
        print("OI")

        self.Save_Data()

        self.Reload()

    def Edit_Student(
        self,
        student_id
    ):

        aluno = self.Data["Alunos"].get(
            student_id
        )

        if not aluno:
            return

        widgets.StudentEditor(

            master=self,

            title=f"Editar Aluno ({student_id})",

            data=aluno,

            on_save=lambda updates:
            self._Save_Student_Edit(
                student_id,
                updates
            )
        )

    def _Save_Student_Edit(
        self,
        student_id,
        updates
    ):

        self.Data["Alunos"][student_id].update(
            updates
        )

        print(f"UPDATES {updates}\n\nSTUDENT_ID: {student_id}\n\n ==========\n\nDATA: {self.Data}\n\n ==========")

        self.Save_Data()

        self.Reload()

    def Delete_Student(
        self,
        student_id
    ):

        confirm = messagebox.askyesno(

            "Excluir",

            f"Deseja excluir o aluno\n\n{student_id}?"
        )

        if not confirm:
            return

        del self.Data["Alunos"][student_id]

        self.Save_Data()

        self.Reload()

    def Refresh(self):

        current_page = self.CurrentPage or "Home"

        self.Load_Data()

        self.Pages.clear()

        for frame in self.PageFrames.values():
            frame.destroy()

        self.PageFrames.clear()

        self.Create_Pages()

        self.Goto(current_page)

    def Reload(self):

        self.Refresh()

    # ========================================================
    # CREATE WIDGETS
    # ========================================================

    def Create_Table_Rows(
        self,
        data,
        sections
    ):

        rows = []

        if not isinstance(data, dict):
            return rows

        for item_id, item_data in data.items():

            if not isinstance(item_data, dict):
                continue

            row = {}

            for column, value in sections.items():

                try:

                    if callable(value):

                        row[column] = value(
                            item_id,
                            item_data
                        )

                    else:

                        row[column] = item_data.get(
                            value,
                            ""
                        )

                except Exception as erro:

                    print(
                        f"[ERRO] Coluna '{column}': {erro}"
                    )

                    row[column] = ""

            rows.append(row)

        return rows

    def Create_Widgets(self, widgets, active_widgets):

        # ====================================================
        # MAP
        # ====================================================

        widget_map = WIDGET_MAP

        # ====================================================
        # LOOP
        # ====================================================

        for widget_data in widgets:

            widget_id = widget_data.get("Id")
            widget_type = widget_data.get("Type")

            # =================================================
            # VALIDATE
            # =================================================

            if widget_type not in widget_map:

                print("\n====================")
                print("WIDGET INVÁLIDO")
                print(widget_data)
                print("====================\n")

                continue

            widget_class = widget_map[widget_type]

            # =================================================
            # REMOVE SPECIAL KEYS
            # =================================================

            widget_args = {

                key: value

                for key, value in widget_data.items()

                    if key not in [
                        "Id",
                        "Type",
                        "pack",
                        "grid",
                        "place",
                        "Children"
                    ]
            }

            # =================================================
            # CREATE
            # =================================================

            widget = widget_class(**widget_args)

            # =================================================
            # SAVE REFERENCE
            # =================================================

            if widget_id:

                if widget_id in active_widgets:

                    try:
                        active_widgets[widget_id].destroy()
                    except:
                        pass

                active_widgets[widget_id] = widget

            # =================================================
            # LAYOUT
            # =================================================

            if "pack" in widget_data:
                widget.pack(**widget_data["pack"])

            elif "grid" in widget_data:
                widget.grid(**widget_data["grid"])

            elif "place" in widget_data:
                widget.place(**widget_data["place"])

            # =================================================
            # CHILDREN
            # =================================================

            if (
                "Children" in widget_data
                and widget_type != "Table"
            ):

                self.Create_Widgets(
                    widget_data["Children"],
                    active_widgets
                )

        return active_widgets

    # ========================================================
    # CLEAR PAGE
    # ========================================================

    def Clear_Page(self):

        for widget in self.MainContainer.winfo_children():
            widget.grid_forget()

    # ========================================================
    # GOTO PAGE
    # ========================================================

    def Goto(self, page_name):

        if page_name not in self.Pages:

            print(
                f"[ERRO] Página '{page_name}' não encontrada"
            )

            return

        self.Clear_Page()

        # ====================================================
        # BUILD PAGE
        # ====================================================

        if page_name not in self.PageFrames:

            frame = ctk.CTkFrame(
                self.MainContainer,
                fg_color="transparent"
            )

            frame.grid_columnconfigure(
                0,
                weight=1
            )

            # deixa qualquer tabela expandir
            for row in range(20):

                frame.grid_rowconfigure(
                    row,
                    weight=1 if row >= 2 else 0
                )

            widgets = []

            for widget_data in self.Pages[page_name]:

                widget_copy = widget_data.copy()

                widget_copy["master"] = frame

                widgets.append(
                    widget_copy
                )

            self.Create_Widgets(
                widgets,
                self.ActiveWidgets
            )

            self.PageFrames[page_name] = frame

        # ====================================================
        # SHOW PAGE
        # ====================================================

        self.PageFrames[page_name].grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        self.CurrentPage = page_name     
