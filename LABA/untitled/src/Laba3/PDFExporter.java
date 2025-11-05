//package Laba3;
//
//import com.itextpdf.io.font.PdfEncodings;
//import com.itextpdf.io.image.ImageData;
//import com.itextpdf.io.image.ImageDataFactory;
//import com.itextpdf.kernel.colors.Color;
//import com.itextpdf.kernel.colors.DeviceRgb;
//import com.itextpdf.kernel.font.PdfFont;
//import com.itextpdf.kernel.font.PdfFontFactory;
//import com.itextpdf.kernel.geom.PageSize;
//import com.itextpdf.kernel.pdf.PdfDocument;
//import com.itextpdf.kernel.pdf.PdfWriter;
//import com.itextpdf.layout.Document;
//import com.itextpdf.layout.borders.Border;
//import com.itextpdf.layout.element.Cell;
//import com.itextpdf.layout.element.Image;
//import com.itextpdf.layout.element.Paragraph;
//import com.itextpdf.layout.element.Table;
//import com.itextpdf.layout.properties.HorizontalAlignment;
//import com.itextpdf.layout.properties.TextAlignment;
//import com.itextpdf.layout.properties.UnitValue;
//
//import javax.swing.*;
//import javax.swing.table.DefaultTableModel;
//import java.awt.*;
//import java.io.File;
//import java.io.IOException;
//import java.text.SimpleDateFormat;
//import java.util.Date;
//import java.util.Vector;
//
//public class PDFExporter {
//
//    // Цветовая схема для PDF
//    private static final DeviceRgb HEADER_COLOR = new DeviceRgb(41, 128, 185);
//    private static final DeviceRgb ACCENT_COLOR = new DeviceRgb(52, 152, 219);
//    private static final DeviceRgb LIGHT_GRAY = new DeviceRgb(245, 245, 245);
//
//    public static void exportTableToPDF(DefaultTableModel tableModel, JFrame parentFrame) {
//        // Проверка на пустую таблицу
//        if (tableModel.getRowCount() == 0) {
//            JOptionPane.showMessageDialog(parentFrame,
//                    "Таблица пуста. Нечего экспортировать.",
//                    "Ошибка",
//                    JOptionPane.WARNING_MESSAGE);
//            return;
//        }
//
//        // Диалог выбора файла
//        JFileChooser fileChooser = new JFileChooser();
//        fileChooser.setDialogTitle("Сохранить как PDF");
//        fileChooser.setSelectedFile(new File("каталог_роботов_пылесосов_" +
//                new SimpleDateFormat("yyyyMMdd_HHmmss").format(new Date()) + ".pdf"));
//
//        // Установка фильтра для PDF файлов
//        fileChooser.setFileFilter(new javax.swing.filechooser.FileFilter() {
//            @Override
//            public boolean accept(File f) {
//                return f.isDirectory() || f.getName().toLowerCase().endsWith(".pdf");
//            }
//
//            @Override
//            public String getDescription() {
//                return "PDF файлы (*.pdf)";
//            }
//        });
//
//        int userSelection = fileChooser.showSaveDialog(parentFrame);
//
//        if (userSelection == JFileChooser.APPROVE_OPTION) {
//            File fileToSave = fileChooser.getSelectedFile();
//
//            // Добавляем расширение .pdf если его нет
//            if (!fileToSave.getName().toLowerCase().endsWith(".pdf")) {
//                fileToSave = new File(fileToSave.getAbsolutePath() + ".pdf");
//            }
//
//            // Проверка на перезапись существующего файла
//            if (fileToSave.exists()) {
//                int overwrite = JOptionPane.showConfirmDialog(parentFrame,
//                        "Файл уже существует. Перезаписать?",
//                        "Подтверждение",
//                        JOptionPane.YES_NO_OPTION);
//                if (overwrite != JOptionPane.YES_OPTION) {
//                    return;
//                }
//            }
//
//            // Создание PDF в отдельном потоке с прогресс-баром
//            SwingWorker<Boolean, Void> worker = new SwingWorker<Boolean, Void>() {
//                @Override
//                protected Boolean doInBackground() throws Exception {
//                    try {
//                        createPDFDocument(tableModel, fileToSave.getAbsolutePath());
//                        return true;
//                    } catch (Exception e) {
//                        e.printStackTrace();
//                        return false;
//                    }
//                }
//
//                @Override
//                protected void done() {
//                    try {
//                        if (get()) {
//                            JOptionPane.showMessageDialog(parentFrame,
//                                    "<html><div style='text-align: center;'>" +
//                                            "<h3>✅ Экспорт завершен успешно!</h3>" +
//                                            "Файл сохранен как:<br><b>" + fileToSave.getName() + "</b><br>" +
//                                            "Расположение: " + fileToSave.getParent() +
//                                            "</div></html>",
//                                    "Успех",
//                                    JOptionPane.INFORMATION_MESSAGE);
//
//                            // Опционально: открыть файл после сохранения
//                            int openFile = JOptionPane.showConfirmDialog(parentFrame,
//                                    "Хотите открыть полученный PDF файл?",
//                                    "Открыть файл",
//                                    JOptionPane.YES_NO_OPTION);
//
//                            if (openFile == JOptionPane.YES_OPTION) {
//                                openPDFFile(fileToSave);
//                            }
//                        } else {
//                            throw new Exception("Ошибка при создании PDF");
//                        }
//                    } catch (Exception e) {
//                        JOptionPane.showMessageDialog(parentFrame,
//                                "Ошибка при экспорте в PDF: " + e.getMessage(),
//                                "Ошибка",
//                                JOptionPane.ERROR_MESSAGE);
//                    }
//                }
//            };
//
//            worker.execute();
//        }
//    }
//
//    private static void createPDFDocument(DefaultTableModel tableModel, String filePath) throws IOException {
//        PdfWriter writer = new PdfWriter(filePath);
//        PdfDocument pdfDoc = new PdfDocument(writer);
//        Document document = new Document(pdfDoc, PageSize.A4.rotate());
//
//        // Настройка документа
//        document.setMargins(20, 20, 20, 20);
//
//        try {
//            // Загрузка шрифта с поддержкой кириллицы
//            PdfFont font = PdfFontFactory.createFont("fonts/times.ttf", PdfEncodings.IDENTITY_H, true);
//            document.setFont(font);
//
//            // Заголовок документа
//            Paragraph title = new Paragraph("Каталог роботов-пылесосов")
//                    .setFontSize(18)
//                    .setFontColor(HEADER_COLOR)
//                    .setBold()
//                    .setTextAlignment(TextAlignment.CENTER)
//                    .setMarginBottom(20);
//            document.add(title);
//
//            // Информация о дате создания
//            Paragraph dateInfo = new Paragraph("Создано: " +
//                    new SimpleDateFormat("dd.MM.yyyy HH:mm").format(new Date()))
//                    .setFontSize(10)
//                    .setTextAlignment(TextAlignment.CENTER)
//                    .setMarginBottom(15);
//            document.add(dateInfo);
//
//            // Создание таблицы
//            float[] columnWidths = {3, 1, 1, 1}; // Ширины колонок
//            Table pdfTable = new Table(UnitValue.createPercentArray(columnWidths));
//            pdfTable.setWidth(UnitValue.createPercentValue(100));
//
//            // Заголовки таблицы
//            String[] headers = {"Модель", "Время работы (мин)", "Мощность (Pa)", "Цена (руб)"};
//            for (String header : headers) {
//                Cell headerCell = new Cell()
//                        .add(new Paragraph(header)
//                                .setFontSize(11)
//                                .setBold())
//                        .setBackgroundColor(HEADER_COLOR)
//                        .setFontColor(DeviceRgb.WHITE)
//                        .setTextAlignment(TextAlignment.CENTER)
//                        .setPadding(8);
//                pdfTable.addHeaderCell(headerCell);
//            }
//
//            // Данные таблицы
//            Vector<Vector> data = tableModel.getDataVector();
//            for (int i = 0; i < data.size(); i++) {
//                Vector row = data.get(i);
//                for (int j = 0; j < row.size(); j++) {
//                    String cellValue = row.get(j).toString();
//                    Cell dataCell = new Cell()
//                            .add(new Paragraph(cellValue)
//                                    .setFontSize(10))
//                            .setPadding(6);
//
//                    // Чередование цветов строк для лучшей читаемости
//                    if (i % 2 == 0) {
//                        dataCell.setBackgroundColor(LIGHT_GRAY);
//                    }
//
//                    // Выравнивание для числовых колонок
//                    if (j >= 1) { // Колонки с числами
//                        dataCell.setTextAlignment(TextAlignment.RIGHT);
//                    } else {
//                        dataCell.setTextAlignment(TextAlignment.LEFT);
//                    }
//
//                    pdfTable.addCell(dataCell);
//                }
//            }
//
//            document.add(pdfTable);
//
//            // Статистика в конце документа
//            Paragraph stats = new Paragraph("\n\nСтатистика: всего " + data.size() + " записей")
//                    .setFontSize(10)
//                    .setItalic()
//                    .setTextAlignment(TextAlignment.RIGHT);
//            document.add(stats);
//
//        } finally {
//            document.close();
//        }
//    }
//
//    private static void openPDFFile(File pdfFile) {
//        try {
//            if (Desktop.isDesktopSupported()) {
//                Desktop.getDesktop().open(pdfFile);
//            } else {
//                JOptionPane.showMessageDialog(null,
//                        "Не удалось открыть файл автоматически. Файл сохранен: " + pdfFile.getAbsolutePath(),
//                        "Информация",
//                        JOptionPane.INFORMATION_MESSAGE);
//            }
//        } catch (Exception ex) {
//            JOptionPane.showMessageDialog(null,
//                    "Ошибка при открытии файла: " + ex.getMessage() +
//                            "\nФайл сохранен: " + pdfFile.getAbsolutePath(),
//                    "Ошибка",
//                    JOptionPane.WARNING_MESSAGE);
//        }
//    }
//}