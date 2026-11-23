REM Paste into a LibreOffice Basic module: Tools > Macros > Organize Macros > Basic.
Option Explicit

Sub TrainMNIST
    Dim doc As Object, w As Object, s As Object
    Dim next1, next2, e As Long, row As Long, total As Long
    doc = ThisComponent
    w = doc.Sheets.getByName("Weights")
    s = doc.Sheets.getByName("Summary")
    total = CLng(s.getCellRangeByName("B6").Value)
    doc.lockControllers()
    On Error GoTo Failed
    For e = 1 To total
        doc.calculateAll()
        REM Capture BOTH next matrices before overwriting either current matrix.
        next1 = w.getCellRangeByPosition(1,44,785,59).getDataArray()
        next2 = w.getCellRangeByName("B65:R74").getDataArray()
        w.getCellRangeByPosition(1,4,785,19).setDataArray(next1)
        w.getCellRangeByName("B25:R34").setDataArray(next2)
        s.getCellRangeByName("B7").Value = s.getCellRangeByName("B7").Value + 1
        doc.calculateAll()
        row = 30 + CLng(s.getCellRangeByName("B7").Value)
        s.getCellByPosition(0,row).Value = s.getCellRangeByName("B7").Value
        s.getCellByPosition(1,row).Value = s.getCellRangeByName("B12").Value
        s.getCellByPosition(2,row).Value = s.getCellRangeByName("B10").Value
        s.getCellByPosition(3,row).Value = s.getCellRangeByName("B13").Value
        s.getCellByPosition(4,row).Value = s.getCellRangeByName("B11").Value
        If s.getCellRangeByName("B10").Value >= s.getCellRangeByName("B8").Value Then Exit For
    Next e
    doc.unlockControllers()
    MsgBox "Training complete. See Summary. Save as ODS to retain the macro."
    Exit Sub
Failed:
    doc.unlockControllers()
    MsgBox "Training stopped: " & Error$
End Sub

Sub ResetMNIST
    Dim doc As Object, w As Object, s As Object
    doc = ThisComponent
    w = doc.Sheets.getByName("Weights")
    s = doc.Sheets.getByName("Summary")
    w.getCellRangeByPosition(1,4,785,19).setDataArray(w.getCellRangeByPosition(1,84,785,99).getDataArray())
    w.getCellRangeByName("B25:R34").setDataArray(w.getCellRangeByName("B105:R114").getDataArray())
    s.getCellRangeByName("B7").Value = 0
    s.getCellRangeByName("A31:E10000").clearContents(7)
    doc.calculateAll()
End Sub
