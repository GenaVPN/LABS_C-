package org.example.Laba3;

import com.itextpdf.kernel.font.PdfFont;
import com.itextpdf.kernel.font.PdfFontFactory;
import com.itextpdf.kernel.pdf.PdfDocument;
import com.itextpdf.kernel.pdf.PdfWriter;
import com.itextpdf.layout.Document;
import com.itextpdf.layout.element.Cell;
import com.itextpdf.layout.element.Paragraph;
import com.itextpdf.layout.element.Table;
import javax.swing.table.DefaultTableModel;
import java.awt.*;
import java.util.Vector;

public class PDF {

    public static void createPDF(DefaultTableModel tableModel, String[] tableHeader){
        try {
            PdfFont font = PdfFontFactory.createFont("FONTS/arialmt.ttf");
            PdfWriter pdfWriter = new PdfWriter("TABLE.pdf");
            PdfDocument pdfDocument = new PdfDocument(pdfWriter);
            Table pdfTable = new Table(4);
            Vector<Vector> data = tableModel.getDataVector();


            for (String head: tableHeader){
                pdfTable.addHeaderCell(new Cell().add(new Paragraph(head).setFont(font)));
            }

            for (Vector row: data){
                for (Object obj: row){
                    String str = obj.toString();
                    Cell cell = new Cell().add(new Paragraph(str).setFont(font));
                    pdfTable.addCell(cell);
                }
            }

            Document doc = new Document(pdfDocument);
            doc.add(pdfTable);
            doc.close();
        }
        catch (Exception ex){
            System.out.print(ex);
        }
    }
}
