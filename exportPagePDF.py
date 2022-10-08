
from PyPDF2 import PdfWriter, PdfReader

def readPDF(dir):
    reader = PdfReader(dir)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text

def newPDF(dir, page):
    reader = PdfReader(dir)
    writer = PdfWriter()

    writer.add_page(reader.pages[page]) #Adiciona uma pagina no PDF

    with open("PyPDF2-output.pdf", "wb") as fp: #Cria o novo PDF
        writer.write(fp) #Salva o novo PDF
    print("Processo Finalizado!")

if __name__ == "__main__":
    file = "C:/Users/hidek/Downloads/WS_Upload_Arquivos.pdf"
    textPDF = readPDF(file)
    newPDF(file, 5)