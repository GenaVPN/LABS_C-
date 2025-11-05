package Laba3;

import javax.swing.*;
import javax.swing.table.DefaultTableModel;

import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.util.Random;
import java.util.Vector;

public class Frame_programm extends JFrame {
    Random ran = new Random();
    private JLabel labelReturn;
    private Object[][] data = new Object[11][4];

    private String[] StringRand = {
            "Xiaomi Mi Robot",
            "Roborock S7",
            "iRobot Roomba",
            "Samsung Jet Bot",
            "Samsung New Robobot",
            "Dyson 360 Eye",
            "Ecovacs Deebot",
            "Neato Robotics",
            "LG Hom-Bot",
            "iLife A4",
            "Miele Scout",
            "Philips SmartPro",
            "Panasonic Rulo",
            "Coredy R650",
            "Eufy RoboVac",
            "Shark IQ",
            "Dream Vision D700",
            "Hobot 168",
            "Viomi S9",
            "Trifo Lucy"
    };

    private DefaultTableModel tableModel;

    JTextField name_field = new JTextField();
    JTextField time_field = new JTextField();
    JTextField power_field = new JTextField();
    JTextField price_field = new JTextField();


    private Object[] randomFill(){
        String randomName = StringRand[ran.nextInt(StringRand.length)];
        int time_of_work = (ran.nextInt(12)+6)*10;
        int power = (ran.nextInt(40)+10)*100;
        int price = (ran.nextInt(90) + 10)*1000;
        return new Object[]{randomName,time_of_work, power, price};
    }
    private void randomAdded(){
        tableModel.addRow(randomFill());
    }


    private void getMostRobotID(){
        Vector<Vector> a = tableModel.getDataVector();
        if (a.isEmpty()) {
            JOptionPane.showMessageDialog(this, "Таблица пуста", "Ошибка", JOptionPane.WARNING_MESSAGE);
            return;
        }
        int MostRobotPrice = (int) a.getFirst().get(3) ;
        int currentID = 0;
        for (int i = 1; i<a.size(); i++){
            if ((int) a.get(i).get(3) < MostRobotPrice){
                currentID = i;
                MostRobotPrice = (int) a.get(i).get(3);
            }

        }
        String str ="" + a.get(currentID);
        JOptionPane.showMessageDialog(this, str, "Самый бюджетный", JOptionPane.INFORMATION_MESSAGE);
    }

    private void getArifm(){
        Vector<Vector> a = tableModel.getDataVector();
        if (a.isEmpty()){
            JOptionPane.showMessageDialog(this, "Таблица пуста", "Ошибка", JOptionPane.WARNING_MESSAGE);
            return;
        }
        int sum = 0;
        for (Vector i: a){
            sum += (int) i.get(3);
        }

        float ar = sum/ (float)a.size();
        String str = String.format("Средняя стоимость пылесоса: %.2f Руб", ar);
        labelReturn.setText(str);
    }




    private void buttonAdded(){
        try {
            String name = name_field.getText();
            int time = Integer.parseInt(time_field.getText());
            int power = Integer.parseInt(power_field.getText());
            int price = Integer.parseInt(price_field.getText());
            Object[] obj = {name, time,power,price};
            name_field.setText("");
            time_field.setText("");
            power_field.setText("");
            price_field.setText("");
            tableModel.addRow(obj);
        }
        catch (Exception ex)  {
            JOptionPane.showMessageDialog(this, "Некорректные данные", "Ошибка", JOptionPane.ERROR_MESSAGE);
        }

    }

    Frame_programm(){
        for (int i =0; i<data.length; i++){
            data[i] = randomFill();
        }
        JPanel main_panel = new JPanel(new BorderLayout());
        main_panel.setBorder(BorderFactory.createEmptyBorder(10,10,10,10));


        String[] tableHeader = new String[]{"Модель", "Время работы (мин)", "Мощность всасывания (Pa)", "Цена (руб)"};
        tableModel = new DefaultTableModel(data, tableHeader){
            @Override
            public boolean isCellEditable(int row, int column) {
                return false;
            }
        };
        JTable table = new JTable(tableModel);
        table.setSelectionMode(ListSelectionModel.SINGLE_SELECTION);

        JScrollPane scrollPane = new JScrollPane(table);

        scrollPane.setBorder(BorderFactory.createMatteBorder(0,5,5,5,Color.GRAY));
        JPanel nort_panel = new JPanel();
        JPanel left_panel = new JPanel(new GridLayout(4,2, 10,5));
        JPanel leftPanelWButton = new JPanel(new BorderLayout(0,5));
        leftPanelWButton.setBorder(BorderFactory.createEmptyBorder(5,5,5,5));

        JButton button1 = new JButton("Самый бюджетный");
        button1.addActionListener(e -> getMostRobotID());
        JButton button2 = new JButton("Средняя цена");
        button2.addActionListener(e -> getArifm());
        JButton exportPDF = new JButton("Экспортировать в pdf");
//        exportPDF.addActionListener(e -> PDFExporter.exportTableToPDF(tableModel, Frame_programm.this));
        JButton delete = new JButton("Удалить строку");
        delete.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                Functional.deleteRowFromTable(table.getSelectedRow(), tableModel);
            }
        });

        JPanel panelButton = new JPanel(new BorderLayout(0,10));

        labelReturn = new JLabel("Выберите операцию");
        labelReturn.setHorizontalAlignment(JLabel.CENTER);



        JPanel panelWithButton = new JPanel(new GridLayout(2,2,5,5));
        panelWithButton.add(button1);
        panelWithButton.add(button2);
        panelWithButton.add(exportPDF);
        panelWithButton.add(delete);

        panelButton.add(panelWithButton, BorderLayout.CENTER);
        panelButton.add(labelReturn, BorderLayout.SOUTH);


        JLabel name = new JLabel("Название модели");
        JLabel timeWork = new JLabel("Время работы");
        JLabel power = new JLabel("Мощность");
        JLabel price = new JLabel("Цена");

        JButton buttonAdd = new JButton("Добавить");
        buttonAdd.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                buttonAdded();
            }
        });
        JButton randButton = new JButton("Добавить случайно");
        randButton.addActionListener(e -> randomAdded());

        JPanel leftbuttonPanel = new JPanel(new GridLayout(1,2,5,0));
        leftbuttonPanel.add(buttonAdd);
        leftbuttonPanel.add(randButton);



        left_panel.add(name);
        left_panel.add(name_field);
        left_panel.add(timeWork);
        left_panel.add(time_field);
        left_panel.add(power);
        left_panel.add(power_field);
        left_panel.add(price);
        left_panel.add(price_field);

        leftPanelWButton.add(left_panel, BorderLayout.CENTER);
        leftPanelWButton.add(leftbuttonPanel, BorderLayout.SOUTH);


        panelButton.setBorder(BorderFactory.createEmptyBorder(20,40,10,10));

        nort_panel.setLayout(new BorderLayout());
        nort_panel.setBorder(BorderFactory.createMatteBorder(5,5,5,5, Color.GRAY));
        nort_panel.add(leftPanelWButton, BorderLayout.WEST);
        nort_panel.add(panelButton, BorderLayout.EAST);

        main_panel.add(nort_panel, BorderLayout.NORTH);
        main_panel.add(scrollPane, BorderLayout.CENTER);


        setSize(new Dimension(700,500));
        setDefaultCloseOperation(EXIT_ON_CLOSE);
        setResizable(false);
        setVisible(true);
        add(main_panel);
    }
}
