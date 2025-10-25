import tkinter
from tkinter import filedialog
from PDF_Comparator import PDF_Comparator
import os


def select_file(entry):
    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    entry.delete(0, tkinter.END)
    entry.insert(0, file_path)
    return file_path


def compare_and_show():
    try:
        output = os.path.abspath(PDF_Comparator(entry1.get(), entry2.get()))
        os.startfile(output)
    except Exception as e:
        output = e
    var_result.set(output)


def copy_to_clipboard(text):
    root.clipboard_clear()
    root.clipboard_append(text)


root = tkinter.Tk()
root.title(u"PDF比較ツール")
root.geometry("600x200")
root.resizable(False, False)

select_file_frame1 = tkinter.Frame(root)
select_file_frame2 = tkinter.Frame(root)
select_file_frame1.pack(pady=10)
select_file_frame2.pack(pady=10)

label1 = tkinter.Label(select_file_frame1, text="変更後PDFファイル:")
label2 = tkinter.Label(select_file_frame2, text="変更前PDFファイル:")
label1.pack(side=tkinter.LEFT)
label2.pack(side=tkinter.LEFT)

entry1 = tkinter.Entry(select_file_frame1, width=60)
entry2 = tkinter.Entry(select_file_frame2, width=60)
entry1.pack(side=tkinter.LEFT, padx=10)
entry2.pack(side=tkinter.LEFT, padx=10)

button1 = tkinter.Button(select_file_frame1, text="参照", command=lambda: select_file(entry1))
button2 = tkinter.Button(select_file_frame2, text="参照", command=lambda: select_file(entry2))
button1.pack(side=tkinter.LEFT)
button2.pack(side=tkinter.LEFT)

button_compare = tkinter.Button(root, text="PDF比較実行", width=50, command=compare_and_show)
button_compare.pack(pady=10)

result_frame = tkinter.Frame(root)
result_frame.pack(pady=20)

label_result = tkinter.Label(result_frame, text="結果:")
label_result.pack(side=tkinter.LEFT)

var_result = tkinter.StringVar()
entry_result = tkinter.Entry(result_frame, textvariable=var_result, width=80, state="readonly")
entry_result.pack(side=tkinter.LEFT, padx=10)

button_copy = tkinter.Button(result_frame, text="コピー", command=lambda: copy_to_clipboard(var_result.get()))
button_copy.pack(side=tkinter.LEFT, padx=10)

root.mainloop()
