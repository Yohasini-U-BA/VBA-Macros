import win32com.client

def extract_vba_code(file_path, bas_file_path):
    excel = win32com.client.Dispatch("Excel.Application")
    workbook = excel.Workbooks.Open(file_path)
    vba_project = workbook.VBProject
    
    with open(bas_file_path, 'a') as bas_file:  # Open the .bas file in append mode
        for module in vba_project.VBComponents:
            if module.Type == 1:  # Standard Module
                code = module.CodeModule.Lines(1, module.CodeModule.CountOfLines)
                bas_file.write(f"\n' VBA Module: {module.Name}\n")
                bas_file.write(code)
    
    workbook.Close(SaveChanges=False)
    excel.Quit()

if __name__ == "__main__":
    file_path = r"D:\SG Hackathon\on-demand-details-in-excel-demo.xlsm"
    bas_file_path = r"D:\SG Hackathon\macro_code.bas"
    extract_vba_code(file_path, bas_file_path)
    print(f"VBA code extracted to {bas_file_path}")
