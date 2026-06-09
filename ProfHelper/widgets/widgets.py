import customtkinter as ctk
from tkinter import ttk

class Table(ctk.CTkFrame):

    def __init__(
        self,
        master,
        Sections=None,
        Rows=None,
        HeaderFont=("Arial", 15, "bold"),
        CellFont=("Arial", 13),
        **kwargs
    ):

        super().__init__(master, **kwargs)

        self.Sections = Sections or []
        self.Rows = Rows or []

        self.HeaderFont = HeaderFont
        self.CellFont = CellFont

        self.HeaderWidgets = []
        self.RowWidgets = []

        self.Build()

    # ========================================================
    # BUILD
    # ========================================================

    def Build(self):

        self.Clear()

        self.Create_Header()

        self.Create_Rows()

    # ========================================================
    # CLEAR
    # ========================================================

    def Clear(self):

        for widget in self.winfo_children():
            widget.destroy()

        self.HeaderWidgets.clear()
        self.RowWidgets.clear()

    # ========================================================
    # HEADER
    # ========================================================

    def Create_Header(self):

        for column, section in enumerate(self.Sections):

            self.grid_columnconfigure(
                column,
                weight=1
            )

            label = ctk.CTkLabel(
                self,
                text=str(section),
                font=self.HeaderFont
            )

            label.grid(
                row=0,
                column=column,
                padx=5,
                pady=(5, 10),
                sticky="ew"
            )

            self.HeaderWidgets.append(
                label
            )

    # ========================================================
    # ROWS
    # ========================================================

    def Create_Rows(self):

        for row_index, row_data in enumerate(
            self.Rows,
            start=1
        ):

            current_row = []

            for column, section in enumerate(
                self.Sections
            ):

                value = row_data.get(
                    section,
                    ""
                )

                # =====================================
                # WIDGETS
                # =====================================

                if (
                    isinstance(value, list)
                    and value
                    and isinstance(value[0], dict)
                ):

                    container = ctk.CTkFrame(
                        self,
                        fg_color="transparent"
                    )

                    container.grid(
                        row=row_index,
                        column=column,
                        padx=5,
                        pady=5,
                        sticky="ew"
                    )

                    current_row.append(
                        container
                    )

                    for widget_data in value:

                        widget_type = widget_data.get(
                            "Type"
                        )

                        if not widget_type:
                            continue

                        # ============================
                        # RESOLVE TYPE
                        # ============================

                        if isinstance(
                            widget_type,
                            str
                        ):

                            widget_class = widget_map.get(
                                widget_type
                            )

                        else:

                            widget_class = widget_type

                        if not widget_class:
                            continue

                        widget_args = {

                            key: value

                            for key, value
                            in widget_data.items()

                            if key not in [
                                "Type",
                                "pack",
                                "grid",
                                "place"
                            ]
                        }

                        widget = widget_class(
                            container,
                            **widget_args
                        )

                        if "pack" in widget_data:

                            widget.pack(
                                **widget_data["pack"]
                            )

                        elif "grid" in widget_data:

                            widget.grid(
                                **widget_data["grid"]
                            )

                        elif "place" in widget_data:

                            widget.place(
                                **widget_data["place"]
                            )

                        else:

                            widget.pack(
                                side="left",
                                padx=2
                            )

                    continue

                # =====================================
                # TEXTO
                # =====================================

                cell = ctk.CTkLabel(
                    self,
                    text=str(value),
                    font=self.CellFont
                )

                cell.grid(
                    row=row_index,
                    column=column,
                    padx=5,
                    pady=5,
                    sticky="ew"
                )

                current_row.append(
                    cell
                )

            self.RowWidgets.append(
                current_row
            )

    # ========================================================
    # SET ROWS
    # ========================================================

    def Set_Rows(
        self,
        rows
    ):

        self.Rows = rows

        self.Build()

    # ========================================================
    # ADD ROW
    # ========================================================

    def Add_Row(
        self,
        row
    ):

        self.Rows.append(
            row
        )

        self.Build()

    # ========================================================
    # REMOVE ROW
    # ========================================================

    def Remove_Row(
        self,
        index
    ):

        if 0 <= index < len(self.Rows):

            self.Rows.pop(
                index
            )

            self.Build()

    # ========================================================
    # UPDATE ROW
    # ========================================================

    def Update_Row(
        self,
        index,
        new_data
    ):

        if 0 <= index < len(self.Rows):

            self.Rows[index] = new_data

            self.Build()

    # ========================================================
    # GET ROW
    # ========================================================

    def Get_Row(
        self,
        index
    ):

        if 0 <= index < len(self.Rows):

            return self.Rows[index]

        return None

    # ========================================================
    # GET ALL ROWS
    # ========================================================

    def Get_Rows(self):

        return self.Rows

