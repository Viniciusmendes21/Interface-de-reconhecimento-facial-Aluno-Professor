# Importações necessárias
import tkinter as tk  # Biblioteca para a criação da interface gráfica
from tkinter import messagebox, filedialog  # Módulos específicos para caixas de mensagem e seleção de arquivos
import cv2  # OpenCV para manipulação de vídeo e imagens
import os  # Biblioteca para operações com sistema operacional
import pickle  # Para serialização e desserialização de objetos Python
import imutils  # Utilitários para facilitar o uso do OpenCV
import numpy as np  # Biblioteca para operações numéricas
import datetime  # Para manipulação de datas e horas
import shutil  # Utilitários para operações de arquivos
import face_recognition

class SistemaReconhecimento(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        #CRIA FORMATAÇÃO DA JANELA
        self.title("Sistema de Reconhecimento Facial")
        self.geometry("330x100")
        self.resizable(width=False,height=False)

        #CRIA BOTÃO DE REGISTRAR PESSOA
        self.registrar_btn = tk.Button(self, text="Registrar Pessoa", command=lambda: self.abrir_janela_registro_pessoa())
        self.registrar_btn.grid(column=0, row=0, padx=10 ,pady=10)

        #CRIA BOTÃO DE RECONHECIMENTO EM TEMPO REAL
        self.reconhecer_btn = tk.Button(self, text="Reconhecimento em Tempo Real", command=self.iniciar_reconhecimento)
        self.reconhecer_btn.grid(column=1, row=0, padx=10 ,pady=10)

        #CRIA BOTÃO DE EXCLUIR REGISTRO
        self.excluir_btn = tk.Button(self, text="Excluir Registro", command=lambda: self.criar_janela_exclusao())
        self.excluir_btn.grid(column=0, row=1, padx=2 ,pady=2)

        #CRIA BOTÃO DE REGISTRO DE RECONHECIMENTO
        self.registro_btn = tk.Button(self, text="Registro Reconhecimento", command=lambda: self.criar_janela_registro_reconhecimento())
        self.registro_btn.grid(column=1, row=1, padx=2 ,pady=2)

    #CRIAÇÃO DE DUAS FUNÇÕES PARA O TEXTO NAS CAIXAS DE TEXTO SUMIREM LOGO QUANDO PRESSIONADOS PARA ESCREVER. (PLACEHOLDER)
    def on_entry_click(self, entry):
        if entry.get() in ['INICIAL - YYYYMMDD', 'FINAL - YYYYMMDD']:
            entry.delete(0, "end")  # Deleta o texto atual na caixa de entrada
            entry.insert(0, '')  # Insere texto vazio para começar a digitar
            entry.config(fg='black')
        if entry.get() == 'Nome do Registro':
            entry.delete(0, "end") # Deleta o texto atual na caixa de texto
            entry.config(fg='black') # Muda a cor do texto para preto

    def on_focusout(self, entry):
        if entry.get() == '':
            if entry == self.data_inicio_entry:
                entry.insert(0, 'INICIAL - YYYYMMDD')
            else:
                entry.insert(0, 'FINAL - YYYYMMDD')
            entry.config(fg='grey')
        if entry.get() == '':
            entry.insert(0, 'Nome do Registro') # Insere o texto padrão
            entry.config(fg='grey') # Muda a cor do texto para cinza

#-------------------------------- CRIAÇÃO DA JANELA DE REGISTRO DE PESSOAS --------------------------------
    def abrir_janela_registro_pessoa(self):
        #CRIA FORMATAÇÃO DA JANELA
        sub_janela = tk.Toplevel(self)
        sub_janela.title("Registrar Pessoa")
        sub_janela.geometry("500x100")
        sub_janela.resizable(width=False,height=False)

        #CRIA LABEL E CAIXA DE TEXTO PARA INSERCAO DA CATEGORIA DA PESSOA ESPECIFICA
        categoria_label = tk.Label(sub_janela, text="Escolha a sua categoria:")
        categoria_label.grid(row=0, column=0, padx=0, pady=5)

        def selecionar_categoria():
            print(self.categoria_var.get())

        # Variável para controlar a categoria selecionada
        self.categoria_var = tk.StringVar(value="Aluno")  # Inicializa com "Aluno"
        tk.Radiobutton(sub_janela, text="Aluno", variable=self.categoria_var, value=1, command=selecionar_categoria).grid(row=0, column=1)
        tk.Radiobutton(sub_janela, text="Professor", variable=self.categoria_var, value=2, command=selecionar_categoria).grid(row=0, column=2)

        #CRIA LABEL E CAIXA DE TEXTO PARA INSERÇÃO DO NOME
        nome_label = tk.Label(sub_janela, text="Digite o nome da pessoa que será registrada:")
        nome_label.grid(row=1, column=0, padx=10, pady=5)
        self.nome_entry = tk.Entry(sub_janela)
        self.nome_entry.grid(row=1, column=1, padx=10, pady=5)

        #CRIA BOTÃO DE CONFIRMAR
        confirmar_btn = tk.Button(sub_janela, text="Confirmar", command=self.registrar_pessoa)
        confirmar_btn.grid(row=2, columnspan=3, padx=10, pady=10)

#-------------------------------- CRIAÇÃO DA JANELA REGISTRO DE RECONHECIMENTO --------------------------------
    def criar_janela_registro_reconhecimento(self):
        #CRIA FORMATAÇÃO DA JANELA
        self.janela_registro = tk.Toplevel(self)
        self.janela_registro.title("Registro de Reconhecimento")
        self.janela_registro.geometry("270x120")
        self.janela_registro.resizable(width=False,height=False)

        data_label = tk.Label(self.janela_registro, text="   Insira a data inicial e final do período desejado:")
        data_label.grid(row=0, column=0, padx=0, pady=5)

        #CRIA CAMPO PARA DATA LIMITE INFERIOR
        self.data_inicio_entry = tk.Entry(self.janela_registro, fg='grey')
        self.data_inicio_entry.grid(column=0, row=1, padx=2, pady=2)
        self.data_inicio_entry.insert(0, 'INICIAL - YYYYMMDD')
        self.data_inicio_entry.bind('<FocusIn>', lambda event: self.on_entry_click(self.data_inicio_entry))
        self.data_inicio_entry.bind('<FocusOut>', lambda event: self.on_focusout(self.data_inicio_entry))

        #CRIA CAMPO PARA DATA LIMITE SUPERIOR
        self.data_fim_entry = tk.Entry(self.janela_registro, fg='grey')
        self.data_fim_entry.grid(column=0, row=2, padx=2, pady=2)
        self.data_fim_entry.insert(0, 'FINAL - YYYYMMDD')
        self.data_fim_entry.bind('<FocusIn>', lambda event: self.on_entry_click(self.data_fim_entry))
        self.data_fim_entry.bind('<FocusOut>', lambda event: self.on_focusout(self.data_fim_entry))

        #CRIA BOTÃO DE CONFIRMAR
        self.confirmar_btn = tk.Button(self.janela_registro, text="Confirmar", command=self.criar_relatorio)
        self.confirmar_btn.grid(column=0, row=3, padx=2, pady=2)

#-------------------------------- CRIAÇÃO DA JANELA DE EXCLUSÃO DE REGISTRO --------------------------------
    def criar_janela_exclusao(self):
        self.janela_exclusao = tk.Toplevel(self)
        self.janela_exclusao.title("Exclusão de Registro")
        self.janela_exclusao.geometry("280x140") #DIMENSÃO DA JANELA
        self.janela_exclusao.resizable(width=False,height=False)

        c_label = tk.Label(self.janela_exclusao, text="  Escolha de qual categoria deseja excluir o registro:")
        c_label.grid(row=0, column=0, padx=0, pady=5)

        self.categoria_var = tk.IntVar()
        self.categoria_var.set(1)  # Inicializa com aluno (1)
        tk.Radiobutton(self.janela_exclusao, text="Aluno", variable=self.categoria_var, value=1).grid(column=0, row=1, padx=0, pady=0)
        tk.Radiobutton(self.janela_exclusao, text="Professor", variable=self.categoria_var, value=2).grid(column=0, row=2, padx=0, pady=0)

        self.nome_registro_entry = tk.Entry(self.janela_exclusao, fg='grey')
        self.nome_registro_entry.grid(column=0, row=3, padx=2, pady=2)
        self.nome_registro_entry.insert(0, '    Nome do Registro')
        self.nome_registro_entry.bind('<FocusIn>', lambda event: self.on_entry_click(self.nome_registro_entry))
        self.nome_registro_entry.bind('<FocusOut>', lambda event: self.on_focusout(self.nome_registro_entry))

        self.confirmar_exclusao_btn = tk.Button(self.janela_exclusao, text="Confirmar", command=self.excluir_registro)
        self.confirmar_exclusao_btn.grid(column=0, row=4, padx=0, pady=4)

#-------------------------------- FUNÇÃO DE REGISTRO DE PESSOA --------------------------------
    def registrar_pessoa(self):
        registros = "pessoas\\"

        categoria = int(self.categoria_var.get())
        nome_registro = self.nome_entry.get()
        print(f"Categoria selecionada: {categoria}")
        print(f"Nome da pessoa: {nome_registro}")

        if categoria == 1:
            pasta_registro = os.path.join(registros, "aluno", nome_registro)
        elif categoria == 2:
            pasta_registro = os.path.join(registros, "professor", nome_registro)

        if os.path.exists(pasta_registro):
            # Se a pasta já existe, pede a confirmação do usuário
            opcao = input(f"O aluno {nome_registro} já existe. Deseja substituir? (S/N): ").lower()
            if opcao == 's'.lower():
                # Exclui a pasta existente
                shutil.rmtree(pasta_registro)
                print(f"Registro do aluno {nome_registro} substituído.")
            else:
                cat_input = int(input("Digite 1 para aluno e 2 para professor: "))
                if(cat_input == 1):
                    cat = "aluno"
                elif(cat_input ==2):
                    cat = "professor"
                # Oferece a possibilidade de alterar o nome
                novo_nome = input("Digite um novo nome para a pessoa: ")
                # Atualiza a pasta de registro com o novo nome
                pasta_registro = os.path.join(registros, cat, novo_nome)
                nome_registro = novo_nome
                print(f"Nome alterado para {novo_nome}.")

        if not os.path.exists(pasta_registro):
            os.makedirs(pasta_registro)

        cap = cv2.VideoCapture(0)  # 0 representa a câmera padrão

        limite_fotos = 5  # Altere para o número desejado
        fotos_tiradas = 0
        print("Aperte s para tirar foto")

        # Loop para ler e exibir cada quadro da webcam
        while fotos_tiradas < limite_fotos:
            # Leia o próximo quadro da webcam
            ret, frame = cap.read()

            # Exiba o quadro
            cv2.imshow('Webcam', frame)

            # Aguarde 25 milissegundos e verifique se a tecla 'q' foi pressionada para sair
            key = cv2.waitKey(25) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('s'):
                # Salve o frame como uma imagem (pode ajustar o nome do arquivo conforme necessário)
                nome_arquivo = f"{nome_registro}_{fotos_tiradas + 1}.jpg"
                caminho_arquivo = os.path.join(pasta_registro, nome_arquivo)
                cv2.imwrite(caminho_arquivo, frame)
                print(f"Aperte s para tirar foto - {fotos_tiradas + 1}/{limite_fotos} fotos tiradas")
                print(f"Frame {fotos_tiradas + 1} capturado e salvo em {caminho_arquivo}")

                fotos_tiradas += 1

        # Libere os recursos quando o loop terminar
        cap.release()
        cv2.destroyAllWindows()
        pass

#-------------------------------- FUNÇÃO PARA EXCLUIR REGISTRO --------------------------------
    def excluir_registro(self):
        registros = "pessoas\\"

        categoria = self.categoria_var.get()
        nome_registro = self.nome_registro_entry.get()

        if categoria == 1:
            pasta_registro = os.path.join(registros, "aluno", nome_registro)
        elif categoria == 2:
            pasta_registro = os.path.join(registros, "professor", nome_registro)
        if os.path.exists(pasta_registro):
            # Exclua a pasta do aluno ou professor
            shutil.rmtree(pasta_registro)
            print(f"Registro de {nome_registro} excluído com sucesso.")
        else:
            print(f"O registro de {nome_registro} não existe.")
        pass

#-------------------------------- FUNÇÃO QUE SALVA OS REGISTROS --------------------------------
    def carrega_encodings(self,path_dataset):
        list_encodings = []
        list_nomes = []
        list_categorias = []

        for role in ['aluno', 'professor']:
            role_path = os.path.join(path_dataset, role)

            if os.path.exists(role_path):
                subdirs = [os.path.join(role_path, f) for f in os.listdir(role_path)]

                for subdir in subdirs:
                    name = subdir.split(os.path.sep)[-1]

                    images_list = [os.path.join(subdir, f) for f in os.listdir(subdir) if not os.path.basename(f).startswith(".")]

                    for image_path in images_list:
                        img = cv2.imread(image_path)
                        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

                        print(name + '<-- '+ image_path)

                        face_roi = face_recognition.face_locations(img, model='cnn')

                        if face_roi:
                            (start_y, end_x, end_y, start_x) = face_roi[0]
                            roi = img[start_y:end_y, start_x:end_x]
                            roi = imutils.resize(roi, width=100)
                            #cv2.imshow("",cv2.cvtColor(roi, cv2.COLOR_RGB2BGR))

                            img_encoding = face_recognition.face_encodings(img, face_roi)[0]

                            list_encodings.append(img_encoding)
                            list_nomes.append(name)
                            list_categorias.append(role)  # Adiciona a categoria correspondente

                        else:
                            print('Não foi possível fazer o encoding da imagem --> {}'.format(image_path))
            else:
                print(f'Diretório {role} não encontrado em {path_dataset}')

        return list_encodings, list_nomes, list_categorias

#-------------------------------- FUNÇÃO PARA O RECONHECIMENTO FACIAL --------------------------------
    def reconhece_faces(self,imagem, lista_encodings, lista_nomes, list_cat, tolerancia=0.6):
        img_rgb = cv2.cvtColor(imagem, cv2.COLOR_BGR2RGB)
        localizacao_faces = face_recognition.face_locations(img_rgb)
        face_encodings = face_recognition.face_encodings(img_rgb, localizacao_faces)

        face_nomes = []
        conf = []
        categoria = []

        for encoding in face_encodings:
            if not lista_encodings:
                nome = 'Rosto nao reconhecido'
                categoria_nome = 'N/A'
                confianca = 0.0
            else:
                matches = face_recognition.compare_faces(lista_encodings, encoding, tolerance=tolerancia)
                nome = 'Rosto nao reconhecido'
                categoria_nome = 'N/A'
                distancias = face_recognition.face_distance(lista_encodings, encoding)

                if any(matches):
                    best_match_index = np.argmin(distancias)
                    nome = lista_nomes[best_match_index]
                    categoria_nome = list_cat[best_match_index]
                    confianca = 1 - distancias[best_match_index]
                else:
                    confianca = 0.0

            face_nomes.append(nome)
            categoria.append(categoria_nome)
            conf.append(confianca)

        localizacao_faces = np.array(localizacao_faces)
        return localizacao_faces.astype(int), face_nomes, conf, categoria

#-------------------------------- FUNÇÃO PARA O RECONHECIMENTO FACIAL OCORRER EM TEMPO REAL --------------------------------
    def reconhece_em_tempo_real(self,lista_encodings, lista_nomes, list_cat, max_width=700, tolerancia=0.6):
        cap = cv2.VideoCapture(0)  # Use the webcam as the video source

        while True:
            ret, frame = cap.read()  # Read a frame from the webcam
            localizacoes, nomes, confiancas, categorias = self.reconhece_faces(frame, lista_encodings, lista_nomes, list_cat, tolerancia)

            for face_loc, nome, conf, categoria in zip(localizacoes, nomes, confiancas, categorias):
                y1, x2, y2, x1 = face_loc[0], face_loc[1], face_loc[2], face_loc[3]

                # Verifica se há algum registro
                if not lista_encodings:
                    nome = 'Rosto nao reconhecido'
                    categoria = 'N/A'
                    conf = 0.0

                if nome != 'Rosto nao reconhecido':
                    self.processar_registro_presenca(nome, categoria)
                    cor_retangulo = (0, 255, 0)
                else:
                    cor_retangulo = (0, 0, 255)

                texto = f"{nome} ({categoria}): conf -> {conf:.2f}"  # Adiciona a categoria e confiança ao texto
                cv2.putText(frame, texto, (x1, y1 - 10), cv2.FONT_HERSHEY_DUPLEX, 0.8, cor_retangulo, 2)
                cv2.rectangle(frame, (x1, y1), (x2, y2), cor_retangulo, 4)

            if frame.shape[1] > max_width:
                frame = imutils.resize(frame, width=max_width)

            cv2.imshow("Reconhecimento em Tempo Real", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to exit the loop
                break

        cap.release()
        cv2.destroyAllWindows()

#-------------------------------- FUNÇÕES PARA SALVAMENTO EM TEMPO REAL E ATUALIZAÇÕES DE ARQUIVO --------------------------------
    def salvar_carregar_encodings(self, pasta_treino):
        # Carrega os encodings da pasta de treino
        list_encodings, list_names, list_cat = self.carrega_encodings(pasta_treino)

        # Salva os encodings em um arquivo pickle
        pickle_name = 'econding_atualizado.pickle'
        encodings_data = {"encodings": list_encodings, "names": list_names, "categoria": list_cat}

        with open(pickle_name, "wb") as f:
            pickle.dump(encodings_data, f)

        # Carrega os encodings de volta
        with open(pickle_name, "rb") as f:
            data_encodings = pickle.load(f)

        list_encodings = data_encodings["encodings"]
        list_names = data_encodings["names"]
        list_cat = data_encodings["categoria"]

        # Realiza o reconhecimento em tempo real
        self.reconhece_em_tempo_real(list_encodings, list_names, list_cat)
        pass

    def obter_nome_arquivo(self):
        data_atual = datetime.datetime.now()
        formato_data = data_atual.strftime("%Y%m%d")
        return f"{formato_data}.txt"

    def verificar_arquivo_existente(self,nome_arquivo):
        return os.path.exists(nome_arquivo)

    def gravar_registro_presenca(self, nome_arquivo, nome_registro, categoria):
        with open(nome_arquivo, "a") as arquivo:
            arquivo.write(f"{datetime.datetime.now()};{nome_registro};{categoria}\n")
        print(f"Registro de presença gravado em {nome_arquivo}")

    def processar_registro_presenca(self, nome_registro, categoria):
        nome_arquivo = self.obter_nome_arquivo()

        if not self.verificar_arquivo_existente(nome_arquivo):
            with open(nome_arquivo, "w") as arquivo:
                pass

        if not self.verificar_presenca_registrada(nome_arquivo, nome_registro):
            self.gravar_registro_presenca(nome_arquivo, nome_registro, categoria)


    def verificar_presenca_registrada(self,nome_arquivo, nome_registro):
        with open(nome_arquivo, "r") as arquivo:
            linhas = arquivo.readlines()
            for linha in linhas:
                if nome_registro in linha:
                    return True
        return False

#-------------------------------- FUNÇÃO NA QUAL INICIA O RECONHECIMENTO --------------------------------
    def iniciar_reconhecimento(self):
        list_encodings, list_names, list_cat = self.salvar_carregar_encodings("pessoas")
        self.reconhece_em_tempo_real(list_encodings, list_names, list_cat)

#-------------------------------- FUNÇÃO PARA CRIAR O RELATÓRIO COM O HISTÓRICO DE RECONHECIMENTO --------------------------------
    def criar_relatorio(self):
        # Pede ao usuário para selecionar um diretório que contenha os arquivos de texto
        pasta_arquivos = filedialog.askdirectory(title="Selecione o diretório dos arquivos de texto")

        if not pasta_arquivos:
            print("Nenhum diretório selecionado. Operação cancelada.")
            return

        data_inicio_str = self.data_inicio_entry.get()
        data_fim_str = self.data_fim_entry.get()

        # Converta as strings de data para objetos datetime
        try:
            data_inicio = datetime.datetime.strptime(data_inicio_str, '%Y%m%d')
            data_fim = datetime.datetime.strptime(data_fim_str, '%Y%m%d')
        except ValueError:
            messagebox.showerror("Erro", "Formato de data inválido. Use YYYYMMDD.")
            return

        # Lista para armazenar os registros reconhecidos durante o período
        registros_periodo = []

        # Variável para controlar se a última linha lida foi uma linha em branco
        ultima_linha_em_branco = False

        # Loop através dos dias do período
        while data_inicio <= data_fim:
            nome_arquivo = data_inicio.strftime('%Y%m%d') + ".txt"
            caminho_arquivo = os.path.join(pasta_arquivos, nome_arquivo)

            # Verifica se o arquivo existe antes de tentar lê-lo
            if os.path.exists(caminho_arquivo):
                with open(caminho_arquivo, 'r') as arquivo:
                    # Lê os registros do arquivo
                    registros_dia = arquivo.readlines()

                    # Remove as linhas em branco extras entre os dias
                    registros_dia = [linha.strip() for linha in registros_dia if linha.strip()]

                    # Adiciona as linhas lidas à lista
                    registros_periodo.extend(registros_dia)

                    # Verifica se a última linha lida foi uma linha em branco
                    ultima_linha_em_branco = not bool(registros_dia)

            # Incrementa a data para o próximo dia
            data_inicio += datetime.timedelta(days=1)

        # Remove a última linha em branco se houver mais de uma no final do arquivo
        if ultima_linha_em_branco and registros_periodo[-1] == '\n':
            registros_periodo.pop()

        # Cria um arquivo de relatório apenas se houver registros no período
        if registros_periodo:
            # Cria um arquivo de relatório com a adição da data
            data_atual = datetime.datetime.now().strftime("%Y-%m-%d")
            nome_relatorio = f"relatorio_{data_inicio_str}_{data_fim_str}.txt"

            with open(nome_relatorio, 'w') as relatorio:
                # Adiciona os registros coletados ao relatório
                relatorio.write('\n'.join(registros_periodo))
            print(f"Relatório criado em {nome_relatorio}.")
        else:
            print("Nenhum registro encontrado durante o período especificado. Nenhum relatório foi criado.")

if __name__ == "__main__":
    app = SistemaReconhecimento()
    app.mainloop()
