import json

from pathlib import Path


# ============================================================
# JSON MANAGER
# ============================================================

class Json_Manager:

    # ========================================================
    # INIT
    # ========================================================

    def __init__(self):

        super().__init__()

    # ========================================================
    # LOAD
    # ========================================================

    def Load(self, arquivo, default=None):

        """
        Carrega um arquivo JSON.

        Args:
            arquivo (str): Caminho do arquivo.
            default (any): Valor padrão caso não exista.

        Returns:
            dict | list | any
        """

        caminho = Path(arquivo)

        # ================================================
        # NÃO EXISTE
        # ================================================

        if not caminho.exists():

            if default is not None:
                return default

            return {}

        # ================================================
        # LOAD
        # ================================================

        try:

            with open(caminho, "r", encoding="utf-8") as f:
                return json.load(f)

        except json.JSONDecodeError:

            print(
                f"[ERRO] JSON inválido: {arquivo}"
            )

            if default is not None:
                return default

            return {}

        except Exception as erro:

            print(
                f"[ERRO] Falha ao carregar '{arquivo}': {erro}"
            )

            if default is not None:
                return default

            return {}

    # ========================================================
    # SAVE
    # ========================================================

    def Save(self, arquivo, new):

        """
        Salva dados em um arquivo JSON.

        Args:
            arquivo (str): Caminho do arquivo.
            new (dict | list): Conteúdo.

        Returns:
            bool
        """

        try:

            caminho = Path(arquivo)

            # ============================================
            # CRIA PASTA
            # ============================================

            caminho.parent.mkdir(
                parents=True,
                exist_ok=True
            )

            # ============================================
            # SAVE
            # ============================================

            with open(caminho, "w", encoding="utf-8") as f:

                json.dump(
                    new,
                    f,
                    indent=4,
                    ensure_ascii=False
                )

            return True

        except Exception as erro:

            print(
                f"[ERRO] Falha ao salvar '{arquivo}': {erro}"
            )

            return False

    # ========================================================
    # CREATE
    # ========================================================

    def Create(self, args):

        """
        Cria um novo arquivo JSON.

        Args:
            {
                "Content": {},
                "Name": "dados.json",
                "Folder": "database",

                # opcionais
                "CreateFolderIfMissing": True,
                "CreateIfMissing": True
            }

        Returns:
            str
        """

        content = args.get("Content", {})
        name = args.get("Name")
        folder = args.get("Folder", "")

        create_folder = args.get(
            "CreateFolderIfMissing",
            True
        )

        create_if_missing = args.get(
            "CreateIfMissing",
            True
        )

        # ================================================
        # VALIDATE
        # ================================================

        if not name:

            raise ValueError(
                "Name é obrigatório."
            )

        pasta = Path(folder)

        # ================================================
        # CREATE FOLDER
        # ================================================

        if create_folder:

            pasta.mkdir(
                parents=True,
                exist_ok=True
            )

        caminho = pasta / name

        # ================================================
        # EXISTS
        # ================================================

        if caminho.exists() and not create_if_missing:

            raise FileExistsError(
                f"O arquivo já existe: {caminho}"
            )

        # ================================================
        # CREATE FILE
        # ================================================

        with open(caminho, "w", encoding="utf-8") as f:

            json.dump(
                content,
                f,
                indent=4,
                ensure_ascii=False
            )

        return str(caminho)

    # ========================================================
    # EXISTS
    # ========================================================

    def Exists(self, arquivo):

        """
        Verifica se um arquivo existe.
        """

        return Path(arquivo).exists()

    # ========================================================
    # DELETE
    # ========================================================

    def Delete(self, arquivo):

        """
        Deleta um arquivo.
        """

        try:

            caminho = Path(arquivo)

            if caminho.exists():

                caminho.unlink()

                return True

            return False

        except Exception as erro:

            print(
                f"[ERRO] Falha ao deletar '{arquivo}': {erro}"
            )

            return False

    # ========================================================
    # UPDATE KEY
    # ========================================================

    def Update_Key(
        self,
        arquivo,
        key,
        value
    ):

        """
        Atualiza uma chave do JSON.
        """

        try:

            data = self.Load(arquivo)

            data[key] = value

            self.Save(
                arquivo,
                data
            )

            return data

        except Exception as erro:

            print(
                f"[ERRO] Falha ao atualizar chave '{key}': {erro}"
            )

            return False

    # ========================================================
    # APPEND
    # ========================================================

    def Append(
        self,
        arquivo,
        key,
        value
    ):

        """
        Adiciona um item em uma lista.
        """

        try:

            data = self.Load(arquivo)

            # ============================================
            # CREATE KEY
            # ============================================

            if key not in data:

                data[key] = []

            # ============================================
            # VALIDATE
            # ============================================

            if not isinstance(data[key], list):

                raise TypeError(
                    f"'{key}' não é uma lista."
                )

            # ============================================
            # APPEND
            # ============================================

            data[key].append(value)

            # ============================================
            # SAVE
            # ============================================

            self.Save(
                arquivo,
                data
            )

            return data

        except Exception as erro:

            print(
                f"[ERRO] Falha ao adicionar item em '{key}': {erro}"
            )

            return False

    # ========================================================
    # REMOVE ITEM
    # ========================================================

    def Remove(
        self,
        arquivo,
        key,
        value
    ):

        """
        Remove item de uma lista.
        """

        try:

            data = self.Load(arquivo)

            # ============================================
            # VALIDATE
            # ============================================

            if key not in data:

                return False

            if not isinstance(data[key], list):

                raise TypeError(
                    f"'{key}' não é uma lista."
                )

            # ============================================
            # REMOVE
            # ============================================

            if value in data[key]:

                data[key].remove(value)

            # ============================================
            # SAVE
            # ============================================

            self.Save(
                arquivo,
                data
            )

            return data

        except Exception as erro:

            print(
                f"[ERRO] Falha ao remover item de '{key}': {erro}"
            )

            return False

    # ========================================================
    # READ KEY
    # ========================================================

    def Read_Key(
        self,
        arquivo,
        key,
        default=None
    ):

        """
        Lê uma chave específica.
        """

        try:

            data = self.Load(arquivo)

            return data.get(
                key,
                default
            )

        except Exception as erro:

            print(
                f"[ERRO] Falha ao ler chave '{key}': {erro}"
            )

            return default

    # ========================================================
    # RESET
    # ========================================================

    def Reset(
        self,
        arquivo,
        content=None
    ):

        """
        Reseta um arquivo JSON.
        """

        if content is None:
            content = {}

        return self.Save(
            arquivo,
            content
        )

    # ========================================================
    # MERGE
    # ========================================================

    def Merge(
        self,
        arquivo,
        new_data
    ):

        """
        Mescla dados em um JSON existente.
        """

        try:

            data = self.Load(arquivo)

            if not isinstance(data, dict):

                raise TypeError(
                    "O JSON precisa ser um dicionário."
                )

            if not isinstance(new_data, dict):

                raise TypeError(
                    "new_data precisa ser um dicionário."
                )

            # ============================================
            # MERGE
            # ============================================

            data.update(new_data)

            # ============================================
            # SAVE
            # ============================================

            self.Save(
                arquivo,
                data
            )

            return data

        except Exception as erro:

            print(
                f"[ERRO] Falha ao mesclar dados: {erro}"
            )

            return False