"""
class MessageBox(ctk.CTkTopLevel):
    def __init__(
        self,
        title,
        text,
        buttons={},
        color1,
        color2,
        delay=None
    ):
        super().__init__()

        self.title = title
        self.text = text
        self.buttons = buttons
        self.color1 = color1
        self.color2 = color2
"""


class StudentEditor(ctk.CTkToplevel):

    def __init__(
        self,
        master,
        title="Aluno",
        data=None,
        on_save=None
    ):

        super().__init__(master)

        self.Data = data or {}
        self.OnSave = on_save

        self.title(title)
        self.geometry("500x350")

        self.grab_set()

        # =====================================
        # ID
        # =====================================

        ctk.CTkLabel(
            self,
            text="ID"
        ).pack(
            pady=(20, 5)
        )

        self.IdEntry = ctk.CTkEntry(
            self
        )

        self.IdEntry.pack(
            fill="x",
            padx=20
        )

        self.IdEntry.insert(
            0,
            self.Data.get("Id", "")
        )

        # =====================================
        # NOME
        # =====================================

        ctk.CTkLabel(
            self,
            text="Nome"
        ).pack(
            pady=(10, 5)
        )

        self.NameEntry = ctk.CTkEntry(
            self
        )

        self.NameEntry.pack(
            fill="x",
            padx=20
        )

        self.NameEntry.insert(
            0,
            self.Data.get("Nome", "")
        )

        # =====================================
        # TURMA
        # =====================================

        ctk.CTkLabel(
            self,
            text="Turma"
        ).pack(
            pady=(10, 5)
        )

        self.ClassEntry = ctk.CTkEntry(
            self
        )

        self.ClassEntry.pack(
            fill="x",
            padx=20
        )

        self.ClassEntry.insert(
            0,
            self.Data.get("Turma", "")
        )

        # =====================================
        # BUTTONS
        # =====================================

        buttons = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        buttons.pack(
            pady=20
        )

        ctk.CTkButton(
            buttons,
            text="Salvar",
            command=self.Save
        ).pack(
            side="left",
            padx=5
        )

        ctk.CTkButton(
            buttons,
            text="Cancelar",
            command=self.destroy
        ).pack(
            side="left",
            padx=5
        )

    def Save(self):

        data = {

            "Id":
                self.IdEntry.get(),

            "Nome":
                self.NameEntry.get(),

            "Turma":
                self.ClassEntry.get()
        }

        if self.OnSave:

            self.OnSave(data)

        self.destroy()

