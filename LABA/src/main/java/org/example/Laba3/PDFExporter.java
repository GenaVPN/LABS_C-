package org.example.Laba3;

import com.itextpdf.io.font.PdfEncodings;
import com.itextpdf.kernel.colors.DeviceRgb;
import com.itextpdf.kernel.font.PdfFont;
import com.itextpdf.kernel.font.PdfFontFactory;
import com.itextpdf.kernel.geom.PageSize;
import com.itextpdf.kernel.pdf.PdfDocument;
import com.itextpdf.kernel.pdf.PdfWriter;
import com.itextpdf.layout.Document;
import com.itextpdf.layout.element.Cell;
import com.itextpdf.layout.element.Paragraph;
import com.itextpdf.layout.element.Table;
import com.itextpdf.layout.properties.TextAlignment;
import com.itextpdf.layout.properties.UnitValue;

import javax.swing.*;
import javax.swing.filechooser.FileFilter;
import javax.swing.table.DefaultTableModel;
import java.awt.*;
import java.io.File;
import java.io.IOException;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.Vector;

public class PDFExporter {

    // Цветовая схема для PDF
    private static final DeviceRgb HEADER_COLOR = new DeviceRgb(41, 128, 185);
    private static final DeviceRgb ACCENT_COLOR = new DeviceRgb(52, 152, 219);
    private static final DeviceRgb LIGHT_GRAY = new DeviceRgb(245, 245, 245);

    public static void exportTableToPDF(DefaultTableModel tableModel, JFrame parentFrame) {
        // Проверка на пустую таблицу
        if (tableModel.getRowCount() == 0) {
            JOptionPane.showMessageDialog(parentFrame,
                    "Таблица пуста. Нечего экспортировать.",
                    "Ошибка",
                    JOptionPane.WARNING_MESSAGE);
            return;
        }

        // Диалог выбора файла
        JFileChooser fileChooser = new JFileChooser();
        fileChooser.setDialogTitle("Сохранить как PDF");
        fileChooser.setSelectedFile(new File("каталог_роботов_пылесосов_" +
                new SimpleDateFormat("yyyyMMdd_HHmmss").format(new Date()) + ".pdf"));

        // Установка фильтра для PDF файлов
        fileChooser.setFileFilter(new FileFilter() {
            @Override
            public boolean accept(File f) {
                return f.isDirectory() || f.getName().toLowerCase().endsWith(".pdf");
            }

            @Override
            public String getDescription() {
                return "PDF файлы (*.pdf)";
            }
        });

        int userSelection = fileChooser.showSaveDialog(parentFrame);

        if (userSelection == JFileChooser.APPROVE_OPTION) {
            File fileToSave = fileChooser.getSelectedFile();

            // Добавляем расширение .pdf если его нет
            if (!fileToSave.getName().toLowerCase().endsWith(".pdf")) {
                fileToSave = new File(fileToSave.getAbsolutePath() + ".pdf");
            }

            // Проверка на перезапись существующего файла
            if (fileToSave.exists()) {
                int overwrite = JOptionPane.showConfirmDialog(parentFrame,
                        "Файл уже существует. Перезаписать?",
                        "Подтверждение",
                        JOptionPane.YES_NO_OPTION);
                if (overwrite != JOptionPane.YES_OPTION) {
                    return;
                }
            }

            // Показываем прогресс-бар
            JProgressBar progressBar = new JProgressBar();
            progressBar.setIndeterminate(true);
            JOptionPane progressDialog = new JOptionPane(progressBar,
                    JOptionPane.INFORMATION_MESSAGE,
                    JOptionPane.DEFAULT_OPTION,
                    null,
                    new Object[]{});
            JDialog dialog = progressDialog.createDialog(parentFrame, "Создание PDF...");
            dialog.setDefaultCloseOperation(JDialog.DO_NOTHING_ON_CLOSE);

            // Создание PDF в отдельном потоке
            File finalFileToSave = fileToSave;
            SwingWorker<Boolean, Void> worker = new SwingWorker<Boolean, Void>() {
                @Override
                protected Boolean doInBackground() throws Exception {
                    try {
                        createPDFDocument(tableModel, finalFileToSave.getAbsolutePath());
                        return true;
                    } catch (Exception e) {
                        e.printStackTrace();
                        return false;
                    }
                }

                @Override
                protected void done() {
                    dialog.dispose(); // Закрываем диалог прогресса

                    try {
                        if (get()) {
                            JOptionPane.showMessageDialog(parentFrame,
                                    "<html><div style='text-align: center;'>" +
                                            "<h3>✅ Экспорт завершен успешно!</h3>" +
                                            "Файл сохранен как:<br><b>" + finalFileToSave.getName() + "</b><br>" +
                                            "Расположение: " + finalFileToSave.getParent() +
                                            "</div></html>",
                                    "Успех",
                                    JOptionPane.INFORMATION_MESSAGE);

                            // Опционально: открыть файл после сохранения
                            int openFile = JOptionPane.showConfirmDialog(parentFrame,
                                    "Хотите открыть полученный PDF файл?",
                                    "Открыть файл",
                                    JOptionPane.YES_NO_OPTION);

                            if (openFile == JOptionPane.YES_OPTION) {
                                openPDFFile(finalFileToSave);
                            }
                        } else {
                            JOptionPane.showMessageDialog(parentFrame,
                                    "Ошибка при создании PDF. Проверьте зависимости iText.",
                                    "Ошибка",
                                    JOptionPane.ERROR_MESSAGE);
                        }
                    } catch (Exception e) {
                        JOptionPane.showMessageDialog(parentFrame,
                                "Ошибка при экспорте в PDF: " + e.getMessage(),
                                "Ошибка",
                                JOptionPane.ERROR_MESSAGE);
                    }
                }
            };

            worker.execute();
            dialog.setVisible(true); // Показываем диалог прогресса
        }
    }