class Proof_Manager:

    def __init__(self, args):

        self.Database = Json_Manager()

        self.DataPath = args.get(
            "DataPath",
            "data/data.json"
        )

        self.Load_Data()

    def Load_Data(self):

        self.Data = self.Database.Load(
            self.DataPath,
            default={
                "Configuracoes": {},
                "Provas": {},
                "Alunos": {}
            }
        )

        self.Provas = self.Data.setdefault(
            "Provas",
            {}
        )

        self.Alunos = self.Data.setdefault(
            "Alunos",
            {}
        )

    def Save_Data(self):

        return self.Database.Save(
            self.DataPath,
            self.Data
        )

    def Criar_Prova(self, args):

        prova_id = args["Id"]

        if prova_id in self.Provas:

            raise ValueError(
                "Prova já existe."
            )

        self.Provas[prova_id] = {

            "Nome": args.get("Nome", ""),
            "Disciplina": args.get("Disciplina", ""),
            "Turma": args.get("Turma", ""),
            "Data": args.get("Data", ""),

            "Versoes": {},

            "ResultadosGerais": []
        }

        self.Save_Data()

        return self.Provas[prova_id]

    def Editar_Prova(
        self,
        prova_id,
        updates
    ):

        if prova_id not in self.Provas:
            return False

        self.Provas[prova_id].update(
            updates
        )

        self.Save_Data()

        return True

    def Excluir_Prova(
        self,
        prova_id
    ):

        if prova_id not in self.Provas:
            return False

        del self.Provas[prova_id]

        self.Save_Data()

        return True

    def Criar_Versao(
        self,
        prova_id,
        versao
    ):

        prova = self.Provas[prova_id]

        prova["Versoes"][versao] = {

            "Questoes": {},
            "Resultados": []
        }

        self.Save_Data()

    def Criar_Questao(self, args):

        prova_id = args["Prova"]
        versao = args["Versao"]
        questao_id = str(args["Id"])

        questao = {

            "Type": args["Type"],
            "Question": args["Question"],
            "Answer": args["Answer"],
            "Weight": args.get(
                "Weight",
                1
            ),
            "Required": args.get(
                "Required",
                True
            )
        }

        if "Tolerance" in args:

            questao["Tolerance"] = args[
                "Tolerance"
            ]

        self.Provas[prova_id] \
            ["Versoes"][versao] \
            ["Questoes"][questao_id] = questao

        self.Save_Data()

        return questao