class ProofEditor(ctk.CTkToplevel):

    def __init__(
        self,
        master,
        data=None,
        on_save=None
    ):

        super().__init__(master)

        self.Data = data or {

            "Versoes": {
                "A": {
                    "Questoes": {},
                    "Resultados": []
                }
            }
        }

        self.OnSave = on_save

        self.geometry(
            "1200x800"
        )

        self.title(
            "Editor de Prova"
        )

        self.Build()

    def Build(self):

        top = ctk.CTkFrame(self)

        top.pack(
            fill="x",
            padx=10,
            pady=10
        )

        self.IdEntry = ctk.CTkEntry(
            top,
            placeholder_text="ID"
        )

        self.IdEntry.pack(
            fill="x",
            pady=2
        )

        self.NameEntry = ctk.CTkEntry(
            top,
            placeholder_text="Nome"
        )

        self.NameEntry.pack(
            fill="x",
            pady=2
        )

        self.SubjectEntry = ctk.CTkEntry(
            top,
            placeholder_text="Disciplina"
        )

        self.SubjectEntry.pack(
            fill="x",
            pady=2
        )

        self.ClassEntry = ctk.CTkEntry(
            top,
            placeholder_text="Turma"
        )

        self.ClassEntry.pack(
            fill="x",
            pady=2
        )

        version_frame = ctk.CTkFrame(self)

        version_frame.pack(
            fill="x",
            padx=10,
            pady=5
        )

        self.VersionCombo = ctk.CTkComboBox(
            version_frame,
            values=list(
                self.Data["Versoes"].keys()
            )
        )

        self.VersionCombo.pack(
            side="left",
            padx=5
        )

        self.VersionCombo.set(
            list(
                self.Data["Versoes"].keys()
            )[0]
        )

        ctk.CTkButton(
            version_frame,
            text="Nova Versão",
            command=self.Add_Version
        ).pack(
            side="left",
            padx=5
        )

        ctk.CTkButton(
            version_frame,
            text="Remover Versão",
            command=self.Remove_Version
        ).pack(
            side="left",
            padx=5
        )

        self.Tree = ttk.Treeview(

            self,

            columns=(

                "Questao",
                "Tipo",
                "Peso"

            ),

            show="headings"
        )

        self.Tree.heading(
            "Questao",
            text="Questão"
        )

        self.Tree.heading(
            "Tipo",
            text="Tipo"
        )

        self.Tree.heading(
            "Peso",
            text="Peso"
        )

        self.Tree.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        self.Tree.bind(
            "<Double-1>",
            self.Edit_Question
        )

        buttons = ctk.CTkFrame(self)

        buttons.pack(
            fill="x",
            padx=10,
            pady=5
        )

        ctk.CTkButton(
            buttons,
            text="Adicionar Questão",
            command=self.Add_Question
        ).pack(
            side="left"
        )

        ctk.CTkButton(
            buttons,
            text="Remover Questão",
            command=self.Remove_Question
        ).pack(
            side="left",
            padx=5
        )

        ctk.CTkButton(
            buttons,
            text="Salvar Prova",
            command=self.Save
        ).pack(
            side="right"
        )

        self.VersionCombo.configure(
            command=lambda _:
            self.Refresh_Questions()
        )

        self.Refresh_Questions()

    def Current_Version(self):

        return self.VersionCombo.get()

    def Refresh_Questions(self):

        for item in self.Tree.get_children():
            self.Tree.delete(item)

        versao = self.Current_Version()

        questoes = self.Data[
            "Versoes"
        ][versao][
            "Questoes"
        ]

        for qid, q in questoes.items():

            self.Tree.insert(

                "",

                "end",

                iid=qid,

                values=(

                    qid,

                    q.get(
                        "Type"
                    ),

                    q.get(
                        "Weight"
                    )
                )
            )

    def Add_Version(self):

        letra = chr(

            ord(
                max(
                    self.Data[
                        "Versoes"
                    ].keys()
                )
            ) + 1
        )

        self.Data[
            "Versoes"
        ][letra] = {

            "Questoes": {},
            "Resultados": []
        }

        self.VersionCombo.configure(
            values=list(
                self.Data[
                    "Versoes"
                ].keys()
            )
        )

        self.VersionCombo.set(
            letra
        )

        self.Refresh_Questions()

    def Add_Question(self):

        QuestionEditor(

            self,

            on_save=
            self.Save_New_Question
        )

    def Save_New_Question(
        self,
        question
    ):

        versao = self.Current_Version()

        qid = str(

            len(

                self.Data[
                    "Versoes"
                ][versao][
                    "Questoes"
                ]

            ) + 1
        )

        self.Data[
            "Versoes"
        ][versao][
            "Questoes"
        ][qid] = question

        self.Refresh_Questions()



