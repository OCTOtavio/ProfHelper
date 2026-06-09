import traceback
from tkinter import messagebox

import database
import app


# ============================================
# DATABASE
# ============================================

Json_Manager = database.Json_Manager()


# ============================================
# PATHS
# ============================================

JSON_Paths = {
    "data": "data/data.json",
    "config": "data/config.json"
}


# ============================================
# LOAD JSON
# ============================================

def Load_JSON(arquivo=None, args=None):

    try:

        # ====================================
        # LOAD ESPECÍFICO
        # ====================================

        if arquivo:

            load = Json_Manager.Load(arquivo)

            # cria se não existir
            if load is None:

                created_path = Json_Manager.Create(args)

                return Json_Manager.Load(created_path)

            return load

        # ====================================
        # LOAD GLOBAL
        # ====================================

        values = {}

        for chave, valor in JSON_Paths.items():

            values[chave] = Json_Manager.Load(valor)

        return values

    except Exception as e:

        traceback.print_exc()

        messagebox.showerror(
            "ERRO NO APP",
            f"Erro ao carregar JSON:\n\n{e}"
        )

        return None

# ============================================
# INIT
# ============================================

def Init():
    try:
        # iniciar app
        App = app.Root()

        print("APP iniciado")

        App.mainloop()

    except Exception as e:

        traceback.print_exc()

        messagebox.showerror(
            "ERRO FATAL",
            f"O aplicativo encontrou um erro fatal:\n\n{e}"
        )

# ============================================
# START
# ============================================

if __name__ == "__main__":
    print("INICIO DO INICIO DO APP")
    Init()