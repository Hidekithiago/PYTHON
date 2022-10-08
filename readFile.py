#pip install pdfminer install pdfminer.six
#pdf2txt.py -o sample.csv readFile.pdf (Comando CMD para converter PDF para excel)

import re

text_arq = ""
arquivo = open('sample.csv', 'r')
for linha in arquivo:
    if (linha != "\n"):
        print('',linha)
        
        text_arq += linha
arquivo.close()
#print(text_arq)



nome_Empresa = re.search(r"(?<=Obrigado por escolher a )\w+", text_arq)
codReserva_Empresa = re.search(r"(?<=DE RESERVA\n)\d+", text_arq)

nome_Empresa = "Nome:; " + str(nome_Empresa.group(0))
codReserva = "Reserva:; " + str(codReserva_Empresa.group(0))
textRelatorio_Arq = "Dados Empresa \n" + nome_Empresa +"\n"+ codReserva



cnpj_Cliente = re.search(r"(?<=Cliente\n)\w+\.\w+\.\w+\/\w+\-\w+", text_arq)
nome_Cliente = re.search(r".*(?=\nObrigado por escolher a Unidas!)", text_arq)
nomeCondutor_Cliente = re.search(r"(?<=Condutor:\n).*", text_arq)

cnpj_Cliente = "CNPJ:; " + str(cnpj_Cliente.group(0))
nome_Cliente = "Nome Cliente:; " + str(nome_Cliente.group(0))
nomeCondutor_Cliente = "Nome Condutor:; " + str(nomeCondutor_Cliente.group(0))
textRelatorio_Arq += "\n\nDados Cliente \n" + cnpj_Cliente +"\n"+ nome_Cliente+"\n"+ nomeCondutor_Cliente



local_retDev = re.findall(r"(?<=LOCAL:\n).*", text_arq)
end_retDev = re.findall(r"(?<=End.:\n).*", text_arq)
cid_retDev = re.findall(r"(?<=Cidade:\n).*", text_arq)
tel_retDev = re.findall(r"(?<=Tel.:\n).*", text_arq)
email_retDev = re.findall(r"(?<=E-mail:\n).*", text_arq)
data_retDev = re.findall(r"(?<=DATA:\n).*", text_arq)
hora_retDev = re.findall(r"(?<=HORA:\n).*", text_arq)

local_Retirada = "Local:; " + str(local_retDev[0])
end_Retirada = "End:; " + str(end_retDev[0])
cid_Retirada = "Cidade:; " + str(cid_retDev[0])
tel_Retirada = "Tel:; " + str(tel_retDev[0])
email_Retirada = "Email:; " + str(email_retDev[1])
data_Retirada = "Data:; " + str(data_retDev[0])
hora_Retirada = "Hora:; " + str(hora_retDev[0])

textRelatorio_Arq += "\n\nDados Retirada \n" + local_Retirada +"\n"+ end_Retirada + "\n"+ cid_Retirada +"\n"+ tel_Retirada +"\n"+ email_Retirada +"\n"+ data_Retirada     + "\n"+ hora_Retirada +"\n"



local_Devolucao = "Local:; " + str(local_retDev[1])
end_Devolucao = "End:; " + str(end_retDev[1])
cid_Devolucao = "Cidade:; " + str(cid_retDev[1])
tel_Devolucao = "Tel:; " + str(tel_retDev[1])
email_Devolucao = "Email:; " + str(email_retDev[2])
data_Devolucao = "Data:; " + str(data_retDev[1])
hora_Devolucao = "Hora:; " + str(hora_retDev[1])

textRelatorio_Arq += "\n\nDados Devolucao \n" + local_Devolucao +"\n"+ end_Devolucao + "\n"+ cid_Devolucao +"\n"+ tel_Devolucao +"\n"+ email_Devolucao +"\n"+ data_Devolucao + "\n"+ hora_Devolucao +"\n"


f = open("demofile3.txt", "w")
f.write(text_arq)
f.close()
f = open("result.csv", "w")
print(textRelatorio_Arq)
f.write(textRelatorio_Arq)
f.close()
#open and read the file after the appending:
f = open("demofile3.txt", "r")
#print(f.read())