class ProofCorrectionWindow(ctk.CTkToplevel):

    def __init__(
        self,
        master,
        proof_manager,
        proof_id,
        on_save=None
    ):

        super().__init__(master)

        self.ProofManager = proof_manager
        self.ProofId = proof_id
        self.OnSave = on_save

        self.title(
            f"Correção - {proof_id}"
        )

        self.geometry(
            "1400x800"
        )

        self.grab_set()

        self.Create_UI()

    # =====================================================
    # UI
    # =====================================================

    def Create_UI(self):

        top = ctk.CTkFrame(self)

        top.pack(
            fill="x",
            padx=10,
            pady=10
        )

        ctk.CTkLabel(
            top,
            text="Aluno"
        ).pack(
            side="left",
            padx=5
        )

        alunos = list(
            self.ProofManager.Alunos.keys()
        )

        self.StudentBox = ctk.CTkComboBox(
            top,
            values=alunos
        )

        self.StudentBox.pack(
            side="left",
            padx=5
        )

        ctk.CTkButton(

            top,

            text="Iniciar Correção",

            command=self.Load_Questions

        ).pack(
            side="left",
            padx=10
        )

        # ==========================================
        # TABELA
        # ==========================================

        self.Table = EditableTable(

            self,

            Sections=[

                "Quest",
                "Resposta Aluno",
                "Resposta Correta",
                "Correto",
                "Nota",
                "Peso"

            ]
        )

        self.Table.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        # ==========================================
        # FINAL
        # ==========================================

        bottom = ctk.CTkFrame(self)

        bottom.pack(
            fill="x",
            padx=10,
            pady=10
        )

        ctk.CTkLabel(

            bottom,

            text="Nota Final"

        ).pack(
            side="left"
        )

        self.FinalGrade = ctk.CTkEntry(
            bottom,
            width=100
        )

        self.FinalGrade.pack(
            side="left",
            padx=10
        )

        ctk.CTkButton(

            bottom,

            text="Finalizar Correção",

            command=self.Save_Correction

        ).pack(
            side="right"
        )

    # =====================================================
    # LOAD QUESTIONS
    # =====================================================

    def Load_Questions(self):

        prova = self.ProofManager.Provas[
            self.ProofId
        ]

        versao = next(
            iter(
                prova["Versoes"]
            )
        )

        questoes = prova[
            "Versoes"
        ][versao][
            "Questoes"
        ]

        rows = []

        for qid, questao in questoes.items():

            rows.append({

                "Quest":
                    qid,

                "Resposta Aluno":
                    "",

                "Resposta Correta":
                    str(
                        questao.get(
                            "Answer",
                            ""
                        )
                    ),

                "Correto":
                    "0",

                "Nota":
                    "0",

                "Peso":
                    str(
                        questao.get(
                            "Weight",
                            1
                        )
                    )
            })

        self.Table.Set_Rows(
            rows
        )

    # =====================================================
    # CALCULATE
    # =====================================================

    def Calculate_Grade(self):

        nota = 0
        peso_total = 0

        for row in self.Table.Get_Data():

            try:

                peso = float(
                    row["Peso"]
                )

                valor = float(
                    row["Nota"]
                )

            except:

                continue

            nota += valor
            peso_total += peso

        if peso_total <= 0:
            return 0

        return (
            nota /
            peso_total
        ) * 10

    # =====================================================
    # SAVE
    # =====================================================

    def Save_Correction(self):

        nota = self.FinalGrade.get()

        if not nota:

            nota = self.Calculate_Grade()

        aluno = self.StudentBox.get()

        historico = self.ProofManager.Alunos[
            aluno
        ].setdefault(
            "Historico",
            []
        )

        historico.append({

            "Prova":
                self.ProofId,

            "Nota":
                float(nota),

            "Detalhes":
                self.Table.Get_Data()
        })

        self.ProofManager.Save_Data()

        if self.OnSave:

            self.OnSave()

        self.destroy()

class EditableTable(ctk.CTkScrollableFrame):

    def __init__(
        self,
        master,
        Sections=None,
        Rows=None,
        **kwargs
    ):

        super().__init__(
            master,
            **kwargs
        )

        self.Sections = Sections or []
        self.Rows = Rows or []

        self.Cells = []

        self.Build()

    def Build(self):

        for widget in self.winfo_children():
            widget.destroy()

        self.Cells.clear()

        for col, section in enumerate(
            self.Sections
        ):

            self.grid_columnconfigure(
                col,
                weight=1
            )

            ctk.CTkLabel(
                self,
                text=section,
                font=(
                    "Arial",
                    14,
                    "bold"
                )
            ).grid(
                row=0,
                column=col,
                padx=5,
                pady=5,
                sticky="ew"
            )

        for row_index, row in enumerate(
            self.Rows,
            start=1
        ):

            current = {}

            for col, section in enumerate(
                self.Sections
            ):

                value = row.get(
                    section,
                    ""
                )

                entry = ctk.CTkEntry(
                    self
                )

                entry.insert(
                    0,
                    str(value)
                )

                entry.grid(
                    row=row_index,
                    column=col,
                    padx=2,
                    pady=2,
                    sticky="ew"
                )

                current[section] = entry

            self.Cells.append(
                current
            )

    def Set_Rows(
        self,
        rows
    ):

        self.Rows = rows
        self.Build()

    def Get_Data(self):

        data = []

        for row in self.Cells:

            item = {}

            for section, widget in row.items():

                item[section] = widget.get()

            data.append(
                item
            )

        return data

