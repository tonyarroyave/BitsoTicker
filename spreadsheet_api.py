'''
Funciones para adquirir las worksheets e insertar los valores
'''

def get_all_worksheets(spreadsheet):    
    return [spreadsheet.get_worksheet(0),
            spreadsheet.get_worksheet(1),
            spreadsheet.get_worksheet(2),
            spreadsheet.get_worksheet(3)]

def insert_values(worksheet,values):
    worksheet.insert_row(values, worksheet.row_count + 1)