class SolutionChecker:
    
    @staticmethod
    def Normalize(value):

        if value is None:
            return None

        if isinstance(value, str):

            return value.strip().upper()

        if isinstance(value, list):

            return [
                SolutionChecker.Normalize(v)
                for v in value
            ]

        if isinstance(value, dict):

            return {

                str(k):
                SolutionChecker.Normalize(v)

                for k, v in value.items()
            }

        return value
        
    @staticmethod
    def CheckSolution(
        solution,
        response,
        tolerance=0
    ):
        if isinstance(solution, (int, float)):

            try:

                return abs(
                    float(solution)
                    -
                    float(response)
                ) <= tolerance

            except:
                return False

        if isinstance(solution, list):

            return (
                SolutionChecker.Normalize(solution)
                ==
                SolutionChecker.Normalize(response)
            )

        if isinstance(solution, dict):

            return (
                SolutionChecker.Normalize(solution)
                ==
                SolutionChecker.Normalize(response)
            )

        return (

            SolutionChecker.Normalize(solution)

            ==

            SolutionChecker.Normalize(response)

        )

    def Corrigir_Prova(
        self,
        args
    ):

        aluno_id = args["Aluno"]
        prova_id = args["Prova"]
        versao = args["Versao"]

        respostas = args["Respostas"]

        prova = self.Provas[
            prova_id
        ]

        questoes = prova[
            "Versoes"
        ][versao][
            "Questoes"
        ]

        nota = 0

        peso_total = 0

        acertos = 0
        erros = 0

        status = {}

        for qid, questao in questoes.items():

            resposta = respostas.get(qid)

            correta = questao.get(
                "Answer"
            )

            peso = questao.get(
                "Weight",
                1
            )

            peso_total += peso

            resultado = SolutionChecker.CheckSolution(
                correta,
                resposta,
                questao.get(
                    "Tolerance",
                    0
                )
            )

            status[qid] = resultado

            if resultado:

                nota += peso
                acertos += 1

            else:

                erros += 1

        nota_final = 0

        if peso_total > 0:

            nota_final = (
                nota / peso_total
            ) * 10

        historico = self.Alunos[
            aluno_id
        ].setdefault(
            "Provas_Realizadas",
            []
        )

        historico.append({

            "Prova": prova_id,

            "Versao": versao,

            "Nota": nota_final,

            "Acertos": acertos,

            "Erros": erros,

            "Respostas": respostas,

            "Status": status
        })

        return {
            "Nota": nota_final,
            "Acertos": acertos,
            "Erros": erros,

            "Status": status,

            "Respostas": respostas,

            "Corretas": {
                qid: questao["Answer"]
                for qid, questao
                in questoes.items()
            }
        }