class QuestionEditor(
    ctk.CTkToplevel
):

    QUESTION_TYPES = [

        "Radio",
        "Choices",
        "TrueFalse",
        "Dissertativa",
        "Numerica",
        "Associacao",
        "Ordem",
        "Other"
    ]

    def __init__(
        self,
        master,
        data=None,
        on_save=None
    ):

        super().__init__(
            master
        )

        self.Data = data or {}
        self.OnSave = on_save

        self.geometry(
            "800x700"
        )

        self.title(
            "Questão"
        )

        self.Build()

    def Build(self):

        ctk.CTkLabel(
            self,
            text="Tipo"
        ).pack()

        self.TypeCombo = ctk.CTkComboBox(
            self,
            values=self.QUESTION_TYPES
        )

        self.TypeCombo.pack(
            fill="x",
            padx=20
        )

        self.TypeCombo.set(
            self.Data.get(
                "Type",
                "Radio"
            )
        )

        ctk.CTkLabel(
            self,
            text="Pergunta"
        ).pack()

        self.QuestionBox = ctk.CTkTextbox(
            self,
            height=120
        )

        self.QuestionBox.pack(
            fill="x",
            padx=20
        )

        self.QuestionBox.insert(
            "0.0",
            self.Data.get(
                "Question",
                ""
            )
        )

        ctk.CTkLabel(
            self,
            text="Resposta"
        ).pack()

        self.AnswerBox = ctk.CTkTextbox(
            self,
            height=150
        )

        self.AnswerBox.pack(
            fill="x",
            padx=20
        )

        self.AnswerBox.insert(
            "0.0",
            str(
                self.Data.get(
                    "Answer",
                    ""
                )
            )
        )

        ctk.CTkLabel(
            self,
            text="Peso"
        ).pack()

        self.WeightEntry = ctk.CTkEntry(
            self
        )

        self.WeightEntry.pack(
            fill="x",
            padx=20
        )

        self.WeightEntry.insert(
            0,
            str(
                self.Data.get(
                    "Weight",
                    1
                )
            )
        )

        self.RequiredSwitch = ctk.CTkSwitch(
            self,
            text="Obrigatória"
        )

        self.RequiredSwitch.pack(
            pady=10
        )

        if self.Data.get(
            "Required",
            True
        ):
            self.RequiredSwitch.select()

        ctk.CTkButton(
            self,
            text="Salvar",
            command=self.Save
        ).pack(
            pady=20
        )

    def Save(self):

        data = {

            "Type":
                self.TypeCombo.get(),

            "Question":
                self.QuestionBox.get(
                    "0.0",
                    "end"
                ).strip(),

            "Answer":
                self.AnswerBox.get(
                    "0.0",
                    "end"
                ).strip(),

            "Weight":
                float(
                    self.WeightEntry.get()
                ),

            "Required":
                bool(
                    self.RequiredSwitch.get()
                )
        }

        if self.OnSave:
            self.OnSave(data)

        self.destroy()

widget_map = {

    "Frame": ctk.CTkFrame,
    "ScrollableFrame": ctk.CTkScrollableFrame,

    "Label": ctk.CTkLabel,
    "Button": ctk.CTkButton,
    "Textbox": ctk.CTkTextbox,
    "Entry": ctk.CTkEntry,

    "CheckBox": ctk.CTkCheckBox,
    "RadioButton": ctk.CTkRadioButton,
    "Switch": ctk.CTkSwitch,

    "OptionMenu": ctk.CTkOptionMenu,
    "ComboBox": ctk.CTkComboBox,

    "Slider": ctk.CTkSlider,
    "ProgressBar": ctk.CTkProgressBar,

    "Table": Table
}