    private static void createPDFDocument(DefaultTableModel tableModel, String filePath) throws IOException {
        PdfWriter writer = new PdfWriter(filePath);
        PdfDocument pdfDoc = new PdfDocument(writer);
        Document document = new Document(pdfDoc, PageSize.A4.rotate());

        // Настройка документа
        document.setMargins(20, 20, 20, 20);

        try {
            // Используем стандартный шрифт (для простоты)
            // В идеале нужно указать путь к шрифту с поддержкой кириллицы
            PdfFont font;
            try {
                // Пробуем использовать шрифт Times
                font = PdfFontFactory.createFont("Times-Roman", PdfEncodings.WINANSI);
            } catch (Exception e) {
                // Если не получилось, используем стандартный
                font = PdfFontFactory.createFont();
            }
            document.setFont(font);

            // Заголовок документа
            Paragraph title = new Paragraph("Catalog of Robot Vacuum Cleaners")
                    .setFontSize(18)
                    .setFontColor(HEADER_COLOR)
                    .setBold()
                    .setTextAlignment(TextAlignment.CENTER)
                    .setMarginBottom(20);
            document.add(title);

            // Информация о дате создания
            Paragraph dateInfo = new Paragraph("Created: " +
                    new SimpleDateFormat("dd.MM.yyyy HH:mm").format(new Date()))
                    .setFontSize(10)
                    .setTextAlignment(TextAlignment.CENTER)
                    .setMarginBottom(15);
            document.add(dateInfo);

            // Создание таблицы
            float[] columnWidths = {3, 1, 1, 1}; // Ширины колонок
            Table pdfTable = new Table(UnitValue.createPercentArray(columnWidths));
            pdfTable.setWidth(UnitValue.createPercentValue(100));

            // Заголовки таблицы (на английском для избежания проблем с кириллицей)
            String[] headers = {"Model", "Work Time (min)", "Power (Pa)", "Price (RUB)"};
            for (String header : headers) {
                Cell headerCell = new Cell()
                        .add(new Paragraph(header)
                                .setFontSize(11)
                                .setBold())
                        .setBackgroundColor(HEADER_COLOR)
                        .setFontColor(DeviceRgb.WHITE)
                        .setTextAlignment(TextAlignment.CENTER)
                        .setPadding(8);
                pdfTable.addHeaderCell(headerCell);
            }

            // Данные таблицы
            Vector<Vector> data = tableModel.getDataVector();
            for (int i = 0; i < data.size(); i++) {
                Vector row = data.get(i);
                for (int j = 0; j < row.size(); j++) {
                    String cellValue = row.get(j).toString();
                    Cell dataCell = new Cell()
                            .add(new Paragraph(cellValue)
                                    .setFontSize(10))
                            .setPadding(6);

                    // Чередование цветов строк для лучшей читаемости
                    if (i % 2 == 0) {
                        dataCell.setBackgroundColor(LIGHT_GRAY);
                    }

                    // Выравнивание для числовых колонок
                    if (j >= 1) { // Колонки с числами
                        dataCell.setTextAlignment(TextAlignment.RIGHT);
                    } else {
                        dataCell.setTextAlignment(TextAlignment.LEFT);
                    }

                    pdfTable.addCell(dataCell);
                }
            }

            document.add(pdfTable);

            // Статистика в конце документа
            Paragraph stats = new Paragraph("\n\nStatistics: total " + data.size() + " records")
                    .setFontSize(10)
                    .setItalic()
                    .setTextAlignment(TextAlignment.RIGHT);
            document.add(stats);

        } finally {
            document.close();
        }
    }

    private static void openPDFFile(File pdfFile) {
        try {
            if (Desktop.isDesktopSupported()) {
                Desktop.getDesktop().open(pdfFile);
            } else {
                JOptionPane.showMessageDialog(null,
                        "Cannot open file automatically. File saved: " + pdfFile.getAbsolutePath(),
                        "Information",
                        JOptionPane.INFORMATION_MESSAGE);
            }
        } catch (Exception ex) {
            JOptionPane.showMessageDialog(null,
                    "Error opening file: " + ex.getMessage() +
                            "\nFile saved: " + pdfFile.getAbsolutePath(),
                    "Error",
                    JOptionPane.WARNING_MESSAGE);
        }
    }
}