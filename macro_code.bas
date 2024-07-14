
' VBA Module: Module1
Sub UpdateAfterAction()
    Dim topRow As Integer
    
    topRow = Range("rngReviews").Cells(1, 1).Row
    [valSelItem] = ActiveCell.Row() - topRow + 1
End Sub