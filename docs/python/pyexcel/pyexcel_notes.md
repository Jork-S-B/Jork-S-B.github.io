## 📌 openpyxl==3.0.10

* 仅支持xlsx文件，读写xls文件可使用`xlwings`或`pandas`等库。
* 读取带筛选的excel文件报错：`Value must be either numerical or a string containing a wildcard`；降级为`openpyxl==3.0.10`即可。
* 保存excel文件，打开报错问题：`发现“xx.xlsx”中的部分内容有问题。是否让我们尽量尝试恢复？...`；降级为`openpyxl==3.0.10`即可。

### 🚁 插入超链接

=== "hyperlink_learn.py"

    ```python
    from openpyxl import Workbook
    from openpyxl.styles import Font
    from openpyxl.worksheet.hyperlink import Hyperlink
    
    wb = Workbook()
    ws = wb.active
    
    # 在A1插入超链接
    cell = ws.cell(row=1, column=1)
    cell.value = 'Click here'
    cell.font = Font(color='0000FF', underline='single')
    # cell.coordinate，用于表示单元格位置的属性，返回字符串如'A1'
    cell.hyperlink = Hyperlink(ref=cell.coordinate, target='https://www.python.org/')
    
    wb.save('hyperlink.xlsx')
    
    ```

### 🚁 设置样式、遍历方式、excel公式

=== "openpyxl_learn.py"

    ```python
    from openpyxl import load_workbook
    from openpyxl.styles import Font, Alignment, Border, Side

    wb = load_workbook('openpyxl_learn.xlsx')
    sheet = wb['Sheet']
    
    sheet.append(('A', 'B', 'C'))
    
    # 字体
    font = Font(name='等线', size=10, italic=True, color='FF0000', bold=True)
    # 对齐方式
    alignment = Alignment(horizontal='center', vertical='center',wrap_text=True)
    # 边框
    border = Border(left=Side(style='thin'), right=Side(style='thin'), top=Side(style='thin'), bottom=Side(style='thin'))
    
    # 切片方式访问
    for row_idx, row in enumerate(sheet['A1:C5'], start=1):
        sheet.row_dimensions[row_idx].height = 50  # 设置行高
        for cell in row:
            cell.font = font
            cell.alignment = alignment
            cell.border = border
            # print(cell.value)
    
    # 获取sheet中某一行，返回一个元组
    for cell in sheet.iter_rows(min_row=1, max_row=1, values_only=True):
        row_th = cell

    # 访问单个单元格
    _ = sheet.cell(row=5, column=1).value
    # 修改单元格的值
    _ = sheet.cell(row=5, column=1, value='修改').value

    sheet = wb['Sheet1']  
    # Sheet1_A1单元格的内容为excel公式“=SUM(Sheet!B:B)”
    print(sheet.cell(row=1, column=1).value)  # 打印"=SUM(Sheet!B:B)"

    # load_workbook()设置data_only=True，才会读取excel公式的计算结果

    wb.save('openpyxl_learn_bak.xlsx')

    ```

=== "openpyxl_learn.xlsx"

    [openpyxl_learn.xlsx](file/openpyxl_learn.xlsx)

---

参考资料：

1. [Python操作Excel库总结](https://zhuanlan.zhihu.com/p/353669230)
2. [openpyxl模块常用方法](https://www.cnblogs.com/programmer-tlh/p/10461353.html)
3. [openpyxl模块使用样式](https://zhuanlan.zhihu.com/p/154206853)
